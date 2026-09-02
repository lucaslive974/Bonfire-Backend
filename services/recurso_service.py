from typing import Any, Dict, List

from exceptions.CustomExceptions import ErrNullInsert
from repositories.interfaces import IRepositoryManager


class RecursoService:
    """Serviço de domínio para casos de uso de Recursos de 1ª e 2ª instância."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def get_primeira_instancia(self, date: Any, ata: Any) -> List[Dict[str, Any]]:
        """Retorna os recursos de primeira instância."""
        with self._db_manager.session() as session:
            repo = session.get_recurso_repository()
            return repo.get_primeira_instancia(date, ata)

    def get_segunda_instancia(self, date: Any) -> List[Dict[str, Any]]:
        """Retorna os recursos de segunda instância."""
        with self._db_manager.session() as session:
            repo = session.get_recurso_repository()
            return repo.get_segunda_instancia(date)

    def insert_primeira_instancia(
        self,
        recursos_primeira_instancia: List[Dict[str, Any]] | None,
    ) -> int:
        """Insere no banco de dados uma lista de recursos de primeira instância."""
        if recursos_primeira_instancia is None:
            raise ErrNullInsert(
                "Lista de recursos vazia, nenhum registro inserido", 400
            )

        with self._db_manager.session() as session:
            repo = session.get_recurso_repository()
            count = repo.insert_primeira_instancia(recursos_primeira_instancia)
            return count

    def insert_segunda_instancia(
        self,
        recursos_segunda_instancia: List[Dict[str, Any]] | None,
    ) -> int:
        """Insere no banco de dados uma lista de recursos de segunda instância."""
        if recursos_segunda_instancia is None:
            raise ErrNullInsert(
                "Lista de recursos vazia, nenhum registro inserido", 400
            )

        with self._db_manager.session() as session:
            repo = session.get_recurso_repository()
            count = repo.insert_segunda_instancia(recursos_segunda_instancia)
            return count
