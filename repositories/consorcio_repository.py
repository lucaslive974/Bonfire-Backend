from typing import Any, Dict, List

from sqlalchemy.orm import Session

from classes.Operadora import Operadora
from repositories.models.operadora_model import OperadoraModel


class ConsorcioRepository:
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
        """Retorna todas as operadoras (consórcios)."""
        models = self.db.query(OperadoraModel).all()
        return [self._to_domain(m) for m in models if m is not None]

    def get_by_id(self, id_consorcio: int) -> Operadora | None:
        """Busca uma operadora pelo ID."""
        model = (
            self.db.query(OperadoraModel)
            .filter(OperadoraModel.ID == id_consorcio)
            .first()
        )
        return self._to_domain(model)

    def insert_bulk(self, consorcios_data: List[Dict[str, Any]]) -> int:
        """Insere ou atualiza (merge) uma lista de consórcios no banco de dados."""
        counter = 0
        for data in consorcios_data:
            id_consorcio = data.get("ID") or data.get("id")
            if id_consorcio is not None:
                operadora = Operadora(
                    ID=int(id_consorcio),
                    NOME=data.get("NOME") or data.get("nome"),
                    CONCESSIONARIA=data.get("CONCESSIONARIA")
                    or data.get("concessionaria"),
                )
                model = self._to_model(operadora)
                self.db.merge(model)
                counter += 1
        return counter

    def update_bulk(self, consorcios_data: List[Dict[str, Any]]) -> int:
        """Atualiza campos de uma lista de consórcios no banco de dados."""
        counter = 0
        for data in consorcios_data:
            id_consorcio = data.get("ID") or data.get("id")
            if id_consorcio is not None:
                try:
                    id_consorcio_int = int(id_consorcio)
                except (ValueError, TypeError):
                    continue
                model = (
                    self.db.query(OperadoraModel)
                    .filter(OperadoraModel.ID == id_consorcio_int)
                    .first()
                )
                if model:
                    operadora = self._to_domain(model)
                    if operadora:
                        operadora.atualizar(data)
                        model.NOME = operadora.NOME
                        model.CONCESSIONARIA = operadora.CONCESSIONARIA
                        self.db.merge(model)
                        counter += 1
        return counter

    def delete(self, id_consorcio: int) -> int:
        """Exclui um consórcio pelo ID."""
        deleted = (
            self.db.query(OperadoraModel)
            .filter(OperadoraModel.ID == id_consorcio)
            .delete()
        )
        return deleted
