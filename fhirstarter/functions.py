from collections.abc import Callable, Mapping
from types import FunctionType
from typing import Any

from fastapi import Body, Form, Path, Query, Request, Response
from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.resource import Resource

from .provider import ResourceType, TypeInteraction
from .search_parameters import (
    fhir_sp_name_to_var_sp_name,
    load_search_parameters,
    supported_search_parameters,
    var_sp_name_to_fhir_sp_name,
)


def make_create_function(interaction: TypeInteraction[ResourceType]) -> FunctionType:
    """Make a function suitable for creation of a FHIR create API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    source = f"""async def {resource_type_str.lower()}_create(request, response, resource):
    \"\"\"
    Function for {resource_type_str} {interaction.interaction_type.value} interaction.

    Calls the callable, and sets the Location header based on the Id of the created resource.
    \"\"\"
    result = await callable_(resource, request=request)
    id_, result_resource = _result_to_id_resource_tuple(result)

    response.headers["Location"] = f"{{request.base_url}}{resource_type_str}/{{id_}}/_history/1"

    return result_resource"""

    return _make_function(
        source=source,
        annotations={
            "resource": interaction.resource_type,
            "return": interaction.resource_type | None,
        },
        argdefs=(
            Body(
                None,
                media_type="application/fhir+json",
                alias=resource_type_str,
            ),
        ),
        callable_=interaction.callable_,
    )


def make_read_function(interaction: TypeInteraction[ResourceType]) -> FunctionType:
    """Make a function suitable for creation of a FHIR read API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    source = f"""async def {resource_type_str.lower()}_read(request, response, id_):
    \"\"\"Function for {resource_type_str} {interaction.interaction_type.value} interaction.\"\"\"
    return await callable_(id_, request=request)"""

    return _make_function(
        source=source,
        annotations={"id_": Id, "return": interaction.resource_type},
        argdefs=(
            Path(
                None,
                alias="id",
                description=Resource.schema()["properties"]["id"]["title"],
            ),
        ),
        callable_=interaction.callable_,
    )


# TODO: If possible, map FHIR primitives to correct type annotations for better validation
def make_search_type_function(
    interaction: TypeInteraction[ResourceType], post: bool
) -> FunctionType:
    """Make a function suitable for creation of a FHIR search-type API route."""
    resource_type_str = interaction.resource_type.get_resource_type()
    http_method = "post" if post else "get"

    search_parameters = load_search_parameters()[
        interaction.resource_type.get_resource_type()
    ]
    arg_names = tuple(
        fhir_sp_name_to_var_sp_name(name) for name in sorted(search_parameters.keys())
    )
    callable_kwargs = ", ".join((f"{name}={name}" for name in arg_names))

    source = f"""async def {resource_type_str.lower()}_search_{http_method}(request, response, {", ".join(arg_names)}):
    \"\"\"Function for {resource_type_str} {interaction.interaction_type.value} interaction.\"\"\"
    return await callable_({callable_kwargs})"""

    supported_search_parameters_ = set(
        supported_search_parameters(interaction.callable_)
    )

    if post:
        argdefs = tuple(
            Form(
                None,
                alias=var_sp_name_to_fhir_sp_name(name),
                description=search_parameters[var_sp_name_to_fhir_sp_name(name)][
                    "description"
                ],
            )
            if name in supported_search_parameters_
            else Query(
                None,
                alias=var_sp_name_to_fhir_sp_name(name),
                description=search_parameters[var_sp_name_to_fhir_sp_name(name)][
                    "description"
                ],
                include_in_schema=False)
            for name in arg_names
        )
    else:
        argdefs = tuple(
            Query(
                None,
                alias=var_sp_name_to_fhir_sp_name(name),
                description=search_parameters[var_sp_name_to_fhir_sp_name(name)][
                    "description"
                ],
                include_in_schema=name in supported_search_parameters_,
            )
            for name in arg_names
        )

    return _make_function(
        source=source,
        annotations={name: str for name in arg_names} | {"return": Bundle},
        argdefs=argdefs,
        callable_=interaction.callable_,
    )


def make_update_function(interaction: TypeInteraction[ResourceType]) -> FunctionType:
    """Make a function suitable for creation of a FHIR update API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    source = f"""async def {resource_type_str.lower()}_update(request, response, id_, resource):
    \"\"\"Function for {resource_type_str} {interaction.interaction_type.value} interaction.\"\"\"
    result = await callable_(id_, resource, request=request)
    _, result_resource = result_to_id_resource_tuple(result)

    return result_resource"""

    return _make_function(
        source=source,
        annotations={
            "id_": Id,
            "resource": interaction.resource_type,
            "return": interaction.resource_type | None,
        },
        argdefs=(
            Path(
                None,
                alias="id",
                description=Resource.schema()["properties"]["id"]["title"],
            ),
            Body(
                None,
                media_type="application/fhir+json",
                alias=resource_type_str,
            ),
        ),
        callable_=interaction.callable_,
    )


def _make_function(
    source: str,
    annotations: Mapping[str, Any],
    argdefs: tuple[Any, ...],
    callable_: Callable[[...], Any],
) -> FunctionType:
    code = compile(source, "<string>", "exec")

    annotations |= {"request": Request, "response": Response}

    globals_ = {
        "_result_to_id_resource_tuple": _result_to_id_resource_tuple,
        "callable_": callable_,
    }

    func = FunctionType(code=code, globals=globals_, argdefs=argdefs)
    func.__annotations__ = annotations

    return func


def _result_to_id_resource_tuple(
    result: Id | Resource,
) -> tuple[Id | None, Resource | None]:
    """
    Given an Id or a Resource, return an Id and a Resource.

    If a Resource is provided, both an Id and a Resource can be returned, however if an Id is
    provided, then only the Id can be returned.
    """
    if isinstance(result, Resource):
        return result.id, result
    else:
        return result, None
