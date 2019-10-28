import pytest
from starlette.applications import Starlette

from asgi_request_id import RequestIDMiddleware


@pytest.fixture
def app():
    return Starlette()


@pytest.fixture
def middleware(app):
    return RequestIDMiddleware(app)
