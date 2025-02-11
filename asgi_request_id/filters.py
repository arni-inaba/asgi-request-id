from logging import Filter, LogRecord
from .context import REQUEST_ID_CTX_KEY, request_id_ctx_var

class RequestIdFilter(Filter):
    """
    A logging filter that integrates the request ID context into log records.
    
    Attributes:
        context_key (str): The key to retrieve the request ID context value.
        default_value (str): The default value if the request ID context key is not found.
    """
    def __init__(self, name: str = "", context_key: str = REQUEST_ID_CTX_KEY, default_value: str = "") -> None:
        """
        Initializes the RequestIdFilter with the given parameters.
        
        Args:
            name (str): The name of the filter.
            context_key (str): The key to retrieve the request ID context value.
            default_value (str): The default value if the request ID context key is not found.
        """
        super().__init__(name)
        self.context_key: str = context_key
        self.default_value: str = default_value

    def filter(self, record: LogRecord) -> bool:
        """
        Applies the filter to the given log record.
        
        This method retrieves the request ID context value using the context key and sets it as an attribute on the log record. 
        If the context key is not found, the default_value is used.
        
        Args:
            record (LogRecord): The log record to which the filter is applied.
        
        Returns:
            bool: Always returns True to indicate the record should be logged.
        """
        try:
            context_value = request_id_ctx_var.get(self.default_value)
        except RuntimeError:
            context_value = self.default_value
        setattr(record, self.context_key, context_value)
        return True