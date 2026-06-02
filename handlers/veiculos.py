import json
from typing import List, Dict, Any
from repositories.database import get_db
from repositories.veiculo_repository import VeiculoRepository
from exceptions.CustomExceptions import ErrGetData, ErrInsertData, ErrUpdateData
from handlers.log import logger

def getVeiculos() -> str:
    """Recupera os veiculos do banco de dados e retorna em formato JSON string."""
    try:
        with get_db() as db:
            repo = VeiculoRepository(db)
            veiculos = repo.get_all()
            # Convert list of models to list of dicts, then serialize to json
            data = [v.to_dict() for v in veiculos]
            return json.dumps(data)
    except Exception as e:
        logger.systemLog(e)
        raise ErrGetData("Erro ao recuperar os veiculos", 500)


def insertVeiculos(veiculos_data: List[Dict[str, Any]]) -> int:
    """Insere uma lista de veículos no banco de dados"""
    try:
        with get_db() as db:
            repo = VeiculoRepository(db)
            count = repo.insert_bulk(veiculos_data)
            return count
    except Exception as e:
        logger.systemLog(e)
        raise ErrInsertData("Erro ao inserir veiculos", 500)


def updateVeiculos(veiculos_data: List[Dict[str, Any]]) -> int:
    """Atualiza uma lista de veículos no banco de dados"""
    try:
        with get_db() as db:
            repo = VeiculoRepository(db)
            count = repo.update_bulk(veiculos_data)
            return count
    except Exception as e:
        logger.systemLog(e)
        raise ErrUpdateData("Erro ao atualizar os veiculos", 500)


def deleteVeiculos(num_veic: str) -> int:
    """Deleta um veiculo no banco de dados pelo seu número"""
    try:
        # Convert num_veic to integer if possible, as it is INT in veiculos table
        try:
            num_veic_int = int(num_veic)
        except ValueError:
            raise ErrUpdateData("Número do veículo inválido", 400)

        with get_db() as db:
            repo = VeiculoRepository(db)
            count = repo.delete(num_veic_int)
            return count
    except Exception as e:
        logger.systemLog(e)
        if isinstance(e, ErrUpdateData):
            raise e
        raise ErrUpdateData("Erro ao deletar os veiculos", 500)
