from typing import List

from sqlalchemy.orm import Session

from classes.Operadora import Operadora
from repositories.interfaces import IConsorcioRepository
from repositories.models.operadora_model import OperadoraModel


class ConsorcioRepository(IConsorcioRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: OperadoraModel | None) -> Operadora | None:
        if model is None:
            return None
        return Operadora(
            ID=model.ID,
            NOME=model.NOME,
            CONCESSIONARIA=model.CONCESSIONARIA,
        )

    def _to_model(self, entity: Operadora) -> OperadoraModel:
        return OperadoraModel(
            ID=entity.ID,
            NOME=entity.NOME,
            CONCESSIONARIA=entity.CONCESSIONARIA,
        )

    def get_all(self) -> List[Operadora]:
        """Return all operator entities (consórcios)."""
        models = self.db.query(OperadoraModel).all()
        return [self._to_domain(m) for m in models if m is not None]

    def get_by_id(self, id_consorcio: int) -> Operadora | None:
        """Find an operator by ID."""
        model = (
            self.db.query(OperadoraModel)
            .filter(OperadoraModel.ID == id_consorcio)
            .first()
        )
        return self._to_domain(model)

    def insert_bulk(self, consorcios: List[Operadora]) -> int:
        """Insert or merge a list of consórcio entities into the database."""
        counter = 0
        for item in consorcios:
            model = self._to_model(item)
            self.db.merge(model)
            counter += 1
        return counter

    def update_bulk(self, consorcios: List[Operadora]) -> int:
        """Update fields for a list of consórcio entities in the database."""
        counter = 0
        for item in consorcios:
            if item.ID is not None:
                model = (
                    self.db.query(OperadoraModel)
                    .filter(OperadoraModel.ID == item.ID)
                    .first()
                )
                if model:
                    operadora = self._to_domain(model)
                    if operadora:
                        if item.name is not None:
                            operadora.set_name(item.name)
                        if item.concessionaire is not None:
                            operadora.set_concessionaire(item.concessionaire)
                        model.NOME = operadora.get_name()
                        model.CONCESSIONARIA = operadora.get_concessionaire()
                        self.db.merge(model)
                        counter += 1
        return counter

    def delete(self, id_consorcio: int) -> int:
        """Delete a consórcio by its ID."""
        deleted = (
            self.db.query(OperadoraModel)
            .filter(OperadoraModel.ID == id_consorcio)
            .delete()
        )
        return deleted
