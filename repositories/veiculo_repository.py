from typing import List, Dict, Any
from sqlalchemy.orm import Session
from classes.Veiculo import Veiculo


class VeiculoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Veiculo]:
        return self.db.query(Veiculo).all()

    def get_by_id(self, num_veic: int) -> Veiculo | None:
        return self.db.query(Veiculo).filter(Veiculo.NUM_VEIC == num_veic).first()

    def insert(self, veiculo: Veiculo) -> bool:
        self.db.add(veiculo)
        return True

    def insert_bulk(self, veiculos_data: List[Dict[str, Any]]) -> int:
        counter = 0
        for data in veiculos_data:
            num_veic = data.get("NUM_VEIC") or data.get("num_veiculo")
            if num_veic is not None:
                veiculo = Veiculo(
                    NUM_VEIC=int(num_veic),
                    IDN_PLAC_VEIC=data.get("IDN_PLAC_VEIC") or data.get("placa"),
                    VEIC_ATIV_EMPR=bool(data.get("VEIC_ATIV_EMPR", True)),
                )
                self.db.merge(veiculo)
                counter += 1
        return counter

    def update_bulk(self, veiculos_data: List[Dict[str, Any]]) -> int:
        counter = 0
        for data in veiculos_data:
            num_veic = data.get("NUM_VEIC") or data.get("num_veiculo")
            if num_veic is not None:
                try:
                    num_veic_int = int(num_veic)
                except (ValueError, TypeError):
                    continue
                veiculo = self.get_by_id(num_veic_int)
                if veiculo:
                    if "IDN_PLAC_VEIC" in data or "placa" in data:
                        val = data.get("IDN_PLAC_VEIC") or data.get("placa")
                        veiculo.IDN_PLAC_VEIC = str(val) if val else None
                    if "VEIC_ATIV_EMPR" in data:
                        veiculo.VEIC_ATIV_EMPR = bool(data.get("VEIC_ATIV_EMPR"))
                    self.db.merge(veiculo)
                    counter += 1
        return counter

    def delete(self, num_veic: int) -> int:
        deleted = self.db.query(Veiculo).filter(Veiculo.NUM_VEIC == num_veic).delete()
        return deleted
