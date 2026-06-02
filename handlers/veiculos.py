import json
from typing import List, Dict, Any
from repositories.database import get_db
from repositories.veiculo_repository import VeiculoRepository
from exceptions.CustomExceptions import ErrUpdateData

def getVeiculos() -> str:
    """Recupera os veiculos do banco de dados e retorna em formato JSON string."""
    with get_db() as db:
        repo = VeiculoRepository(db)
        veiculos = repo.get_all()
        data = [v.to_dict() for v in veiculos]
        return json.dumps(data)


def insertVeiculos(veiculos_data: List[Dict[str, Any]]) -> int:
    """Insere uma lista de veículos no banco de dados"""
    with get_db() as db:
        repo = VeiculoRepository(db)
        count = repo.insert_bulk(veiculos_data)
        return count


def updateVeiculos(veiculos_data: List[Dict[str, Any]]) -> int:
    """Atualiza uma lista de veículos no banco de dados"""
    with get_db() as db:
        repo = VeiculoRepository(db)
        count = repo.update_bulk(veiculos_data)
        return count


def deleteVeiculos(num_veic: str) -> int:
    """Deleta um veiculo no banco de dados pelo seu número"""
    try:
        num_veic_int = int(num_veic)
    except ValueError:
        raise ErrUpdateData("Número do veículo inválido", 400)

    with get_db() as db:
        repo = VeiculoRepository(db)
        count = repo.delete(num_veic_int)
        return count
