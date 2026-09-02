from typing import Any, Dict, List

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
            VEIC_ATIV_EMPR=entity.VEIC_ATIV_EMPR,
            DAT_BAIX=entity.DAT_BAIX,
        )

    def get_all(self) -> List[Veiculo]:
        models = self.db.query(VeiculoModel).all()
        return [self._to_domain(m) for m in models if m is not None]

    def get_by_id(self, num_veic: int) -> Veiculo | None:
        model = (
            self.db.query(VeiculoModel)
            .filter(VeiculoModel.NUM_VEIC == num_veic)
            .first()
        )
        return self._to_domain(model)

    def insert(self, veiculo: Veiculo) -> bool:
        model = self._to_model(veiculo)
        self.db.add(model)
        return True

    def insert_bulk(self, veiculos_data: List[Dict[str, Any]]) -> int:
        from exceptions.CustomExceptions import ErrInsertData

        novos_num_veic = []
        for data in veiculos_data:
            if data.get("NUM_VEIC") is not None:
                try:
                    novos_num_veic.append(int(data.get("NUM_VEIC")))
                except ValueError, TypeError:
                    continue

        if novos_num_veic:
            existentes = (
                self.db.query(VeiculoModel.NUM_VEIC)
                .filter(VeiculoModel.NUM_VEIC.in_(novos_num_veic))
                .all()
            )
            if existentes:
                veiculos_existentes = ", ".join(str(e[0]) for e in existentes)
                raise ErrInsertData(
                    message="Veículo já existe",
                    status=409,
                    error="Conflict",
                    friendly_message=f"Os seguintes veículos já existem e não podem ser sobrescritos: {veiculos_existentes}",
                )

        counter = 0
        for data in veiculos_data:
            num_veic = data.get("NUM_VEIC")
            if num_veic is not None:
                try:
                    num_veic_int = int(num_veic)
                except ValueError, TypeError:
                    continue
                veiculo = Veiculo(
                    NUM_VEIC=num_veic_int,
                    IDN_PLAC_VEIC=data.get("IDN_PLAC_VEIC"),
                    VEIC_ATIV_EMPR=bool(data.get("VEIC_ATIV_EMPR", True)),
                    DAT_BAIX=data.get("DAT_BAIX"),
                )
                model = self._to_model(veiculo)
                self.db.add(model)
                counter += 1
        return counter

    def update_bulk(self, veiculos_data: List[Dict[str, Any]]) -> int:
        counter = 0
        for data in veiculos_data:
            num_veic = data.get("NUM_VEIC")
            if num_veic is not None:
                try:
                    num_veic_int = int(num_veic)
                except ValueError, TypeError:
                    continue
                model = (
                    self.db.query(VeiculoModel)
                    .filter(VeiculoModel.NUM_VEIC == num_veic_int)
                    .first()
                )
                if model:
                    veiculo = self._to_domain(model)
                    if veiculo:
                        veiculo.atualizar(data)
                        model.IDN_PLAC_VEIC = veiculo.IDN_PLAC_VEIC
                        model.VEIC_ATIV_EMPR = veiculo.VEIC_ATIV_EMPR
                        model.DAT_BAIX = veiculo.DAT_BAIX
                        self.db.merge(model)
                        counter += 1
        return counter

    def delete(self, num_veic: int) -> int:
        deleted = (
            self.db.query(VeiculoModel)
            .filter(VeiculoModel.NUM_VEIC == num_veic)
            .delete()
        )
        return deleted
