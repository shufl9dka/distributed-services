from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from modules.services import send_to_services

app = FastAPI()


@app.get('/{request_path:path}')
async def client_request(request_path: str, request: Request):
    resp = await send_to_services(request_path, request)
    if resp is None:
        return JSONResponse({
            'status': "FAILED",
            'result': "There's no available service"
        }, status_code=502)
    response = Response(content=resp['content'], status_code=resp['status'])
    return response
