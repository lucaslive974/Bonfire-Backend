from typing import List

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
            COMPARTILHADA=bool(
                entity.COMPARTILHADA if entity.COMPARTILHADA is not None else False
            ),
            LINH_ATIV_EMPR=bool(
                entity.LINH_ATIV_EMPR if entity.LINH_ATIV_EMPR is not None else True
            ),
            DAT_BAIX=entity.DAT_BAIX,
        )

    def get_all(self) -> List[Linha]:
        """Return all line entities."""
        models = self.db.query(LinhaModel).all()
        return [self._to_domain(m) for m in models if m is not None]

    def get_by_id(self, cod_linh: str) -> Linha | None:
        """Find a line by its line code."""
        model = (
            self.db.query(LinhaModel).filter(LinhaModel.COD_LINH == cod_linh).first()
        )
        return self._to_domain(model)

    def insert_bulk(self, linhas: List[Linha]) -> int:
        """Insert a list of line domain entities into the database."""
        from exceptions.CustomExceptions import ErrInsertData
        from repositories.models.operadora_model import OperadoraModel

        new_cod_linhas = [
            linha.COD_LINH for linha in linhas if linha.COD_LINH is not None
        ]
        operadoras_ids = {
            linha.ID_OPERADORA for linha in linhas if linha.ID_OPERADORA is not None
        }

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

        if new_cod_linhas:
            existentes = (
                self.db.query(LinhaModel.COD_LINH)
                .filter(LinhaModel.COD_LINH.in_(new_cod_linhas))
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
        for linha in linhas:
            model = self._to_model(linha)
            self.db.add(model)
            counter += 1
        return counter

    def update_bulk(self, linhas: List[Linha]) -> int:
        """Update fields for a list of line domain entities in the database."""
        from exceptions.CustomExceptions import ErrUpdateData
        from repositories.models.operadora_model import OperadoraModel

        operadoras_ids = {
            linha.ID_OPERADORA for linha in linhas if linha.ID_OPERADORA is not None
        }

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
        for item in linhas:
            if isinstance(item.line_code, str):
                model = (
                    self.db.query(LinhaModel)
                    .filter(LinhaModel.COD_LINH == item.line_code)
                    .first()
                )
                if model:
                    linha = self._to_domain(model)
                    if linha:
                        if item.shared is not None:
                            linha.set_shared(item.shared)
                        if item.operator_id is not None:
                            linha.set_operator_id(item.operator_id)
                        if item.active is not None:
                            if not item.active:
                                linha.deactivate(item.deregistration_date)
                            else:
                                linha.activate()
                        elif item.deregistration_date is not None:
                            linha.set_deregistration_date(item.deregistration_date)

                        model.COMPARTILHADA = linha.is_shared()
                        model.ID_OPERADORA = linha.get_operator_id()
                        model.LINH_ATIV_EMPR = linha.is_active()
                        model.DAT_BAIX = linha.get_deregistration_date()
                        self.db.merge(model)
                        counter += 1
        return counter

    def delete(self, cod_linh: str) -> int:
        """Delete a line by its line code."""
        deleted = (
            self.db.query(LinhaModel).filter(LinhaModel.COD_LINH == cod_linh).delete()
        )
        return deleted
