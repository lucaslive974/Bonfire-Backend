from typing import List

from classes.Operadora import Operadora
from exceptions.CustomExceptions import ErrUpdateData
from repositories.interfaces import IRepositoryManager


class ConsorcioService:
    """Domain service for Consórcio / Operadora use cases."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def get_consorcios(self) -> List[Operadora]:
        """Return all registered consórcios as domain entities."""
        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            return repo.get_all()

    def insert_consorcios(self, consorcios: List[Operadora]) -> int:
        """Insert or merge a list of consórcio domain entities in the database."""
        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            return repo.insert_bulk(consorcios)

    def update_consorcios(self, consorcios: List[Operadora]) -> int:
        """Update a list of consórcio domain entities in the database."""
        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            return repo.update_bulk(consorcios)

    def delete_consorcio(self, id_consorcio: str | int) -> int:
        """Delete a consórcio from the database by its ID."""
        try:
            id_consorcio_int = int(id_consorcio)
        except ValueError:
            raise ErrUpdateData("ID do consórcio inválido", 400)

        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            count = repo.delete(id_consorcio_int)
            return count
