resource_type = None
interaction_type = None


async def dispatch(*_, **__):
    pass


async def create(resource):
    return await dispatch(resource_type, interaction_type, resource=resource)


async def read(id_):
    return await dispatch(resource_type, interaction_type, id_=id_)
