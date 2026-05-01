# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

FHIRStarter is an ASGI [FHIR](https://hl7.org/fhir/) API framework built on top of FastAPI and the [fhir.resources](https://pypi.org/project/fhir.resources/) Pydantic models. It is published to PyPI as `fhirstarter` and is maintained by Canvas Medical against Canvas's business needs (rather than as a general-purpose project).

The framework supports three FHIR sequences: STU3, R4B, and R5. The active sequence is selected at process start via the `FHIR_SEQUENCE` environment variable (default `R5`); much of the package's import behavior branches on this value.

## Common commands

Dependency and environment management uses [uv](https://docs.astral.sh/uv/). Lint, format, and type-check are orchestrated through [prek](https://github.com/j178/prek), a Rust reimplementation of pre-commit (same `.pre-commit-config.yaml`).

```bash
uv sync                             # install dependencies (incl. dev group)
uv run pytest                       # run the full test suite (current FHIR sequence)
FHIR_SEQUENCE=STU3 uv run pytest
FHIR_SEQUENCE=R4B  uv run pytest
FHIR_SEQUENCE=R5   uv run pytest    # default
uv run pytest fhirstarter/tests/test_interactions.py::<test_name>  # single test

prek run --all-files                # all hooks (lint + format + type-check + file checks)
uv run ruff check fhirstarter       # lint only
uv run ruff format fhirstarter      # format only
uv run ty check                     # type-check only

uv run python -m fhirstarter.examples.example  # run the example server
uv build                            # produce wheel + sdist
```

CI (`.github/workflows/tests.yml`) runs `uv run --frozen pytest` across the full matrix of Python 3.8–3.13 × {STU3, R4B, R5}. A separate workflow (`.github/workflows/lint.yml`) runs `prek run --all-files` on every PR. When changing behavior that could differ between sequences, run all three locally before declaring done.

`ty` is in beta and produces false positives on the framework's dynamic patterns (FHIR Resource construction via `**{...}` kwarg expansion, dynamic type hints derived from `interaction.resource_type`, the decorator/wrapper pattern in `functions.py`). Several rules are silenced via `[[tool.ty.overrides]]` in `pyproject.toml` for the affected files; new files get full ty enforcement. Promote rules back to default as ty matures.

## Architecture

The framework's core idea is a **provider-decorator pattern**: developers register handler functions for FHIR interactions (read/update/patch/delete/create/search-type) and FHIRStarter generates the spec-conformant FastAPI routes from them. Developers never write the route signatures themselves — the framework wraps each handler at registration time so the wrapper's signature (param names, annotations, defaults) matches what FastAPI needs for OpenAPI generation and what the FHIR spec requires on the wire.

Key components and how they fit together:

- **`fhirstarter/fhirstarter.py`** — `FHIRStarter` (subclass of `FastAPI`). On construction it loads optional TOML config (custom search params, external-example proxy settings), installs three middleware (`_transform_search_type_post_request` → rewrites search POSTs into GETs by merging body/query params, `_transform_null_response_body` → strips `"null"` bodies that FastAPI emits for handlers returning `None`, `_set_content_type_header` → forces `application/fhir+json`), and registers exception handlers that turn errors into `OperationOutcome` resources. `add_providers` collects interactions, sorts them, and dispatches to `_add_route`.
- **`fhirstarter/providers.py`** — `FHIRProvider` holds a list of `TypeInteraction`s. Its `read`/`update`/`patch`/`delete`/`create`/`search_type` decorators register handlers. `_check_resource_type_module` enforces that the resource class comes from the correct `fhir.resources` submodule for the active `FHIR_SEQUENCE`.
- **`fhirstarter/interactions.py`** — `TypeInteraction` subclasses (`ReadInteraction`, `UpdateInteraction`, …) plus the `InteractionContext` dataclass passed as the first argument to every handler. `Callable` type aliases here define what a valid handler signature looks like.
- **`fhirstarter/functions.py`** — Generates the actual FastAPI path-operation callables (`make_read_function`, `make_search_type_function`, etc.). Has both async and non-async branches and rewrites function signatures via `inspect.Parameter`. **Search is the unusual case**: each resource type has a different set of search parameters, so the generated function takes `**kwargs` and its signature is patched after the fact. The module's docstring is essential reading before editing this file.
- **`fhirstarter/utils.py`** — `parse_fhir_request` (used by middleware to classify incoming requests), `*_route_args` helpers that build the kwargs passed to FastAPI's route decorators, `format_response` (handles JSON/XML and pretty-print), and `make_operation_outcome`.
- **`fhirstarter/openapi.py`** — Post-processes the generated OpenAPI schema to add FHIR-specific examples, response models, and external-documentation links. Returns the set of allow-listed external-example URLs that the `/_example` proxy can fetch.
- **`fhirstarter/exceptions.py`** — `FHIRException` hierarchy. Subclasses produce `OperationOutcome` responses with appropriate issue codes; `FHIRResourceNotFoundError` reads the parsed request to fill in the resource type and ID after the fact (`set_request` is called by the exception handler before `operation_outcome()`).
- **`fhirstarter/resources.py`** — Single import surface for `Bundle`, `CapabilityStatement`, `OperationOutcome`, and `Resource` that branches on `FHIR_SEQUENCE` so the rest of the codebase can import these types by a stable name.
- **`fhirstarter/fhir_specification/`** — Sequence-specific bundled data (search parameters, resource type lists, example resources) under `sequences/{STU3,R4B,R5}/`. `utils.py` selects the active sequence at import time and exposes loaders. `scripts/create_sequence_data.py` is the offline tool that scrapes hl7.org to regenerate these zip files; it is **not** run as part of normal development.
- **`fhirstarter/search_parameters.py`** — Loads built-in + extra + user-configured search parameters and supports the `[search-parameters.<Resource>.<name>]` TOML config sections shown in the README.

### Things that bite

- **Function signatures are load-bearing.** FastAPI introspects them for routing and OpenAPI generation. Changes in `functions.py` that look like cosmetic refactors (renaming a kwarg, changing a default) can silently change the API shape or docs. See `CONTRIBUTING.md` for the design rationale.
- **Async and sync handler paths are duplicated** in `functions.py`. When changing wrapper behavior, update both branches.
- **Resource types are sequence-locked.** Importing `from fhir.resources.patient import Patient` (R5) and running with `FHIR_SEQUENCE=R4B` will fail an assertion at provider registration time. Tests in `tests/resources.py` re-export resource types using the same branching trick as `resources.py`.
- **Search POST is rewritten to GET** by middleware before routing, so handlers always see GET-shaped requests. Don't add separate POST search handler logic.

## Tests

Tests live in `fhirstarter/tests/`. `conftest.py` parametrizes every test across both async and non-async handler implementations (`config.py` defines paired `*_async` / non-async functions for each interaction). `client_all` and `client_create_and_read` fixtures spin up a real `FHIRStarter` app backed by an in-memory `DATABASE` dict. There is no separate integration tier — the suite runs against the FastAPI `TestClient`.
