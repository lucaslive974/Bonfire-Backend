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
        num_veics = [v.vehicle_number for v in veiculos if v.vehicle_number is not None]
        if not num_veics:
            return 0

        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            existing = repo.get_by_ids(num_veics)
            existing_map = {
                v.vehicle_number: v for v in existing if v.vehicle_number is not None
            }

            updated_ids = set()
            to_update: List[Veiculo] = []
            for item in veiculos:
                if (
                    item.vehicle_number is not None
                    and item.vehicle_number in existing_map
                ):
                    veiculo = existing_map[item.vehicle_number]
                    if item.license_plate is not None:
                        veiculo.set_license_plate(item.license_plate)
                    if item.active is not None:
                        if not item.active:
                            veiculo.deactivate(item.deregistration_date)
                        else:
                            veiculo.activate()
                    elif item.deregistration_date is not None:
                        veiculo.set_deregistration_date(item.deregistration_date)

                    if item.vehicle_number not in updated_ids:
                        to_update.append(veiculo)
                        updated_ids.add(item.vehicle_number)

            if not to_update:
                return 0

            return repo.update_bulk(to_update)

    def delete_veiculos(self, num_veic: str | int) -> int:
        """Delete a vehicle from the database by its vehicle number."""
        try:
            num_veic_int = int(num_veic)
        except ValueError:
            raise ErrUpdateData("Número do veículo inválido", 400)

        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            return repo.delete(num_veic_int)
