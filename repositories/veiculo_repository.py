from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from classes.Veiculo import Veiculo
from exceptions.CustomExceptions import ErrUpdateData


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
            num_veic = data.get("NUM_VEIC")
            if num_veic is not None:
                dat_baix = data.get("DAT_BAIX")
                if isinstance(dat_baix, str):
                    try:
                        dat_baix = datetime.fromisoformat(dat_baix)
                    except ValueError:
                        dat_baix = None
                veiculo = Veiculo(
                    NUM_VEIC=int(num_veic),
                    IDN_PLAC_VEIC=data.get("IDN_PLAC_VEIC"),
                    VEIC_ATIV_EMPR=bool(data.get("VEIC_ATIV_EMPR", True)),
                    DAT_BAIX=dat_baix,
                )
                self.db.merge(veiculo)
                counter += 1
        return counter

    def update_bulk(self, veiculos_data: List[Dict[str, Any]]) -> int:
        counter = 0
        for data in veiculos_data:
            num_veic = data.get("NUM_VEIC")
            if num_veic is not None:
                try:
                    num_veic_int = int(num_veic)
                except (ValueError, TypeError):
                    continue
                veiculo = self.get_by_id(num_veic_int)
                if veiculo:
                    if "IDN_PLAC_VEIC" in data:
                        val = data.get("IDN_PLAC_VEIC")
                        veiculo.IDN_PLAC_VEIC = str(val) if val else None
                    if "VEIC_ATIV_EMPR" in data:
                        novo_status = bool(data.get("VEIC_ATIV_EMPR"))
                        if not novo_status:
                            if not veiculo.VEIC_ATIV_EMPR:
                                raise ErrUpdateData(
                                    f"Veículo {num_veic_int} já se encontra baixado",
                                    400,
                                )
                            veiculo.VEIC_ATIV_EMPR = False
                            dat_baix = data.get("DAT_BAIX")
                            if isinstance(dat_baix, str):
                                try:
                                    dat_baix = datetime.fromisoformat(dat_baix)
                                except ValueError:
                                    dat_baix = datetime.now()
                            veiculo.DAT_BAIX = (
                                dat_baix if dat_baix is not None else datetime.now()
                            )
                        else:
                            veiculo.VEIC_ATIV_EMPR = True
                            veiculo.DAT_BAIX = None
                    elif "DAT_BAIX" in data:
                        dat_baix = data.get("DAT_BAIX")
                        if isinstance(dat_baix, str):
                            try:
                                dat_baix = datetime.fromisoformat(dat_baix)
                            except ValueError:
                                dat_baix = None
                        veiculo.DAT_BAIX = dat_baix
                    self.db.merge(veiculo)
                    counter += 1
        return counter

    def delete(self, num_veic: int) -> int:
        deleted = self.db.query(Veiculo).filter(Veiculo.NUM_VEIC == num_veic).delete()
        return deleted
