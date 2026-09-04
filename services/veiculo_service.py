from typing import List

from classes.Veiculo import Veiculo
from exceptions.CustomExceptions import ErrUpdateData
from repositories.interfaces import IRepositoryManager


class VeiculoService:
    """Domain service for Vehicle use cases."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def get_veiculos(self) -> List[Veiculo]:
        """Retrieve vehicles from the database as domain entities."""
        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            return repo.get_all()

    def insert_veiculos(self, veiculos: List[Veiculo]) -> int:
        """Insert a list of vehicle domain entities into the database."""
        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            return repo.insert_bulk(veiculos)

    def update_veiculos(self, veiculos: List[Veiculo]) -> int:
        """Update a list of vehicle domain entities in the database."""
        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            return repo.update_bulk(veiculos)

    def delete_veiculos(self, num_veic: str | int) -> int:
        """Delete a vehicle from the database by its vehicle number."""
        try:
            num_veic_int = int(num_veic)
        except ValueError:
            raise ErrUpdateData("Número do veículo inválido", 400)

        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            return repo.delete(num_veic_int)
