resource_type = None
interaction_type = None


async def dispatch(*_, **__):
    pass


async def read(id_):
    return await dispatch(resource_type, interaction_type, id_=id_)
