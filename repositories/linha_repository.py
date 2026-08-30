from typing import Any, Dict, List

from sqlalchemy.orm import Session

from classes.Linha import Linha
from repositories.models.linha_model import LinhaModel


class LinhaRepository:
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: LinhaModel | None) -> Linha | None:
        if model is None:
            return None
        return Linha(
            COD_LINH=model.COD_LINH,
            ID_OPERADORA=model.ID_OPERADORA,
            COMPARTILHADA=model.COMPARTILHADA,
            LINH_ATIV_EMPR=model.LINH_ATIV_EMPR,
            DAT_BAIX=model.DAT_BAIX,
        )

    def _to_model(self, entity: Linha) -> LinhaModel:
        return LinhaModel(
            COD_LINH=entity.COD_LINH,
            ID_OPERADORA=entity.ID_OPERADORA,
            COMPARTILHADA=entity.COMPARTILHADA,
            LINH_ATIV_EMPR=entity.LINH_ATIV_EMPR,
            DAT_BAIX=entity.DAT_BAIX,
        )

    def get_all(self) -> List[Linha]:
        models = self.db.query(LinhaModel).all()
        return [self._to_domain(m) for m in models if m is not None]

    def get_by_id(self, cod_linh: str) -> Linha | None:
        model = (
            self.db.query(LinhaModel).filter(LinhaModel.COD_LINH == cod_linh).first()
        )
        return self._to_domain(model)

    def insert_bulk(self, linhas_data: List[Dict[str, Any]]) -> int:
        counter = 0
        for data in linhas_data:
            cod_linh = data.get("COD_LINH")
            if cod_linh is not None:
                linha = Linha(
                    COD_LINH=str(cod_linh),
                    ID_OPERADORA=data.get("ID_OPERADORA"),
                    COMPARTILHADA=bool(data.get("COMPARTILHADA", False)),
                    LINH_ATIV_EMPR=bool(data.get("LINH_ATIV_EMPR", True)),
                    DAT_BAIX=data.get("DAT_BAIX"),
                )
                model = self._to_model(linha)
                self.db.merge(model)
                counter += 1
        return counter

    def update_bulk(self, linhas_data: List[Dict[str, Any]]) -> int:
        counter = 0
        for data in linhas_data:
            cod_linh = data.get("COD_LINH")
            if isinstance(cod_linh, str):
                model = (
                    self.db.query(LinhaModel)
                    .filter(LinhaModel.COD_LINH == cod_linh)
                    .first()
                )
                if model:
                    linha = self._to_domain(model)
                    if linha:
                        linha.atualizar(data)
                        model.COMPARTILHADA = linha.COMPARTILHADA
                        model.ID_OPERADORA = linha.ID_OPERADORA
                        model.LINH_ATIV_EMPR = linha.LINH_ATIV_EMPR
                        model.DAT_BAIX = linha.DAT_BAIX
                        self.db.merge(model)
                        counter += 1
        return counter

    def delete(self, cod_linh: str) -> int:
        deleted = (
            self.db.query(LinhaModel).filter(LinhaModel.COD_LINH == cod_linh).delete()
        )
        return deleted
