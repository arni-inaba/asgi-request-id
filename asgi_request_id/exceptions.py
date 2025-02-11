class InvalidHeaderNameException(Exception):
    """
    Exception raised for invalid header names.
    This class represents an error that occurs when an invalid header name is provided.
    It provides a custom description to inform the user about the invalid header name.
    """
    description: str = (
        "Invalid header name provided. "
        "Please ensure that the header name is correct and try again."
    )

    def __init__(self, header_name: str, detail: str = description) -> None:
        self.header_name: str = header_name
        super().__init__(detail)

    def __str__(self) -> str:
        return f'{self.header_name} - {self.args}'