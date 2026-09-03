from typing import List, Union

from pydantic import BaseModel, Field, RootModel


class ConsorcioItemDTO(BaseModel):
    ID: Union[int, str] = Field(
        ..., description="Identificador do consórcio / operadora"
    )
    NOME: str = Field(..., description="Nome da operadora")
    CONCESSIONARIA: str = Field(..., description="Nome da concessionária")


class ConsorcioListResponseDTO(BaseModel):
    consorcios: List[ConsorcioItemDTO] = Field(
        ..., description="Lista de consórcios cadastrados"
    )


class ConsorcioRequestDTO(BaseModel):
    ID: Union[int, str] = Field(
        ..., description="Identificador do consórcio / operadora"
    )
    NOME: str = Field(..., description="Nome da operadora")
    CONCESSIONARIA: str = Field(..., description="Nome da concessionária")


class ConsorcioListRequestDTO(RootModel[List[ConsorcioRequestDTO]]):
    pass
