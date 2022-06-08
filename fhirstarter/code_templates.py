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

    response.headers["Location"] = (
        f"{request.base_url}{resource_type_str}" f"/{result.id_}/_history/1"
    )

    return result.resource


async def read(request: Request, response: Response, id_: Id) -> FHIRResourceType:
    result = cast(FHIRInteractionResult[FHIRResourceType], await callable_(id_))

    assert result.resource is not None, "FHIR read interaction cannot return None"

    return result.resource
