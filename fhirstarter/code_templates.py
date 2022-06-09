from typing import Any, cast

from fastapi import Request, Response
from fhir.resources.fhirtypes import Id

from .provider import FHIRInteractionResult, FHIRResourceType

resource_type_str: str | None = None


async def callable_(*_: Any, **__: Any) -> Any:
    return None


async def create(
    request: Request, response: Response, resource: FHIRResourceType
) -> FHIRResourceType | None:
    result = cast(FHIRInteractionResult[FHIRResourceType], await callable_(resource))
    result.validate()

    id_ = resource_id(result)

    response.headers["Location"] = (
        f"{request.base_url}{resource_type_str}" f"/{id_}/_history/1"
    )

    return result.resource


async def update(
    request: Request, response: Response, id_: Id, resource: FHIRResourceType
) -> FHIRResourceType | None:
    result = cast(
        FHIRInteractionResult[FHIRResourceType], await callable_(id_, resource)
    )
    result.validate()

    return result.resource


async def read(request: Request, response: Response, id_: Id) -> FHIRResourceType:
    result = cast(FHIRInteractionResult[FHIRResourceType], await callable_(id_))
    result.validate()

    assert result.resource is not None, "FHIR read interaction must return a resource"

    return result.resource


def resource_id(result: FHIRInteractionResult[FHIRResourceType]) -> Id | None:
    if result.id_ is not None:
        return result.id_

    if result.resource is not None:
        return result.resource.id

    return None
