import pytest
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

@pytest.fixture
def app() -> Starlette:
    routes = [
        Route("/info", info_endpoint, methods=["GET"]),
        Route("/excluded", excluded_endpoint, methods=["GET"]),
    ]
    app = Starlette(routes=routes)
    app.add_middleware(
        RequestIdMiddleware
    )
    return app

@pytest.fixture
def valid_incoming_request_id_header_config_01() -> str:
    return "x-request-id"

@pytest.fixture
def invalid_incoming_request_id_header_config_01() -> str:
    return "#-request-id"

@pytest.fixture
def valid_outgoing_request_id_header_config_01() -> str:
    return "x-request-id"

@pytest.fixture
def invalid_outgoing_request_id_header_config_01() -> str:
    return "!-request-id"