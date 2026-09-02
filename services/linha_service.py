from typing import Any, Dict, List

from repositories.interfaces import IRepositoryManager


class LinhaService:
    """Serviço de domínio para casos de uso de Linhas."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def get_linha(self) -> List[Dict[str, Any]]:
        """Recupera os dados das linhas no banco de dados."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            linhas = repo.get_all()
            return [linha.as_dict() for linha in linhas]

    def insert_linha(self, line_data: List[Dict[str, Any]]) -> int:
        """Insere uma lista de linhas no banco de dados."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            count = repo.insert_bulk(line_data)
            return count

    def update_linha(self, line_data: List[Dict[str, Any]]) -> int:
        """Realiza atualização de uma lista de linhas no banco de dados."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            count = repo.update_bulk(line_data)
            return count

    def delete_linha(self, cod_linh: str) -> int:
        """Realiza a exclusão de uma linha no banco de dados."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            count = repo.delete(cod_linh)
            return count
