from typing import Any, Dict, List

from repositories.database import get_db
from repositories.linha_repository import LinhaRepository


class LinhaService:
    """Serviço de domínio para casos de uso de Linhas."""

    @staticmethod
    def get_linha() -> List[Dict[str, Any]]:
        """Recupera os dados das linhas no banco de dados."""
        with get_db() as db:
            repo = LinhaRepository(db)
            linhas = repo.get_all()
            return [l.as_dict() for l in linhas]

    @staticmethod
    def insert_linha(line_data: List[Dict[str, Any]]) -> int:
        """Insere uma lista de linhas no banco de dados."""
        with get_db() as db:
            repo = LinhaRepository(db)
            count = repo.insert_bulk(line_data)
            return count

    @staticmethod
    def update_linha(line_data: List[Dict[str, Any]]) -> int:
        """Realiza atualização de uma lista de linhas no banco de dados."""
        with get_db() as db:
            repo = LinhaRepository(db)
            count = repo.update_bulk(line_data)
            return count

    @staticmethod
    def delete_linha(cod_linh: str) -> int:
        """Realiza a exclusão de uma linha no banco de dados."""
        with get_db() as db:
            repo = LinhaRepository(db)
            count = repo.delete(cod_linh)
            return count
