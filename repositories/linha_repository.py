from typing import Any, Dict, List

from sqlalchemy.orm import Session

from classes.Linha import Linha
from repositories.interfaces import ILinhaRepository
from repositories.models.linha_model import LinhaModel


class LinhaRepository(ILinhaRepository):
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
        from exceptions.CustomExceptions import ErrInsertData
        from repositories.models.operadora_model import OperadoraModel

        novos_cod_linh = []
        operadoras_ids = set()
        for data in linhas_data:
            cod = data.get("COD_LINH")
            if cod is not None:
                novos_cod_linh.append(str(cod))
            op_id = data.get("ID_OPERADORA")
            if op_id is not None:
                operadoras_ids.add(op_id)

        if operadoras_ids:
            existentes_operadoras = (
                self.db.query(OperadoraModel.ID)
                .filter(OperadoraModel.ID.in_(operadoras_ids))
                .all()
            )
            existentes_ids = {e[0] for e in existentes_operadoras}
            faltantes = operadoras_ids - existentes_ids
            if faltantes:
                faltantes_str = ", ".join(str(f) for f in faltantes)
                raise ErrInsertData(
                    message="Operadora inexistente",
                    status=400,
                    error="Bad Request",
                    friendly_message=f"Os seguintes consórcios/operadoras não existem: {faltantes_str}",
                )

        if novos_cod_linh:
            existentes = (
                self.db.query(LinhaModel.COD_LINH)
                .filter(LinhaModel.COD_LINH.in_(novos_cod_linh))
                .all()
            )
            if existentes:
                linhas_existentes = ", ".join(str(e[0]) for e in existentes)
                raise ErrInsertData(
                    message="Linha já existe",
                    status=409,
                    error="Conflict",
                    friendly_message=f"As seguintes linhas já existem e não podem ser sobrescritas: {linhas_existentes}",
                )

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
                self.db.add(model)
                counter += 1
        return counter

    def update_bulk(self, linhas_data: List[Dict[str, Any]]) -> int:
        from exceptions.CustomExceptions import ErrUpdateData
        from repositories.models.operadora_model import OperadoraModel

        operadoras_ids = set()
        for data in linhas_data:
            op_id = data.get("ID_OPERADORA")
            if op_id is not None:
                operadoras_ids.add(op_id)

        if operadoras_ids:
            existentes_operadoras = (
                self.db.query(OperadoraModel.ID)
                .filter(OperadoraModel.ID.in_(operadoras_ids))
                .all()
            )
            existentes_ids = {e[0] for e in existentes_operadoras}
            faltantes = operadoras_ids - existentes_ids
            if faltantes:
                faltantes_str = ", ".join(str(f) for f in faltantes)
                raise ErrUpdateData(
                    message="Operadora inexistente",
                    status=400,
                    error="Bad Request",
                    friendly_message=f"Não é possível atualizar. Os seguintes consórcios/operadoras não existem: {faltantes_str}",
                )

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
