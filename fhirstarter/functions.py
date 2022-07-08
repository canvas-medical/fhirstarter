"""
Dynamic function creation for FHIR interactions.

The callables passed to FastAPI by FHIRStarter are created on the fly. A callable can be created
using the Python FunctionType type, and by passing it the following:

* A code object, compiled from dynamically-generated source code
* A dictionary of globals, which define all external symbols in the function template
* A tuple of argument defaults
* Type annotations

The four pieces of data above are necessary for FastAPI and FHIRStarter to automatically generate
a route for a FHIR interaction.

Note: How argument defaults are specified is not well-documented in the Python documentation.
      Argument defaults are counted backwards. For example, if a function has four arguments, and
      a tuple of three defaults are provided, then the first listed argument will not have a
      default, and the final three listed arguments will have defaults.
"""

from collections.abc import Mapping
from types import CodeType, FunctionType
from typing import Any

from fastapi import Body, Form, Path, Query, Request, Response
from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.resource import Resource

from .provider import InteractionCallable, ResourceType, TypeInteraction
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
    """
    Make a function suitable for creation of a FHIR search-type API route.

    Creation of a search-type function is more complex than creation of a create, read, or update
    function due to the variability of search parameters, and due to the need to support GET and
    POST.

    Search parameter descriptions are pulled from the FHIR specification.

    Aside from definition of globals, argument defaults, and annotations, the most important thing
    this function does is to set the "include_in_schema" value for each search parameter, based on
    the search parameters that the provided callable supports.
    """
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
                include_in_schema=False,
            )
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
    _, result_resource = _result_to_id_resource_tuple(result)

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
    callable_: InteractionCallable[ResourceType],
) -> FunctionType:
    """
    Return a dynamically-generated function.

    Given a string of source code, a mapping of annotations, a tuple of argument defaults, and a
    FHIR interaction callable that the created function will call, do the following:

    1. Compile the source code.
    2. Find the code object for the function.
    3. Define type annotations and globals (i.e. the function context).
    4. Create the function and annotate it.
    5. Return the function.
    """
    code = compile(source, "<string>", "exec")
    func_code = next(c for c in code.co_consts if isinstance(c, CodeType))

    annotations |= {"request": Request, "response": Response}

    globals_ = {
        "_result_to_id_resource_tuple": _result_to_id_resource_tuple,
        "callable_": callable_,
    }

    func = FunctionType(code=func_code, globals=globals_, argdefs=argdefs)
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
