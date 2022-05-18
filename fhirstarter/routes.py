resource_type = None


async def dispatch(*_, **__):
    pass


async def read(id_):
    return await dispatch(resource_type, "read", id_=id_)
