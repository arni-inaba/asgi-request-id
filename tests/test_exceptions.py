import pytest
from asgi_request_id import InvalidHeaderNameException

def test_invalid_header_name_exception() -> None:
    with pytest.raises(InvalidHeaderNameException) as exc_info:
        raise InvalidHeaderNameException(header_name="x-request-id")
    exception = exc_info.value
    assert exception.header_name == "x-request-id"
