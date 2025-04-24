"""
Dynamic function creation for FHIR interactions.

The callables passed to FastAPI by FHIRStarter are created using functional programming techniques.
Interactions other than search are fairly straightforward — these functions simply call a
developer-provided handler, perform some FHIR-related processing, and return the result up the
chain.

The search use case is slightly more complicated. Because each FHIR resource type has a different
set of search parameters (i.e. query parameters), the approach used for the read, update, and create
use cases to create the callables does not work. Instead, a function that takes arbitrary kwargs is
created, and the function signature is modified afterward to provide the information needed by
FastAPI for documentation purposes: variable name, annotation, and default value.

These functions can create FastAPI path operation functions for both async and non-async handlers,
though not elegantly. Unfortunately the code has to be duplicated, and maintainers will need to be
cognizant that changes made to these generated path operation functions must be applied in two
places.
"""

import keyword
from inspect import Parameter, iscoroutinefunction, signature
from typing import Callable, Coroutine, Dict, List, Tuple, Union, cast

from fastapi import Form, Path, Query, Request, Response

from .exceptions import FHIRBadRequestError
from .interactions import (
    CreateInteractionHandler,
    DeleteInteractionHandler,
    InteractionContext,
    PatchInteractionHandler,
    ReadInteractionHandler,
    ResourceType,
    SearchTypeInteractionHandler,
    TypeInteraction,
    UpdateInteractionHandler,
)
from .json_patch import JSONPatch
from .resources import Bundle, Resource
from .search_parameters import (
    parameter_sort_key,
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

ID_PP = Path(
    alias="id",
    min_length=1,
    max_length=64,
    regex="^[A-Za-z0-9\-.]+$",
    description=Resource.model_fields["id"].title,
)
FORMAT_QP = Query(None, alias="_format", description=_FORMAT_PARAMETER_DESCRIPTION)
PRETTY_QP = Query(None, alias="_pretty", description=_PRETTY_PARAMETER_DESCRIPTION)


# Note: I'm not currently aware of a better way do support both async and non-async handlers than
#       branching based on the result of the iscoroutinefunction function and duplicating most of
#       the code. If there is a better way to do this, I will refactor later.


def make_read_function(
    interaction: TypeInteraction[ResourceType],
) -> Callable[
    [Request, Response, str, str, str],
    Union[Coroutine[None, None, Union[ResourceType, Response]], ResourceType, Response],
]:
    """Make a function suitable for creation of a FHIR read API route."""

    if iscoroutinefunction(interaction.handler):

        async def read_async(
            request: Request,
            response: Response,
            id_: str = ID_PP,
            format_: str = FORMAT_QP,
            pretty_: str = PRETTY_QP,
        ) -> Union[ResourceType, Response]:
            """Function for read interaction."""
            handler = cast(ReadInteractionHandler[ResourceType], interaction.handler)
            result_resource = await handler(InteractionContext(request, response), id_)  # type: ignore[call-arg]

            return format_response(
                resource=result_resource,
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        return read_async

    else:

        def read(
            request: Request,
            response: Response,
            id_: str = ID_PP,
            format_: str = FORMAT_QP,
            pretty_: str = PRETTY_QP,
        ) -> Union[ResourceType, Response]:
            """Function for read interaction."""
            handler = cast(ReadInteractionHandler[ResourceType], interaction.handler)
            result_resource = handler(InteractionContext(request, response), id_)  # type: ignore[call-arg]

            return format_response(
                resource=result_resource,
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        return read


def make_update_function(
    interaction: TypeInteraction[ResourceType],
) -> Callable[
    [Request, Response, ResourceType, str, str, str],
    Union[Coroutine[None, None, Union[ResourceType, Response]], ResourceType, Response],
]:
    """Make a function suitable for creation of a FHIR update API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    if iscoroutinefunction(interaction.handler):

        async def update_async(
            request: Request,
            response: Response,
            resource: ResourceType,
            id_: str = ID_PP,
            format_: str = FORMAT_QP,
            pretty_: str = PRETTY_QP,
        ) -> Union[ResourceType, Response]:
            """Function for update interaction."""
            if resource and resource.id and id_ != resource.id:
                raise FHIRBadRequestError(
                    code="invalid",
                    details_text="Logical Id in URL must match logical Id in resource",
                )

            handler = cast(UpdateInteractionHandler[ResourceType], interaction.handler)
            result = await handler(InteractionContext(request, response), id_, resource)  # type: ignore[call-arg,misc]
            _, result_resource = _result_to_id_resource_tuple(result)

            response.headers["Location"] = f"/{resource_type_str}/{id_}"

            return format_response(
                resource=result_resource,
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        update_async.__annotations__.update(
            {
                "resource": interaction.resource_type,
            }
        )

        return update_async
    else:

        def update(
            request: Request,
            response: Response,
            resource: ResourceType,
            id_: str = ID_PP,
            format_: str = FORMAT_QP,
            pretty_: str = PRETTY_QP,
        ) -> Union[ResourceType, Response]:
            """Function for update interaction."""
            if resource and resource.id and id_ != resource.id:
                raise FHIRBadRequestError(
                    code="invalid",
                    details_text="Logical Id in URL must match logical Id in resource",
                )

            handler = cast(UpdateInteractionHandler[ResourceType], interaction.handler)
            result = handler(InteractionContext(request, response), id_, resource)  # type: ignore[call-arg]
            _, result_resource = _result_to_id_resource_tuple(result)

            response.headers["Location"] = f"/{resource_type_str}/{id_}"

            return format_response(
                resource=result_resource,
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        update.__annotations__.update(
            {
                "resource": interaction.resource_type,
            }
        )

        return update


def make_patch_function(
    interaction: TypeInteraction[ResourceType],
) -> Callable[
    [Request, Response, JSONPatch, str, str, str],
    Union[
        Coroutine[None, None, Union[ResourceType, Response]],
        ResourceType,
        Response,
    ],
]:
    """Make a function suitable for creation of a FHIR patch API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    if iscoroutinefunction(interaction.handler):

        async def patch_async(
            request: Request,
            response: Response,
            json_patch: JSONPatch,
            id_: str = ID_PP,
            format_: str = FORMAT_QP,
            pretty_: str = PRETTY_QP,
        ) -> Union[ResourceType, Response]:
            """Function for patch interaction."""
            handler = cast(PatchInteractionHandler[ResourceType], interaction.handler)
            result = await handler(InteractionContext(request, response), id_, json_patch)  # type: ignore[call-arg,misc]
            _, result_resource = _result_to_id_resource_tuple(result)

            response.headers["Location"] = f"/{resource_type_str}/{id_}"

            return format_response(
                resource=result_resource,
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        return patch_async
    else:

        def patch(
            request: Request,
            response: Response,
            json_patch: JSONPatch,
            id_: str = ID_PP,
            format_: str = FORMAT_QP,
            pretty_: str = PRETTY_QP,
        ) -> Union[ResourceType, Response]:
            """Function for patch interaction."""
            handler = cast(PatchInteractionHandler[ResourceType], interaction.handler)
            result = handler(InteractionContext(request, response), id_, json_patch)  # type: ignore[call-arg]
            _, result_resource = _result_to_id_resource_tuple(result)

            response.headers["Location"] = f"/{resource_type_str}/{id_}"

            return format_response(
                resource=result_resource,
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        return patch


def make_delete_function(
    interaction: TypeInteraction[ResourceType],
) -> Callable[
    [Request, Response, str, str, str],
    Union[Coroutine[None, None, None], None],
]:
    """Make a function suitable for creation of a FHIR delete API route."""
    if iscoroutinefunction(interaction.handler):

        async def delete_async(
            request: Request,
            response: Response,
            id_: str = ID_PP,
            format_: str = FORMAT_QP,
            pretty_: str = PRETTY_QP,
        ) -> None:
            """Function for delete interaction."""
            handler = cast(DeleteInteractionHandler, interaction.handler)
            await handler(InteractionContext(request, response), id_)  # type: ignore[call-arg,misc]

            return None

        return delete_async
    else:

        def delete(
            request: Request,
            response: Response,
            id_: str = ID_PP,
            format_: str = FORMAT_QP,
            pretty_: str = PRETTY_QP,
        ) -> None:
            """Function for delete interaction."""
            handler = cast(DeleteInteractionHandler, interaction.handler)
            handler(InteractionContext(request, response), id_)  # type: ignore[call-arg]

            return None

        return delete


def make_create_function(
    interaction: TypeInteraction[ResourceType],
) -> Callable[
    [Request, Response, ResourceType, str, str],
    Union[
        Coroutine[None, None, Union[ResourceType, Response]],
        ResourceType,
        Response,
    ],
]:
    """Make a function suitable for creation of a FHIR create API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    if iscoroutinefunction(interaction.handler):

        async def create_async(
            request: Request,
            response: Response,
            resource: ResourceType,
            format_: str = FORMAT_QP,
            pretty_: str = PRETTY_QP,
        ) -> Union[ResourceType, Response]:
            """
            Function for create interaction.

            Calls the handler, and sets the Location header based on the Id of the created resource.
            """
            handler = cast(CreateInteractionHandler[ResourceType], interaction.handler)
            result = await handler(InteractionContext(request, response), resource)  # type: ignore[call-arg,misc]
            id_, result_resource = _result_to_id_resource_tuple(result)

            response.headers["Location"] = f"/{resource_type_str}/{id_}"

            return format_response(
                resource=result_resource,
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        create_async.__annotations__.update(
            {
                "resource": interaction.resource_type,
            }
        )

        return create_async
    else:

        def create(
            request: Request,
            response: Response,
            resource: ResourceType,
            format_: str = FORMAT_QP,
            pretty_: str = PRETTY_QP,
        ) -> Union[ResourceType, Response]:
            """
            Function for create interaction.

            Calls the handler, and sets the Location header based on the Id of the created resource.
            """
            handler = cast(CreateInteractionHandler[ResourceType], interaction.handler)
            result = handler(InteractionContext(request, response), resource)  # type: ignore[call-arg]
            id_, result_resource = _result_to_id_resource_tuple(result)

            response.headers["Location"] = f"/{resource_type_str}/{id_}"

            return format_response(
                resource=result_resource,
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        create.__annotations__.update(
            {
                "resource": interaction.resource_type,
            }
        )

        return create


# TODO: If possible, map FHIR primitives to correct type annotations for better validation
def make_search_type_function(
    interaction: TypeInteraction[ResourceType],
    search_parameter_metadata: Dict[str, Dict[str, str]],
    post: bool,
) -> Callable[
    [Request, Response, str, str],
    Union[Coroutine[None, None, Union[Bundle, Response]], Bundle, Response],
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
        # At the time of writing, there is a bug in FastAPI causing Forms parameters to ignore the
        # value specified for alias. The suggested workaround is to use validation_alias instead.
        #
        # Discussion: https://github.com/fastapi/fastapi/discussions/10024
        # Issue: https://github.com/fastapi/fastapi/issues/10286
        format_annotation = Form(
            None, validation_alias="_format", description=_FORMAT_PARAMETER_DESCRIPTION
        )
        pretty_annotation = Form(
            None, validation_alias="_pretty", description=_PRETTY_PARAMETER_DESCRIPTION
        )
    else:
        format_annotation = FORMAT_QP
        pretty_annotation = PRETTY_QP

    search_parameters: Tuple[Parameter, ...] = tuple(
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

    if iscoroutinefunction(interaction.handler):

        async def search_type_async(
            request: Request,
            response: Response,
            *,
            format_: str = format_annotation,
            pretty_: str = pretty_annotation,
            **kwargs: str,
        ) -> Union[Bundle, Response]:
            """Function for search-type interaction."""
            handler = cast(SearchTypeInteractionHandler, interaction.handler)
            bundle = await handler(InteractionContext(request, response), **kwargs)  # type: ignore[call-arg]

            return format_response(
                resource=bundle,
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        return _set_search_type_function_signature(
            search_type_async, search_parameters, search_parameter_metadata
        )

    else:

        def search_type(
            request: Request,
            response: Response,
            *,
            format_: str = format_annotation,
            pretty_: str = pretty_annotation,
            **kwargs: str,
        ) -> Union[Bundle, Response]:
            """Function for search-type interaction."""
            handler = cast(SearchTypeInteractionHandler, interaction.handler)
            bundle = handler(InteractionContext(request, response), **kwargs)  # type: ignore[call-arg]

            return format_response(
                resource=bundle,
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        return _set_search_type_function_signature(
            search_type, search_parameters, search_parameter_metadata
        )


def _result_to_id_resource_tuple(
    result: Union[str, ResourceType],
) -> Tuple[Union[str, None], Union[ResourceType, None]]:
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

    if post:
        # At the time of writing, there is a bug in FastAPI causing Forms parameters to ignore the
        # value specified for alias. The suggested workaround is to use validation_alias instead.
        #
        # Discussion: https://github.com/fastapi/fastapi/discussions/10024
        # Issue: https://github.com/fastapi/fastapi/issues/10286
        #
        # Additionally, Pydantic v2 does not allow model fields to start with an underscore, so
        # parameters like "_lastUpdated" are problematic. For some reason, this only manifests with
        # the search-type by POST endpoint (possibly because FastAPI creates schemas for POST
        # endpoints that accept form data). Search-type by POST is forwarded to the search-type GET
        # endpoint, so the search-type by POST function will never actually handle any requests.
        # Because of this, we can just manipulate it so that the OpenAPI documentation looks
        # correct. We'll use a name mangling scheme for this: The Python parameter name gets a
        # prefix that is acceptable to Pydantic.
        return Parameter(
            name=f"form__{name}",
            kind=Parameter.KEYWORD_ONLY,
            default=Form(
                None,
                validation_alias=var_name_to_qp_name(name),
                description=description,
            ),
            annotation=List[str] if multiple else str,
        )
    else:
        return Parameter(
            name=name,
            kind=Parameter.KEYWORD_ONLY,
            default=Query(
                None, alias=var_name_to_qp_name(name), description=description
            ),
            annotation=List[str] if multiple else str,
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


def _set_search_type_function_signature(
    search_type_function: Callable[
        ..., Union[Coroutine[None, None, Union[Bundle, Response]], Bundle, Response]
    ],
    search_parameters: Tuple[Parameter, ...],
    search_parameter_metadata: Dict[str, Dict[str, str]],
) -> Callable[
    [Request, Response, str, str],
    Union[Coroutine[None, None, Union[Bundle, Response]], Bundle, Response],
]:
    """
    Set the function signature of the search-type function so that it includes the search parameters
    that the handler supports.
    """
    sig = signature(search_type_function)
    parameters: Tuple[Parameter, ...] = tuple(sig.parameters.values())[:-1]

    sorted_search_parameters: List[Parameter] = sorted(
        parameters + search_parameters,
        key=lambda p: parameter_sort_key(
            var_name_to_qp_name(p.name), search_parameter_metadata, p.annotation
        ),
    )

    sig = sig.replace(parameters=sorted_search_parameters)
    setattr(search_type_function, "__signature__", sig)

    return search_type_function
