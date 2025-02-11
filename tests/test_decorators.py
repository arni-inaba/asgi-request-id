import pytest
from asgi_request_id.exceptions import InvalidHeaderNameException
from asgi_request_id.constants import _DEFAULT_HEADER_NAME
from asgi_request_id.decorators import validate_header_name

class TestClass:
    def __init__(self, incoming_request_id_header: str = _DEFAULT_HEADER_NAME, outgoing_request_id_header: str = _DEFAULT_HEADER_NAME) -> None:
        self.incoming_request_id_header = incoming_request_id_header
        self.outgoing_request_id_header = outgoing_request_id_header

    @validate_header_name()
    def test_validate_header_name(self, *args, **kwargs) -> str:
        return "OK"   

def test_validate_header_name_with_default_config() -> None:
    TC = TestClass()
    result = TC.test_validate_header_name()
    assert result == "OK"

@pytest.mark.parametrize("incoming_request_id_header", [f"valid_incoming_request_id_header_config_{i:02d}" for i in range(1, 2)])
@pytest.mark.parametrize("outgoing_request_id_header", [f"valid_outgoing_request_id_header_config_{i:02d}" for i in range(1, 2)])
def test_validate_header_name_with_valid_config(incoming_request_id_header: str, outgoing_request_id_header: str, request: pytest.FixtureRequest) -> None:
    incoming_request_id_header = request.getfixturevalue(incoming_request_id_header)
    outgoing_request_id_header = request.getfixturevalue(outgoing_request_id_header)
    TC = TestClass(incoming_request_id_header=incoming_request_id_header, outgoing_request_id_header=outgoing_request_id_header)
    result = TC.test_validate_header_name()
    assert result == "OK"

@pytest.mark.parametrize("incoming_request_id_header", [f"invalid_incoming_request_id_header_config_{i:02d}" for i in range(1, 2)])
@pytest.mark.parametrize("outgoing_request_id_header", [f"invalid_outgoing_request_id_header_config_{i:02d}" for i in range(1, 2)])
def test_validate_header_name_with_invalid_config(incoming_request_id_header: str, outgoing_request_id_header: str, request: pytest.FixtureRequest) -> None:
    incoming_request_id_header = request.getfixturevalue(incoming_request_id_header)
    outgoing_request_id_header = request.getfixturevalue(outgoing_request_id_header)
    with pytest.raises(InvalidHeaderNameException):
        TC = TestClass(incoming_request_id_header=incoming_request_id_header, outgoing_request_id_header=outgoing_request_id_header)
        TC.test_validate_header_name()