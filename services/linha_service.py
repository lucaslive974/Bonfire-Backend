from typing import List

from classes.Linha import Linha
from repositories.interfaces import IRepositoryManager


class LinhaService:
    """Domain service for Bus Line use cases."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def get_linha(self) -> List[Linha]:
        """Retrieve line data from the database as domain entities."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            return repo.get_all()

    def insert_linha(self, linhas: List[Linha]) -> int:
        """Insert a list of line domain entities into the database."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            return repo.insert_bulk(linhas)

    def update_linha(self, linhas: List[Linha]) -> int:
        """Update a list of line domain entities in the database."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            return repo.update_bulk(linhas)

    def delete_linha(self, cod_linh: str) -> int:
        """Delete a line from the database by its line code."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            return repo.delete(cod_linh)
