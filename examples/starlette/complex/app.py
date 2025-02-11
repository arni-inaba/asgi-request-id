import os
import uvicorn
from asgi_request_id import RequestIdMiddleware
from collections.abc import Callable
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from uuid import uuid4


async def info_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "info"})

async def excluded_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "excluded"})

routes = [
    Route("/info", info_endpoint, methods=["GET"]),
    Route("/excluded", excluded_endpoint, methods=["GET"]),
]

app = Starlette(routes=routes)
app.add_middleware(
    RequestIdMiddleware,
    excluded_paths=["/excluded"],
    incoming_request_id_header="x-request-id",
    outgoing_request_id_header="x-request-id",
    prefix="my-special-prefix-",
    uuid_generator=lambda: uuid4().hex,
)

if __name__ == "__main__":
    log_config = f"{os.path.dirname(__file__)}{os.sep}conf{os.sep}logging.yaml"
    config = uvicorn.Config("app:app", host="127.0.0.1", port=8000, log_config=log_config)
    server = uvicorn.Server(config)
    server.run()