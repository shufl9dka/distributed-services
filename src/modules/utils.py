import aiohttp


async def async_request(session: aiohttp.ClientSession, method: str, url: str, request_str: str, **kwargs) -> aiohttp.ClientResponse:
    async with session.request(method, f"{url.rstrip('/')}/{request_str}", **kwargs) as resp:
        return resp
