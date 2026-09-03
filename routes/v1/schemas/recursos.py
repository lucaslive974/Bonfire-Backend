from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator

from routes.v1.schemas.common import UploadFile, validate_required_file


class RecursoPrimeiraInstanciaUploadDTO(BaseModel):
    file: UploadFile

    @model_validator(mode="before")
    @classmethod
    def check_file(cls, data: Any):
        return validate_required_file(
            data,
            "Arquivo de resultado de primeira instancia não está presente na requisição",
        )


class RecursoSegundaInstanciaUploadDTO(BaseModel):
    file: UploadFile

    @model_validator(mode="before")
    @classmethod
    def check_file(cls, data: Any):
        return validate_required_file(
            data,
            "Arquivo de resultado de segunda instancia não está presente na requisição",
        )


class RecursoPrimeiraInstanciaQueryDTO(BaseModel):
    date: Optional[str] = Field(None, description="Data de publicação do recurso")
    ata: Optional[str] = Field(None, description="Número da ata da sessão")


class RecursoSegundaInstanciaQueryDTO(BaseModel):
    date: Optional[str] = Field(None, description="Data de publicação do recurso")


class RecursoListResponseDTO(BaseModel):
    recurses: List[Dict[str, Any]] = Field(
        ..., description="Lista de recursos encontrados"
    )
