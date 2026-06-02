import json
from typing import List, Dict, Any
from repositories.database import get_db
from repositories.linha_repository import LinhaRepository

def getLinha() -> str:
    """Recupera os dados das linhas no banco de dados"""
    with get_db() as db:
        repo = LinhaRepository(db)
        linhas = repo.get_all()
        data = [l.to_dict() for l in linhas]
        return json.dumps(data)


def insertLinha(line_data: List[Dict[str, Any]]) -> int:
    """Insere uma lista de linhas no banco de dados"""
    with get_db() as db:
        repo = LinhaRepository(db)
        count = repo.insert_bulk(line_data)
        return count


def updateLinha(line_data: List[Dict[str, Any]]) -> int:
    """Realiza atualização de uma lista de linhas no banco de dados"""
    with get_db() as db:
        repo = LinhaRepository(db)
        count = repo.update_bulk(line_data)
        return count


def deleteLinha(cod_linh: str) -> int:
    """Realiza a exclusão de uma linha no banco de dados"""
    with get_db() as db:
        repo = LinhaRepository(db)
        count = repo.delete(cod_linh)
        return count
