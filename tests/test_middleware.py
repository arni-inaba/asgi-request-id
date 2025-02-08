import pytest
from httpx import AsyncClient, ASGITransport
from starlette.applications import Starlette
from uuid import UUID, uuid4

async def test_middleware_info_endpoint(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/info")
        assert response.status_code == 200
        assert response.json() == {"message": "info"}
        assert UUID(response.headers.get("request-id")).version == 4

async def test_middleware_excluded_endpoint(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/excluded")
        assert response.status_code == 200
        assert response.json() == {"message": "excluded"}
        assert UUID(response.headers.get("request-id")).version == 4

async def test_middleware_excluded_endpoint_with_valid_excluded_path(app: Starlette) -> None:
    app.user_middleware[0].kwargs["excluded_paths"] = ["^/excluded/?$"]
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/excluded")
        assert response.status_code == 200
        assert response.json() == {"message": "excluded"}
        assert response.headers.get("request-id") == None

async def test_middleware_excluded_endpoint_with_invalid_excluded_path(app: Starlette) -> None:
    app.user_middleware[0].kwargs["excluded_paths"] = ["^/xxxxxxxx/?$"]
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/excluded")
        assert response.status_code == 200
        assert response.json() == {"message": "excluded"}
        assert UUID(response.headers.get("request-id")).version == 4

async def test_middleware_info_endpoint_with_valid_incoming_request_id_header(app: Starlette) -> None:
    app.user_middleware[0].kwargs["incoming_request_id_header"] = "x-my-company-request-id"
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/info", headers={"x-my-company-request-id": str(uuid4())})
        assert response.status_code == 200
        assert response.json() == {"message": "info"}
        assert UUID(response.headers.get("request-id")).version == 4

async def test_middleware_info_endpoint_with_valid_outgoing_request_id_header(app: Starlette) -> None:
    app.user_middleware[0].kwargs["outgoing_request_id_header"] = "x-my-company-request-id"
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/info")
        assert response.status_code == 200
        assert response.json() == {"message": "info"}
        assert UUID(response.headers.get("x-my-company-request-id")).version == 4

async def test_middleware_info_endpoint_with_valid_prefix(app: Starlette) -> None:
    app.user_middleware[0].kwargs["prefix"] = "x-my-company-request-id-prefix-"
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/info")
        assert response.status_code == 200
        assert response.json() == {"message": "info"}
        assert response.headers.get("request-id").startswith("x-my-company-request-id-prefix-")
        assert UUID(response.headers.get("request-id").replace("x-my-company-request-id-prefix-", "")).version == 4

async def test_middleware_info_endpoint_with_valid_uuid_generator(app: Starlette) -> None:
    app.user_middleware[0].kwargs["uuid_generator"] = lambda: uuid4().hex
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/info")
        assert response.status_code == 200
        assert response.json() == {"message": "info"}
        assert UUID(response.headers.get("request-id")).version == 4
        assert response.headers.get("request-id").count("-") == 0