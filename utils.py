async def async_callback(x, f):
    return f(await x)
