import re
from uuid import uuid4

_DEFAULT_EXCLUDED_PATHS: list = []
_DEFAULT_HEADER_NAME: str = "request-id"
_DEFAULT_SKIP_VALIDATE_HEADER_NAME: bool = False
_DEFAULT_UUID_GENERATOR: callable = lambda: uuid4()
_DETAULT_PREFIX: str = ""
_HEADER_NAME_PATTERN: re.Pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9-_]*$")