[![PyPI - Downloads](https://img.shields.io/pypi/dm/asgi-request-id.svg)](https://pypi.org/project/asgi-request-id/)
[![PyPI - License](https://img.shields.io/pypi/l/asgi-request-id)](https://pypi.org/project/asgi-request-id/)
[![PyPI - Version](https://img.shields.io/pypi/v/asgi-request-id.svg)](https://pypi.org/project/asgi-request-id/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asgi-request-id)](https://pypi.org/project/asgi-request-id/)
[![PyPI - Status](https://img.shields.io/pypi/status/asgi-request-id)](https://pypi.org/project/asgi-request-id/)
[![Dependencies](https://img.shields.io/librariesio/release/pypi/asgi-request-id)](https://libraries.io/pypi/asgi-request-id/)
[![Last Commit](https://img.shields.io/github/last-commit/arni-inaba/asgi-request-id)](https://github.com/arni-inaba/asgi-request-id/commits/main)

# asgi-request-id 🌟

`asgi-request-id` is a middleware for ASGI applications that provides a unique request identifier for each incoming request. This identifier can be used for logging, tracing, and debugging purposes, making it easier to track requests as they flow through your application. The middleware is highly configurable, allowing you to customize the request ID generation, specify headers for incoming and outgoing request IDs, and exclude certain paths from request ID handling. It is compatible with popular ASGI frameworks like Starlette and FastAPI, and can be easily integrated into your existing application with minimal changes.

## Table of Contents 📚

- [Installation 📦](#installation)
- [Usage 🚀](#usage)
- [Middleware 🛠️](#middleware)
  - [Example 🔍](#example)
- [Logging 📝](#logging)

## Installation 📦

```
pip install asgi-request-id
```

## Usage 🚀

The `asgi-request-id` middleware performs the following actions:

- Searches for an incoming request identifier using the `incoming_request_id_header` attribute and uses it as the request ID if found.
- Generates a unique request ID with an optional prefix if no incoming request identifier is found.
- Stores the request ID in a context variable, making it accessible to the logging context through a filter.
- Includes the request ID in the response headers. If the `outgoing_request_id_header` attribute is set, its value will be used as the response header name. Ensure that the chosen header name complies with HTTP header naming conventions.

For Python 3.6 compatibility, install the backported [contextvars](https://github.com/MagicStack/contextvars) package.

## Middleware 🛠️

The `RequestIdMiddleware` class is used to handle the request ID header. It has the following attributes:

- `app`: The ASGI application.
- `excluded_paths`: List of paths to exclude from middleware processing.
- `incoming_request_id_header`: Optional incoming request ID header.
- `outgoing_request_id_header`: Optional outgoing request ID header.
- `prefix`: Optional prefix to add to the request ID.
- `skip_validate_header_name`: Optional flag to skip header name validation.
- `uuid_generator`: Optional UUID generator.

### Example 🔍

Here is a minimal example demonstrating how to use the `asgi-request-id` middleware. Additional examples with more detailed use cases and configurations can be found in the `examples` folder of the repository.

```python
import os
import uvicorn
from asgi_request_id import RequestIdMiddleware
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
```

## Logging 📝

To integrate the request ID into your logging, you can use the `RequestIdFilter` class. Here is an example `logging.yaml` configuration:

```yaml
---
version: 1
filters:
  request_id:
    (): 'asgi_request_id.RequestIdFilter'
    default_value: '-'
formatters:
  default:
    (): 'uvicorn.logging.DefaultFormatter'
    fmt: '%(levelprefix)s [%(asctime)s] %(message)s'
  access:
    (): 'uvicorn.logging.AccessFormatter'
    fmt: '%(levelprefix)s [%(asctime)s] {%(request_id)s} %(client_addr)s - "%(request_line)s" %(status_code)s'
handlers:
  default:
    class: logging.StreamHandler
    formatter: default
    stream: ext://sys.stderr
  access:
    class: logging.StreamHandler
    filters: [request_id]
    formatter: access
    stream: ext://sys.stdout
loggers:
  uvicorn:
    level: INFO
    handlers:
    - default
  uvicorn.error:
    level: INFO
  uvicorn.access:
    level: INFO
    propagate: False
    handlers:
    - access
```