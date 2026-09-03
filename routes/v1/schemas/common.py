from typing import Annotated, Any

from pydantic import BaseModel, Field, WithJsonSchema
from pydantic_core import PydanticCustomError
from spectree import Response
from werkzeug.datastructures import FileStorage

UploadFile = Annotated[
    Any,
    WithJsonSchema(
        {"type": "string", "format": "binary", "description": "Arquivo para upload"}
    ),
]


def validate_required_file(data: Any, error_message: str) -> Any:
    """Valida a presença obrigatória de arquivo em requisições multipart/form-data."""
    if (
        not isinstance(data, dict)
        or "file" not in data
        or not isinstance(data["file"], FileStorage)
        or not data["file"].filename
    ):
        raise PydanticCustomError("incomplete_data", error_message)
    return data


class ErrorResponseDTO(BaseModel):
    error: str = Field(..., description="Identificador do tipo de erro")
    message: str = Field(..., description="Mensagem descritiva do erro")


class MutationResponseDTO(BaseModel):
    message: str = Field(..., description="Mensagem de status da operação")
    counter: int = Field(..., description="Quantidade de registros afetados")


def create_api_response(
    success_model: Any = None,
    success_code: int = 200,
    **extra_responses: Any,
) -> Response:
    """Gera respostas padronizadas para documentação OpenAPI."""
    responses: dict[str, Any] = {
        "HTTP_400": ErrorResponseDTO,
        "HTTP_401": ErrorResponseDTO,
        "HTTP_422": ErrorResponseDTO,
        "HTTP_500": ErrorResponseDTO,
    }
    if success_model is not None:
        responses[f"HTTP_{success_code}"] = success_model
    responses.update(extra_responses)
    return Response(**responses)
