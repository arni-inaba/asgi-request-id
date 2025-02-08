from collections.abc import Callable
from .exceptions import InvalidHeaderNameException
from .constants import (
    _DEFAULT_HEADER_NAME, 
    _DEFAULT_SKIP_VALIDATE_HEADER_NAME,
    _HEADER_NAME_PATTERN,
)

def validate_header_name(skip: bool =_DEFAULT_SKIP_VALIDATE_HEADER_NAME) -> Callable:
    """
    Decorator to validate the header name against a pattern.
    
    Raises:
        InvalidHeaderNameException: If the header name is invalid.
    """
    def decorator(func: Callable)-> Callable:
        def wrapper(self, *args, **kwargs) -> Callable:
            if not skip:
                incoming_request_id_header = getattr(self, 'incoming_request_id_header', _DEFAULT_HEADER_NAME)
                if not _HEADER_NAME_PATTERN.match(incoming_request_id_header):
                    raise InvalidHeaderNameException(incoming_request_id_header)
                outgoing_request_id_header = getattr(self, 'outgoing_request_id_header', _DEFAULT_HEADER_NAME)
                if not _HEADER_NAME_PATTERN.match(outgoing_request_id_header):
                    raise InvalidHeaderNameException(outgoing_request_id_header)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator