from exceptions.CustomExceptions import CustomException

class DocumentParsingError(CustomException):
    def __init__(self, message: str, status: int = 422, error: str = "Parsing Error"):
        super().__init__(message, status, error)

class UnsupportedFormatError(CustomException):
    def __init__(self, message: str, status: int = 415, error: str = "Unsupported Format"):
        super().__init__(message, status, error)
