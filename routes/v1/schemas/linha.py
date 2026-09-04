from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_serializer


class LinhaItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    COD_LINH: str = Field(..., description="Código identificador da linha")
    ID_OPERADORA: Optional[Union[int, str]] = Field(
        None, description="Identificador da operadora associada"
    )
    COMPARTILHADA: Optional[bool] = Field(
        False, description="Indica se a linha é compartilhada"
    )
    LINH_ATIV_EMPR: Optional[bool] = Field(
        True, description="Indica se a linha está ativa na empresa"
    )
    DAT_BAIX: Optional[Union[datetime, str]] = Field(
        None, description="Data de baixa da linha"
    )

    @field_serializer("DAT_BAIX", when_used="json")
    def serialize_dt(self, dt: Optional[Union[datetime, str]]) -> Optional[str]:
        return dt.isoformat() if isinstance(dt, datetime) else dt


class LinhaListResponseDTO(BaseModel):
    linha: List[LinhaItemDTO] = Field(..., description="Lista de linhas")


class LinhaRequestDTO(BaseModel):
    COD_LINH: str = Field(..., description="Código identificador da linha")
    ID_OPERADORA: Optional[Union[int, str]] = Field(
        None, description="Identificador da operadora associada"
    )
    COMPARTILHADA: Optional[bool] = Field(
        None, description="Indica se a linha é compartilhada"
    )
    LINH_ATIV_EMPR: Optional[bool] = Field(
        None, description="Indica se a linha está ativa na empresa"
    )
    DAT_BAIX: Optional[str] = Field(None, description="Data de baixa da linha")


class LinhaListRequestDTO(RootModel[List[LinhaRequestDTO]]):
    pass
