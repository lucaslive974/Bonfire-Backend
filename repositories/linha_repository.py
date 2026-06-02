from typing import List, Dict, Any
from sqlalchemy.orm import Session
from classes.Linha import Linha

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
            linha = Linha(
                COD_LINH=str(data.get("COD_LINH") or data.get("num_linha") or ""),
                ID_OPERADORA=data.get("ID_OPERADORA") or data.get("id_operadora"),
                COMPARTILHADA=bool(data.get("COMPARTILHADA") or data.get("compartilhada", False)),
                LINH_ATIV_EMPR=bool(data.get("LINH_ATIV_EMPR", True))
            )
            self.db.merge(linha)
            counter += 1
        return counter

    def update_bulk(self, linhas_data: List[Dict[str, Any]]) -> int:
        counter = 0
        for data in linhas_data:
            cod_linh = data.get("COD_LINH") or data.get("num_linha")
            if isinstance(cod_linh, str):
                linha = self.get_by_id(cod_linh)
                if linha:
                    if "COMPARTILHADA" in data or "compartilhada" in data:
                        val = data.get("COMPARTILHADA")
                        if val is None:
                            val = data.get("compartilhada")
                        linha.COMPARTILHADA = bool(val)
                    if "LINH_ATIV_EMPR" in data:
                        linha.LINH_ATIV_EMPR = bool(data.get("LINH_ATIV_EMPR"))
                    self.db.merge(linha)
                    counter += 1
        return counter

    def delete(self, cod_linh: str) -> int:
        deleted = self.db.query(Linha).filter(Linha.COD_LINH == cod_linh).delete()
        return deleted
