import json
from typing import List, Dict, Any
from repositories.database import get_db
from repositories.linha_repository import LinhaRepository
from exceptions.CustomExceptions import ErrGetData, ErrInsertData, ErrUpdateData
from handlers.log import logger

def getLinha() -> str:
    """Recupera os dados das linhas no banco de dados"""
    try:
        with get_db() as db:
            repo = LinhaRepository(db)
            linhas = repo.get_all()
            data = [l.to_dict() for l in linhas]
            return json.dumps(data)
    except Exception as e:
        logger.systemLog(e)
        raise ErrGetData('Erro ao recuperar as linhas', 500)


def insertLinha(line_data: List[Dict[str, Any]]) -> int:
    """Insere uma lista de linhas no banco de dados"""
    try:
        with get_db() as db:
            repo = LinhaRepository(db)
            count = repo.insert_bulk(line_data)
            return count
    except Exception as e:
        logger.systemLog(e)
        raise ErrInsertData('Erro ao gravar as linhas', 500)


def updateLinha(line_data: List[Dict[str, Any]]) -> int:
    """Realiza atualização de uma lista de linhas no banco de dados"""
    try:
        with get_db() as db:
            repo = LinhaRepository(db)
            count = repo.update_bulk(line_data)
            return count
    except Exception as e:
        logger.systemLog(e)
        raise ErrUpdateData("Erro ao atualizar a linha", 500)


def deleteLinha(cod_linh: str) -> int:
    """Realiza a exclusão de uma linha no banco de dados"""
    try:
        with get_db() as db:
            repo = LinhaRepository(db)
            count = repo.delete(cod_linh)
            return count
    except Exception as e:
        logger.systemLog(e)
        raise ErrUpdateData("Erro ao excluir a linha", 500)
