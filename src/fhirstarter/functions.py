"""
Dynamic function creation for FHIR interactions.

The callables passed to FastAPI by FHIRStarter are created using functional programming techniques.
The create, read, and updates use cases are fairly straightforward -- these functions simply call a
developer-provided handler, perform some FHIR-related processing, and return the result up the
chain.

The search use case is slightly more complicated. Because each FHIR resource type has a different
set of search parameters (i.e. query parameters), the approach used for the create, read, and update
use cases to create the callables does not work. Instead, a function that takes arbitrary kwargs is
created, and the function signature is modified afterward to provide the information needed by
FastAPI for documentation purposes: variable name, annotation, and default value.
"""

import keyword
from collections.abc import Callable, Coroutine
from inspect import Parameter, signature
from typing import cast

from fastapi import Body, Form, Path, Query, Request, Response
from fhir.resources.fhirtypes import Id
from fhir.resources.resource import Resource

from .exceptions import FHIRBadRequestError
from .interactions import (
    CreateInteractionHandler,
    InteractionContext,
    ReadInteractionHandler,
    ResourceType,
    SearchTypeInteractionHandler,
    TypeInteraction,
    UpdateInteractionHandler,
)
from .search_parameters import (
    search_parameter_sort_key,
    supported_search_parameters,
    var_name_to_qp_name,
)
from .utils import FormatParameters, format_response

_FORMAT_PARAMETER_DESCRIPTION = (
    "Override the HTTP content negotiation to specify JSON or XML response format"
)
_PRETTY_PARAMETER_DESCRIPTION = (
    "Ask for a pretty printed response for human convenience"
)

FORMAT_QP = Query(None, description=_FORMAT_PARAMETER_DESCRIPTION)
PRETTY_QP = Query(None, description=_PRETTY_PARAMETER_DESCRIPTION)


def make_create_function(
    interaction: TypeInteraction[ResourceType],
) -> Callable[
    [Request, Response, str, str, ResourceType],
    Coroutine[None, None, ResourceType | Response | None],
]:
    """Make a function suitable for creation of a FHIR create API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    async def create(
        request: Request,
        response: Response,
        _format: str = FORMAT_QP,
        _pretty: str = PRETTY_QP,
        resource: ResourceType = Body(
            None,
            media_type="application/fhir+json",
            alias=resource_type_str,
        ),
    ) -> ResourceType | Response | None:
        """
        Function for create interaction.

        Calls the handler, and sets the Location header based on the Id of the created resource.
        """
        handler = cast(CreateInteractionHandler[ResourceType], interaction.handler)
        result = await handler(InteractionContext(request, response), resource)  # type: ignore
        id_, result_resource = _result_to_id_resource_tuple(result)

        response.headers[
            "Location"
        ] = f"{request.base_url}{resource_type_str}/{id_}/_history/1"

        return format_response(
            resource=result_resource,
            response=response,
            format_parameters=FormatParameters.from_request(request),
        )

    create.__annotations__ |= {
        "resource": interaction.resource_type,
    }

    return create


def make_read_function(
    interaction: TypeInteraction[ResourceType],
) -> Callable[
    [Request, Response, Id, str, str], Coroutine[None, None, ResourceType | Response]
]:
    """Make a function suitable for creation of a FHIR read API route."""

    async def read(
        request: Request,
        response: Response,
        id_: Id = Path(
            None,
            alias="id",
            description=Resource.schema()["properties"]["id"]["title"],
        ),
        _format: str = FORMAT_QP,
        _pretty: str = PRETTY_QP,
    ) -> ResourceType | Response:
        """Function for read interaction."""
        handler = cast(ReadInteractionHandler[ResourceType], interaction.handler)
        result_resource = await handler(InteractionContext(request, response), id_)  # type: ignore

        return format_response(
            resource=result_resource,
            response=response,
            format_parameters=FormatParameters.from_request(request),
        )

    return read


# TODO: If possible, map FHIR primitives to correct type annotations for better validation
def make_search_type_function(
    interaction: TypeInteraction[ResourceType],
    search_parameter_metadata: dict[str, dict[str, str]],
    post: bool,
) -> Callable[
    [Request, Response, str, str], Coroutine[None, None, Resource | Response]
]:
    """
    Make a function suitable for creation of a FHIR search-type API route.

    Creation of a search-type function is more complex than creation of a create, read, or update
    function due to the variability of search parameters, support for custom search parameters, and
    due to the need to support GET and POST.

    Search parameter descriptions are pulled from the FHIR specification.

    After the function is created, the function signature is changed to account for what search
    parameters are supported by the developer-defined handler.
    """

    if post:
        format_annotation = Form(None, description=_FORMAT_PARAMETER_DESCRIPTION)
        pretty_annotation = Form(None, description=_PRETTY_PARAMETER_DESCRIPTION)
    else:
        format_annotation = FORMAT_QP
        pretty_annotation = PRETTY_QP

    async def search_type(
        request: Request,
        response: Response,
        *,
        _format: str = format_annotation,
        _pretty: str = pretty_annotation,
        **kwargs: str,
    ) -> Resource | Response:
        """Function for search-type interaction."""
        handler = cast(SearchTypeInteractionHandler, interaction.handler)
        bundle = await handler(InteractionContext(request, response), **kwargs)  # type: ignore

        return format_response(
            resource=bundle,
            response=response,
            format_parameters=FormatParameters.from_request(request),
        )

    search_parameters: tuple[Parameter, ...] = tuple(
        _make_search_parameter(
            name=search_parameter.name,
            description=search_parameter_metadata[
                var_name_to_qp_name(search_parameter.name)
            ]["description"],
            post=post,
            multiple=search_parameter.multiple,
        )
        for search_parameter in supported_search_parameters(interaction.handler)
    )

    sig = signature(search_type)
    parameters: tuple[Parameter, ...] = tuple(sig.parameters.values())[:-1]

    sorted_search_parameters: list[Parameter] = sorted(
        parameters + search_parameters,
        key=lambda p: search_parameter_sort_key(
            p.name, search_parameter_metadata, p.annotation
        ),
    )

    sig = sig.replace(parameters=sorted_search_parameters)
    setattr(search_type, "__signature__", sig)

    return search_type


def make_update_function(
    interaction: TypeInteraction[ResourceType],
) -> Callable[
    [Request, Response, Id, str, str, ResourceType],
    Coroutine[None, None, ResourceType | Response | None],
]:
    """Make a function suitable for creation of a FHIR update API route."""

    async def update(
        request: Request,
        response: Response,
        id_: Id = Path(
            None,
            alias="id",
            description=Resource.schema()["properties"]["id"]["title"],
        ),
        _format: str = FORMAT_QP,
        _pretty: str = PRETTY_QP,
        resource: ResourceType = Body(
            None,
            media_type="application/fhir+json",
            alias=interaction.resource_type.get_resource_type(),
        ),
    ) -> ResourceType | Response | None:
        if resource.id and id_ != resource.id:
            raise FHIRBadRequestError(
                code="invalid",
                details_text="Logical Id in URL must match logical Id in resource",
            )

        handler = cast(UpdateInteractionHandler[ResourceType], interaction.handler)
        result = await handler(InteractionContext(request, response), id_, resource)  # type: ignore
        _, result_resource = _result_to_id_resource_tuple(result)

        return format_response(
            resource=result_resource,
            response=response,
            format_parameters=FormatParameters.from_request(request),
        )

    update.__annotations__ |= {
        "resource": interaction.resource_type,
    }

    return update


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


def _make_search_parameter(
    name: str, description: str, post: bool, multiple: bool
) -> Parameter:
    """
    Make a search parameter for the purpose of creating a function signature.

    Set the defaults to Form for POST endpoints, and Query for non-POST endpoints.
    """
    assert _is_valid_parameter_name(
        name
    ), f"{name} is not a valid search parameter name"

    return Parameter(
        name=name,
        kind=Parameter.KEYWORD_ONLY,
        default=Form(None, alias=var_name_to_qp_name(name), description=description)
        if post
        else Query(None, alias=var_name_to_qp_name(name), description=description),
        annotation=list[str] if multiple else str,
    )


def _is_valid_parameter_name(name: str) -> bool:
    """
    Return True or False depending on whether the parameter name is valid.

    Names that are Python keywords are forbidden, in addition to other names that have additional
    meaning in Python or this package.
    """
    return not keyword.iskeyword(name) and name not in {
        "context",
        "format",
        "resource",
        "type",
    }
