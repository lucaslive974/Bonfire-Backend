from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, RootModel


class LinhaItemDTO(BaseModel):
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
    DAT_BAIX: Optional[str] = Field(None, description="Data de baixa da linha")


class LinhaListResponseDTO(BaseModel):
    linha: List[Dict[str, Any]] = Field(..., description="Lista de linhas")


class LinhaRequestDTO(BaseModel):
    COD_LINH: str = Field(..., description="Código identificador da linha")
    ID_OPERADORA: Union[int, str] = Field(
        ..., description="Identificador da operadora associada"
    )
    COMPARTILHADA: bool = Field(..., description="Indica se a linha é compartilhada")
    LINH_ATIV_EMPR: bool = Field(
        ..., description="Indica se a linha está ativa na empresa"
    )
    DAT_BAIX: Optional[str] = Field(None, description="Data de baixa da linha")


class LinhaListRequestDTO(RootModel[List[LinhaRequestDTO]]):
    pass
