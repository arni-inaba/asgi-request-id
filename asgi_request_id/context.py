from contextvars import ContextVar

REQUEST_ID_CTX_KEY: str = "request_id"
request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY)
