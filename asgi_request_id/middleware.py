from contextvars import ContextVar
from uuid import uuid4

REQUEST_ID_CTX_KEY = "request-id"
_request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_request_id() -> str:
    return _request_id_ctx_var.get()


class RequestIDMiddleware:
    """ Request ID middleware for ASGI applications
    Args:
      app (ASGI application): ASGI application
      incoming_request_id_header (string): Optional incoming request ID header
      prefix (string): Optional prefix for self generated request IDs
    """

    def __init__(self, app, incoming_request_id_header=None, prefix=None):
        if incoming_request_id_header is None:
            incoming_request_id_header = "request-id"
        if prefix is None:
            prefix = ""
        self.app = app
        self.incoming_id_header = incoming_request_id_header.lower()
        self.prefix = prefix

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = self.get_headers(scope)
            request_id = headers.get(self.incoming_id_header)
            if not request_id:
                request_id = self.prefix + str(uuid4())
            _request_id_ctx_var.set(request_id)

        def send_wrapper(response):
            response_headers = response.get("headers")
            if response_headers:
                response["headers"].append((b"request-id", request_id.encode()))
            return send(response)

        await self.app(scope, receive, send_wrapper)

    def get_headers(self, scope):
        headers = {}
        for raw_key, raw_value in scope["headers"]:
            key = raw_key.decode("latin-1").lower()
            value = raw_value.decode("latin-1")
            if key in headers:
                headers[key] = headers[key] + ", " + value
            else:
                headers[key] = value
        return headers
