from typing import List

from sqlalchemy.orm import Session

from classes.Veiculo import Veiculo
from repositories.interfaces import IVeiculoRepository
from repositories.models.veiculo_model import VeiculoModel


class VeiculoRepository(IVeiculoRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: VeiculoModel | None) -> Veiculo | None:
        if model is None:
            return None
        return Veiculo(
            NUM_VEIC=model.NUM_VEIC,
            IDN_PLAC_VEIC=model.IDN_PLAC_VEIC,
            VEIC_ATIV_EMPR=model.VEIC_ATIV_EMPR,
            DAT_BAIX=model.DAT_BAIX,
        )

    def _to_model(self, entity: Veiculo) -> VeiculoModel:
        return VeiculoModel(
            NUM_VEIC=entity.NUM_VEIC,
            IDN_PLAC_VEIC=entity.IDN_PLAC_VEIC,
            VEIC_ATIV_EMPR=bool(
                entity.VEIC_ATIV_EMPR if entity.VEIC_ATIV_EMPR is not None else True
            ),
            DAT_BAIX=entity.DAT_BAIX,
        )

    def get_all(self) -> List[Veiculo]:
        """Return all vehicle entities."""
        models = self.db.query(VeiculoModel).all()
        return [self._to_domain(m) for m in models if m is not None]

    def get_by_id(self, num_veic: int) -> Veiculo | None:
        """Find a vehicle by its vehicle number."""
        model = (
            self.db.query(VeiculoModel)
            .filter(VeiculoModel.NUM_VEIC == num_veic)
            .first()
        )
        return self._to_domain(model)

    def get_by_ids(self, num_veics: List[int]) -> List[Veiculo]:
        """Find vehicles by a list of vehicle numbers."""
        if not num_veics:
            return []
        models = (
            self.db.query(VeiculoModel)
            .filter(VeiculoModel.NUM_VEIC.in_(num_veics))
            .all()
        )
        return [self._to_domain(m) for m in models if m is not None]

    def insert(self, veiculo: Veiculo) -> bool:
        """Insert a single vehicle entity."""
        model = self._to_model(veiculo)
        self.db.add(model)
        return True

    def insert_bulk(self, veiculos: List[Veiculo]) -> int:
        """Insert a list of vehicle domain entities into the database."""
        from exceptions.CustomExceptions import ErrInsertData

        new_num_veics = [v.NUM_VEIC for v in veiculos if v.NUM_VEIC is not None]

        if new_num_veics:
            existing = (
                self.db.query(VeiculoModel.NUM_VEIC)
                .filter(VeiculoModel.NUM_VEIC.in_(new_num_veics))
                .all()
            )
            if existing:
                existing_veiculos = ", ".join(str(e[0]) for e in existing)
                raise ErrInsertData(
                    message="Veículo já existe",
                    status=409,
                    error="Conflict",
                    friendly_message=f"Os seguintes veículos já existem e não podem ser sobrescritos: {existing_veiculos}",
                )

        counter = 0
        for veiculo in veiculos:
            model = self._to_model(veiculo)
            self.db.add(model)
            counter += 1
        return counter

    def update_bulk(self, veiculos: List[Veiculo]) -> int:
        """Persist updated vehicle domain entities to the database."""
        counter = 0
        for veiculo in veiculos:
            if veiculo.vehicle_number is not None:
                model = self._to_model(veiculo)
                self.db.merge(model)
                counter += 1
        return counter

    def delete(self, num_veic: int) -> int:
        """Delete a vehicle by its vehicle number."""
        deleted = (
            self.db.query(VeiculoModel)
            .filter(VeiculoModel.NUM_VEIC == num_veic)
            .delete()
        )
        return deleted
