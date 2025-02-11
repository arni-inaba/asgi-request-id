from asgi_request_id import RequestIdMiddleware
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from uvicorn import run

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
    prefix="",
)

if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)