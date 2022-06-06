resource_type = None
interaction_type = None


async def dispatch(*_, **__):
    pass


async def create(request, response, resource):
    return await dispatch(
        request, response, resource_type, interaction_type, resource=resource
    )


async def read(request, response, id_):
    return await dispatch(request, response, resource_type, interaction_type, id_=id_)
