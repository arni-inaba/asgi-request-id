import logging
import re
from collections.abc import Awaitable, Callable, MutableMapping
from dataclasses import dataclass, field
from typing import Any
from .context import request_id_ctx_var
from .decorators import validate_header_name
from .constants import (
    _DEFAULT_EXCLUDED_PATHS,
    _DEFAULT_HEADER_NAME,
    _DEFAULT_UUID_GENERATOR,
    _DEFAULT_PREFIX,
    _DEFAULT_SKIP_VALIDATE_HEADER_NAME,
)

log = logging.getLogger(__name__)

Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]


def _get_header(headers: list[tuple[bytes, bytes]], name: str) -> str | None:
    name_bytes = name.lower().encode("latin-1")
    for key, value in headers:
        if key.lower() == name_bytes:
            return value.decode("latin-1")
    return None


def _append_header(headers: list[tuple[bytes, bytes]], name: str, value: str) -> None:
    headers.append((name.lower().encode("latin-1"), value.encode("latin-1")))


@dataclass
class RequestIdMiddleware:
    """
    Middleware to handle the request ID header.

    Args:
        app (ASGIApp): The ASGI application
        excluded_paths (list[str | None]): List of paths to exclude from middleware processing.
        excluded_paths_patterns (list[re.Pattern]): Compiled regex patterns for paths to exclude from middleware processing.
        incoming_request_id_header (string): Optional incoming request ID header
        outgoing_request_id_header (string): Optional outgoing request ID header
        prefix (string): Optional prefix to add to the request ID
        skip_validate_header_name (bool): Optional flag to skip header name validation
        uuid_generator (callable): Optional UUID generator
    """
    app: ASGIApp
    excluded_paths_patterns: list[re.Pattern] = field(init=False)
    excluded_paths: list[str | None] = field(init=True, default_factory=lambda: _DEFAULT_EXCLUDED_PATHS)
    incoming_request_id_header: str = field(init=True, default=_DEFAULT_HEADER_NAME)
    outgoing_request_id_header: str = field(init=True, default=_DEFAULT_HEADER_NAME)
    prefix: str = field(init=True, default=_DEFAULT_PREFIX)
    skip_validate_header_name: bool = field(init=True, default=_DEFAULT_SKIP_VALIDATE_HEADER_NAME)
    uuid_generator: callable = field(init=True, default=_DEFAULT_UUID_GENERATOR)

    @validate_header_name(skip=skip_validate_header_name)
    def __post_init__(self) -> None:
        """
        Post-initialization to compile excluded path patterns and validate attributes.
        """
        self.excluded_paths_patterns = [re.compile(e) for e in self.excluded_paths]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        ASGI callable to handle the request ID header.
        
        Args:
            scope (Scope): The ASGI scope.
            receive (Receive): The ASGI receive callable.
            send (Send): The ASGI send callable.
        """
        if scope["type"] not in ("http",):
            await self.app(scope, receive, send)
            return
        
        if self._search_patterns_in_string(scope["path"], self.excluded_paths_patterns):
            await self.app(scope, receive, send)
            return

        request_id = _get_header(scope["headers"], self.incoming_request_id_header)
        if not request_id:
            request_id = self.prefix + str(self.uuid_generator())
        request_id_ctx_var.set(request_id)

        async def wrapped_send(message: Message) -> None:
            """
            Wrapper for the send callable to add the request ID header.
            
            Args:
                message (Message): The ASGI message.
            """
            if message["type"] == "http.response.start":
                _append_header(message["headers"], self.outgoing_request_id_header, request_id_ctx_var.get())
            await send(message)
        
        await self.app(scope, receive, wrapped_send)

    @staticmethod
    def _search_patterns_in_string(s: str, patterns: list[re.Pattern]) -> bool:
        """
        Search for any pattern in the string.
        
        Args:
            s (str): The string to search.
            patterns (list[re.Pattern]): The list of compiled regex patterns.
        
        Returns:
            bool: True if any pattern matches the string. False otherwise.
        """
        return any(p.search(s) for p in patterns)
