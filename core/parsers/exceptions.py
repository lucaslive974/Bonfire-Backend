from exceptions.CustomExceptions import CustomException


class DocumentParsingError(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 422,
        error: str = "Parsing Error",
        friendly_message: str = "Falha ao processar o conteúdo do documento. Verifique se o formato interno e os dados estão legíveis.",
    ):
        super().__init__(message, status, error, friendly_message)


class UnsupportedFormatError(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 415,
        error: str = "Unsupported Format",
        friendly_message: str = "Formato de arquivo não suportado pelo parser.",
    ):
        super().__init__(message, status, error, friendly_message)
