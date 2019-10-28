
def test_get_headers(middleware):
    scope = {
        "headers": [
            (b'host', b'localhost:8000'),
            (b'user-agent', b'curl/7.64.1'),
            (b'accept', b'*/*'),
            (b'request-id', b'abc123')
        ]
    }
    headers = middleware.get_headers(scope)
    assert len(headers) == 4
    assert headers["request-id"] == "abc123"

