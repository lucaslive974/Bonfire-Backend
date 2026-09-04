from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_serializer


class VeiculoItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    NUM_VEIC: Union[int, str] = Field(..., description="Número do veículo")
    IDN_PLAC_VEIC: str = Field(..., description="Identificação da placa do veículo")
    VEIC_ATIV_EMPR: bool = Field(
        ..., description="Indica se o veículo está ativo na empresa"
    )
    DAT_BAIX: Optional[Union[datetime, str]] = Field(
        None, description="Data de baixa do veículo, se baixado"
    )

    @field_serializer("DAT_BAIX", when_used="json")
    def serialize_dt(self, dt: Optional[Union[datetime, str]]) -> Optional[str]:
        return dt.isoformat() if isinstance(dt, datetime) else dt


class VeiculoListResponseDTO(BaseModel):
    veiculos: List[VeiculoItemDTO] = Field(..., description="Lista de veículos")


class VeiculoRequestDTO(BaseModel):
    NUM_VEIC: Union[int, str] = Field(..., description="Número do veículo")
    IDN_PLAC_VEIC: Optional[str] = Field(
        None, description="Identificação da placa do veículo"
    )
    VEIC_ATIV_EMPR: Optional[bool] = Field(
        None, description="Indica se o veículo está ativo na empresa"
    )
    DAT_BAIX: Optional[str] = Field(None, description="Data de baixa do veículo")


class VeiculoListRequestDTO(RootModel[List[VeiculoRequestDTO]]):
    pass
