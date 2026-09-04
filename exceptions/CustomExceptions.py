from typing import Any


class CustomException(Exception):
    """Base class for custom application exceptions."""

    def __init__(
        self,
        message: str,
        status: int = 500,
        error: str = "",
        friendly_message: str = "Um erro inesperado ocorreu.",
    ) -> None:
        super().__init__(message)
        self.error = error
        self.message = message  # Detailed/internal information for logging
        self.status = status
        self.friendly_message = friendly_message  # Sanitized user-facing message
        self.counter = None

    def __iter__(self):
        yield "error", self.error
        yield "message", self.friendly_message
        yield "status", self.status


class ErrDataPubli(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 400,
        error: str = "DAT_PUBL Invalida",
        friendly_message: str = "Data de publicação não encontrada ou formato inválido no arquivo.",
    ):
        super().__init__(message, status, error, friendly_message)


class ErrNullInsert(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 400,
        error: str = "autoSegundaInstanciaList NULL",
        friendly_message: str = "Nenhum dado válido extraído para inserção.",
    ):
        super().__init__(message, status, error, friendly_message)


class ErrInvalidDbConfig(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 500,
        error: str = "Invalid DB config",
        friendly_message: str = "Erro interno de configuração do banco.",
    ):
        super().__init__(message, status, error, friendly_message)


class ErrCreatingDbConnection(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 500,
        error: str = "Error creating DB Connection",
        friendly_message: str = "Não foi possível estabelecer conexão com o banco de dados.",
    ):
        super().__init__(message, status, error, friendly_message)


class ErrGetData(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 500,
        error: str = "Error fetching data",
        friendly_message: str = "Falha ao buscar os dados solicitados.",
    ):
        super().__init__(message, status, error, friendly_message)


class ErrInsertData(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 500,
        error: str = "Error inserting data",
        friendly_message: str = "Não foi possível inserir os dados. Verifique se os registros já existem ou se as informações estão corretas.",
    ):
        super().__init__(message, status, error, friendly_message)


class ErrUpdateData(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 500,
        error: str = "Error updating data",
        friendly_message: str = "Não foi possível atualizar os registros solicitados.",
    ):
        super().__init__(message, status, error, friendly_message)


class ErrIncompleteData(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 400,
        error: str = "Incomplete Data",
        friendly_message: str = "Faltam dados obrigatórios na requisição.",
    ):
        super().__init__(message, status, error, friendly_message)


class ErrLogger(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 500,
        error: str = "Error on logs",
        friendly_message: str = "Falha no subsistema de logs.",
    ):
        super().__init__(message, status, error, friendly_message)


class ErrInvalidJson(CustomException):
    def __init__(
        self,
        expectedObject: Any,
        message: str,
        status: int = 400,
        error: str = "Invalid JSON Object",
        friendly_message: str = "O payload enviado está em um formato inválido.",
    ):
        super().__init__(message, status, error, friendly_message)
        self.expectedObject = expectedObject

    def __iter__(self):
        yield from super().__iter__()
        yield "object_expected", self.expectedObject


class ErrReadingFile(CustomException):
    def __init__(
        self,
        message: str,
        status: int = 500,
        error: str = "Error in file",
        friendly_message: str = "Ocorreu um erro ao tentar ler ou processar o arquivo enviado.",
    ):
        super().__init__(message, status, error, friendly_message)


class ErrQuantityOfAtas(CustomException):
    def __init__(
        self,
        message: str,
        qtdAtas: Any,
        qtdTables: Any,
        status: int = 400,
        error: str = "Error extracting atas or tables",
        friendly_message: str = "A quantidade de Atas lidas não corresponde ao número de tabelas encontradas no documento.",
    ):
        super().__init__(message, status, error, friendly_message)
        self.qtdAtas = qtdAtas
        self.qtdTables = qtdTables

    def __iter__(self):
        yield from super().__iter__()
        yield "qtdAtas", self.qtdAtas
        yield "qtdTables", self.qtdTables


class ErrIncorrectInstance(CustomException):
    def __init__(
        self,
        message: str,
        friendly_message: str = "Instância incorreta. O arquivo contém registros de uma instância diferente da esperada.",
    ):
        super().__init__(message, 400, "Incorrect Instance", friendly_message)


class ErrMissingRequiredEnv(CustomException):
    def __init__(
        self,
        message: str,
        friendly_message: str = "Variável de ambiente obrigatória não encontrada.",
    ):
        super().__init__(message, 500, "Missing Required Env", friendly_message)


class ErrInvalidFileData(CustomException):
    def __init__(
        self,
        friendly_message: str,
        status: int = 400,
        error: str = "Invalid File Data",
    ):
        super().__init__(friendly_message, status, error, friendly_message)
