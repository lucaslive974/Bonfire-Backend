from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from routes.v1.schemas.common import UploadFile, validate_required_file


class InfracaoCsvUploadDTO(BaseModel):
    file: UploadFile

    @model_validator(mode="before")
    @classmethod
    def check_file(cls, data: Any):
        return validate_required_file(
            data, "Arquivo CSV de infrações não está presente na requisição"
        )


class InfracaoXlsUploadDTO(BaseModel):
    file: UploadFile

    @model_validator(mode="before")
    @classmethod
    def check_file(cls, data: Any):
        return validate_required_file(
            data, "Arquivo XLS de infrações não está presente na requisição"
        )


class InfracaoCheckUploadDTO(BaseModel):
    file: UploadFile

    @model_validator(mode="before")
    @classmethod
    def check_file(cls, data: Any):
        return validate_required_file(
            data, "Arquivo CSV de infrações não está presente na requisição"
        )


class InfracaoQueryDTO(BaseModel):
    date: Optional[str] = Field(None, description="Data de ocorrência da infração")
    ai: Optional[str] = Field(None, description="Número do Auto de Infração")


class InfracaoXlsQueryDTO(BaseModel):
    insert_ignore: Optional[bool] = Field(
        True, description="Ignorar infrações duplicadas durante a inserção"
    )


class InfracaoListResponseDTO(BaseModel):
    autos: List[Dict[str, Any]] = Field(..., description="Lista de autos de infração")


class InfracaoMessageResponseDTO(BaseModel):
    message: str = Field(
        ..., description="Mensagem descritiva do resultado da operação"
    )


class InfracaoCheckResponseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    db_rows: str = Field(..., description="Registros encontrados no banco de dados")
    file_rows: str = Field(..., description="Linhas presentes no arquivo analisado")
    Not_Present: str = Field(
        ..., alias="Not Present", description="Linhas ausentes ou não encontradas"
    )
