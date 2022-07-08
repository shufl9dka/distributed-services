from fastapi import Request
import aiohttp
import pathlib

URLS_PATH = pathlib.Path(__file__).parent.parent.joinpath('services_list.txt')
CURRENT_WORKING = {}
BAD_STATUSES = set([503, 504, 509, 522, 525, 526])


def read_urls(path=URLS_PATH):
    CURRENT_WORKING.clear()
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('http://') or line.startswith('https://'):
                CURRENT_WORKING[line] = 0


async def send_to_services(request_path, forwarded: Request) -> dict | None:
    urls = sorted(CURRENT_WORKING.items(), key=lambda item: item[1])
    async with aiohttp.ClientSession() as session:
        for service_url, _ in urls:
            CURRENT_WORKING[service_url] += 1
            async with session.request(forwarded.method, f"{service_url.rstrip('/')}/{request_path}", params=dict(forwarded.query_params),
                                       headers=dict(forwarded.headers), data=dict(await forwarded.form())) as resp:
                if resp.status in BAD_STATUSES:
                    CURRENT_WORKING[service_url] -= 1
                    continue
                return {
                    'content': await resp.content.read(),
                    'status': resp.status
                }
        return None


read_urls()
