asgi-request-id
===============

[![PyPI Downloads](https://img.shields.io/pypi/dm/asgi-request-id.svg)](https://pypi.org/project/asgi-request-id/)
[![PyPI Version](https://img.shields.io/pypi/v/asgi-request-id.svg)](https://pypi.org/project/asgi-request-id/)
[![License](https://img.shields.io/badge/license-mit-blue.svg)](https://pypi.org/project/asgi-request-id)

This was developed at [GRID](https://github.com/GRID-is) for use with our
python backend services and intended to make it easier to log/generate 
request IDs.

installation
------------
```
pip install asgi-request-id
```

usage
-----
```python
import logging
import uvicorn

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse

from asgi_request_id import RequestIDMiddleware, get_request_id

logger = logging.getLogger(__name__)
app = Starlette()


@app.route("/")
def homepage(request):
    logger.info(f"Request ID: {get_request_id()}")
    return PlainTextResponse("hello world")


app.add_middleware(
    RequestIDMiddleware,
    incoming_request_id_header="x-amzn-trace-id",
    outgoing_request_id_header="x-amzn-trace-id",
    prefix="myapp-",
)

if __name__ == "__main__":
    uvicorn.run(app)
```
The package will do the following:

Search for an incoming request identifier and use it as the request id if found.
If it is not found, an unique request id with an optional prefix is generated.

The request id is stored in a context variable and made available via 
`get_request_id`

Finally, the request ID is included in the response headers. If the 
`outgoing_request_id_header` variable is set, its value will be used as the 
response header name. Ensure that the chosen header name complies with HTTP 
header naming conventions.

If you want to use it with python 3.6, you need to install the backported
 [contextvars](https://github.com/MagicStack/contextvars) package.