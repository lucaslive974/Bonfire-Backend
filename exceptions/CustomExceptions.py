from typing import Dict, Any

class CustomException(Exception):
    """Classe básica para as exceções customizadas da aplicação"""
    def __init__(self,  message: str, status: int = 500, error:  str = '') -> None:
        super().__init__(message)
        self.error = error
        self.message = message
        self.status = status
        self.counter = None
    
    def to_json(self) -> Dict[str, Any]:
        return {
            "error": self.error,
            "message": self.message,
            "status": self.status,
        }

class ErrDataPubli(CustomException):
    def __init__(self, message: str, status: int, error: str = "DAT_PUBL Invalida"):
        super().__init__(message, status, error)

class ErrNullInsert(CustomException):
    def __init__(self, message: str, status: int, error: str = "autoSegundaInstanciaList NULL"):
        super().__init__(message, status, error)
    
class ErrInvalidDbConfig(CustomException):
    def __init__(self, message: str, status: int, error: str = "Invalid DB config"):
        super().__init__(message, status, error)
    
class ErrCreatingDbConnection(CustomException):
    def __init__(self, message: str, status: int, error: str = "Error creating DB Connection"):
        super().__init__(message, status, error)

class ErrGetData(CustomException):
    def __init__(self, message: str, status: int, error: str = "Error fetching data"):
        super().__init__(message, status, error)
    
class ErrInsertData(CustomException):
    def __init__(self, message: str, status: int, error: str = "Error inserting data"):
        super().__init__(message, status, error)
        
class ErrUpdateData(CustomException):
    def __init__(self, message: str, status: int, error: str = "Error updating data"):
        super().__init__(message, status, error)

class ErrIncompleteData(CustomException):
    def __init__(self,  message: str, status: int, error: str = "Incomplete Data"):
        super().__init__(message, status, error)
    
class ErrLogger(CustomException):
    def __init__(self, message: str, status: int, error: str = "Error on logs"):
        super().__init__(message, status, error)       
        
class ErrInvalidJson(CustomException):
    def __init__(self, expectedObject: Any, message: str, status: int, error: str = "Invalid JSON Object"):
        super().__init__(message, status, error)
        self.expectedObject = expectedObject

    def to_json(self) -> Dict[str, Any]:
        return {
            "error": self.error,
            "message": self.message,
            "object_expected": self.expectedObject,
        }

class ErrReadingFile(CustomException):
    def __init__(self, message: str, status: int = 500, error: str = "Error in file"):
        super().__init__(message, status, error)


class ErrQuantityOfAtas(CustomException):
    def __init__(self, message: str, qtdAtas: Any, qtdTables: Any, status: int = 400, error: str = "Error extracting atas or tables"):
        super().__init__(message, status, error)
        self.qtdAtas = qtdAtas
        self.qtdTables = qtdTables

    def to_json(self) -> Dict[str, Any]:
        return {
            "error": self.error,
            "message": self.message,
            "qtdAtas": self.qtdAtas,
            "qtdTables": self.qtdTables,
        }

class ErrIncorrectInstance(CustomException):
    def __init__(self, message: str):
        super().__init__(message, 400)

class ErrMissingRequiredEnv(CustomException):
    def __init__(self, message: str):
        super().__init__(message, 500)
