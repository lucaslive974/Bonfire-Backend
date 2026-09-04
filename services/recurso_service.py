from typing import Any, Dict, List

from exceptions.CustomExceptions import ErrNullInsert
from repositories.interfaces import IRepositoryManager


class RecursoService:
    """Domain service for 1st and 2nd instance appeal use cases."""

    def __init__(self, db_manager: IRepositoryManager, parser_factory=None):
        self._parser_factory = parser_factory
        self._db_manager = db_manager

    def get_primeira_instancia(self, date: Any, ata: Any) -> List[Dict[str, Any]]:
        """Return 1st instance appeals."""
        with self._db_manager.session() as session:
            repo = session.get_recurso_repository()
            return repo.get_primeira_instancia(date, ata)

    def get_segunda_instancia(self, date: Any) -> List[Dict[str, Any]]:
        """Return 2nd instance appeals."""
        with self._db_manager.session() as session:
            repo = session.get_recurso_repository()
            return repo.get_segunda_instancia(date)

    def insert_primeira_instancia(
        self,
        recursos_primeira_instancia: List[Dict[str, Any]] | None,
    ) -> int:
        """Insert a list of 1st instance appeals into the database."""
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
        """Insert a list of 2nd instance appeals into the database."""
        if recursos_segunda_instancia is None:
            raise ErrNullInsert(
                "Lista de recursos vazia, nenhum registro inserido", 400
            )

        with self._db_manager.session() as session:
            repo = session.get_recurso_repository()
            count = repo.insert_segunda_instancia(recursos_segunda_instancia)
            return count

    def extract_primeira_instancia(self, file_stream: Any) -> dict:
        if not self._parser_factory:
            raise RuntimeError("ParserFactory not injected")
        extractor = self._parser_factory.create_primeira_instancia_parser()
        return extractor.extract(file_stream)

    def extract_segunda_instancia(self, file_stream: Any) -> dict:
        if not self._parser_factory:
            raise RuntimeError("ParserFactory not injected")
        extractor = self._parser_factory.create_segunda_instancia_parser()
        return extractor.extract(file_stream)
