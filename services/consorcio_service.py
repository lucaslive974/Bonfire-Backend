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
        ids = [item.id for item in consorcios if item.id is not None]
        if not ids:
            return 0

        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            existing = repo.get_by_ids(ids)
            existing_map = {op.id: op for op in existing if op.id is not None}

            updated_ids = set()
            to_update: List[Operadora] = []
            for item in consorcios:
                if item.id is not None and item.id in existing_map:
                    operadora = existing_map[item.id]
                    if item.name is not None:
                        operadora.set_name(item.name)
                    if item.concessionaire is not None:
                        operadora.set_concessionaire(item.concessionaire)

                    if item.id not in updated_ids:
                        to_update.append(operadora)
                        updated_ids.add(item.id)

            if not to_update:
                return 0

            return repo.update_bulk(to_update)

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
