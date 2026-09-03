from typing import List, Optional, Union

from pydantic import BaseModel, Field, RootModel


class VeiculoItemDTO(BaseModel):
    NUM_VEIC: Union[int, str] = Field(..., description="Número do veículo")
    IDN_PLAC_VEIC: str = Field(..., description="Identificação da placa do veículo")
    VEIC_ATIV_EMPR: bool = Field(
        ..., description="Indica se o veículo está ativo na empresa"
    )
    DAT_BAIX: Optional[str] = Field(
        None, description="Data de baixa do veículo, se baixado"
    )


class VeiculoListResponseDTO(BaseModel):
    veiculos: List[VeiculoItemDTO] = Field(..., description="Lista de veículos")


class VeiculoRequestDTO(BaseModel):
    NUM_VEIC: Union[int, str] = Field(..., description="Número do veículo")
    IDN_PLAC_VEIC: str = Field(..., description="Identificação da placa do veículo")
    VEIC_ATIV_EMPR: bool = Field(
        ..., description="Indica se o veículo está ativo na empresa"
    )
    DAT_BAIX: Optional[str] = Field(None, description="Data de baixa do veículo")


class VeiculoListRequestDTO(RootModel[List[VeiculoRequestDTO]]):
    pass
