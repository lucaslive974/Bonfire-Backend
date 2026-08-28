from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from classes.Linha import Linha
from exceptions.CustomExceptions import ErrUpdateData


class LinhaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Linha]:
        return self.db.query(Linha).all()

    def get_by_id(self, cod_linh: str) -> Linha | None:
        return self.db.query(Linha).filter(Linha.COD_LINH == cod_linh).first()

    def insert_bulk(self, linhas_data: List[Dict[str, Any]]) -> int:
        counter = 0
        for data in linhas_data:
            cod_linh = data.get("COD_LINH")
            if cod_linh is not None:
                dat_baix = data.get("DAT_BAIX")
                if isinstance(dat_baix, str):
                    try:
                        dat_baix = datetime.fromisoformat(dat_baix)
                    except ValueError:
                        dat_baix = None
                linha = Linha(
                    COD_LINH=str(cod_linh),
                    ID_OPERADORA=data.get("ID_OPERADORA"),
                    COMPARTILHADA=bool(data.get("COMPARTILHADA", False)),
                    LINH_ATIV_EMPR=bool(data.get("LINH_ATIV_EMPR", True)),
                    DAT_BAIX=dat_baix,
                )
                self.db.merge(linha)
                counter += 1
        return counter

    def update_bulk(self, linhas_data: List[Dict[str, Any]]) -> int:
        counter = 0
        for data in linhas_data:
            cod_linh = data.get("COD_LINH")
            if isinstance(cod_linh, str):
                linha = self.get_by_id(cod_linh)
                if linha:
                    if "COMPARTILHADA" in data:
                        linha.COMPARTILHADA = bool(data.get("COMPARTILHADA"))
                    if "ID_OPERADORA" in data:
                        linha.ID_OPERADORA = data.get("ID_OPERADORA")
                    if "LINH_ATIV_EMPR" in data:
                        novo_status = bool(data.get("LINH_ATIV_EMPR"))
                        if not novo_status:
                            if not linha.LINH_ATIV_EMPR:
                                raise ErrUpdateData(
                                    f"Linha {cod_linh} já se encontra baixada",
                                    400,
                                )
                            linha.LINH_ATIV_EMPR = False
                            dat_baix = data.get("DAT_BAIX")
                            if isinstance(dat_baix, str):
                                try:
                                    dat_baix = datetime.fromisoformat(dat_baix)
                                except ValueError:
                                    dat_baix = datetime.now()
                            linha.DAT_BAIX = (
                                dat_baix if dat_baix is not None else datetime.now()
                            )
                        else:
                            linha.LINH_ATIV_EMPR = True
                            linha.DAT_BAIX = None
                    elif "DAT_BAIX" in data:
                        dat_baix = data.get("DAT_BAIX")
                        if isinstance(dat_baix, str):
                            try:
                                dat_baix = datetime.fromisoformat(dat_baix)
                            except ValueError:
                                dat_baix = None
                        linha.DAT_BAIX = dat_baix
                    self.db.merge(linha)
                    counter += 1
        return counter

    def delete(self, cod_linh: str) -> int:
        deleted = self.db.query(Linha).filter(Linha.COD_LINH == cod_linh).delete()
        return deleted
