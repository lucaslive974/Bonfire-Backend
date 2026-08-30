from typing import Any, Dict, List

from sqlalchemy import insert
from sqlalchemy.orm import Session

from repositories.models.autoinfracao_model import AutoInfracaoModel
from repositories.models.recurso_model import (
    RecursoPrimeiraInstanciaModel,
    RecursoSegundaInstanciaModel,
)


class RecursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_primeira_instancia(self, date: Any, ata: Any) -> List[Dict[str, Any]]:
        query = self.db.query(
            RecursoPrimeiraInstanciaModel.NUM_AI,
            RecursoPrimeiraInstanciaModel.NUM_ATA,
            RecursoPrimeiraInstanciaModel.DAT_PUBL,
            AutoInfracaoModel.COD_LINH,
            AutoInfracaoModel.NUM_VEIC,
            AutoInfracaoModel.IDN_PLAC_VEIC,
        ).join(
            AutoInfracaoModel,
            RecursoPrimeiraInstanciaModel.NUM_AI == AutoInfracaoModel.NUM_AI,
        )

        if ata is not None:
            query = query.filter(RecursoPrimeiraInstanciaModel.NUM_ATA == ata)
        if date is not None:
            query = query.filter(RecursoPrimeiraInstanciaModel.DAT_PUBL == date)

        results = query.limit(300).all()
        return [
            {
                "NUM_AI": r.NUM_AI,
                "NUM_ATA": r.NUM_ATA,
                "DAT_PUBL": r.DAT_PUBL.strftime("%Y-%m-%d") if r.DAT_PUBL else None,
                "COD_LINH": r.COD_LINH,
                "NUM_VEIC": r.NUM_VEIC,
                "IDN_PLAC_VEIC": r.IDN_PLAC_VEIC,
            }
            for r in results
        ]

    def get_segunda_instancia(self, date: Any) -> List[Dict[str, Any]]:
        query = self.db.query(
            RecursoSegundaInstanciaModel.NUM_AI,
            RecursoSegundaInstanciaModel.DAT_PUBL,
            AutoInfracaoModel.COD_LINH,
            AutoInfracaoModel.NUM_VEIC,
            AutoInfracaoModel.IDN_PLAC_VEIC,
        ).join(
            AutoInfracaoModel,
            RecursoSegundaInstanciaModel.NUM_AI == AutoInfracaoModel.NUM_AI,
        )

        if date is not None:
            query = query.filter(RecursoSegundaInstanciaModel.DAT_PUBL == date)

        results = query.limit(300).all()
        return [
            {
                "NUM_AI": r.NUM_AI,
                "DAT_PUBL": r.DAT_PUBL.strftime("%Y-%m-%d") if r.DAT_PUBL else None,
                "COD_LINH": r.COD_LINH,
                "NUM_VEIC": r.NUM_VEIC,
                "IDN_PLAC_VEIC": r.IDN_PLAC_VEIC,
            }
            for r in results
        ]

    def insert_primeira_instancia(self, rows: List[Dict[str, Any]]) -> int:
        counter = 0
        for row in rows:
            stmt = (
                insert(RecursoPrimeiraInstanciaModel).values(row).prefix_with("IGNORE")
            )
            result: Any = self.db.execute(stmt)
            rowcount = getattr(result, "rowcount", 0)
            if rowcount > 0:
                counter += 1
        return counter

    def insert_segunda_instancia(self, rows: List[Dict[str, Any]]) -> int:
        counter = 0
        for row in rows:
            stmt = (
                insert(RecursoSegundaInstanciaModel).values(row).prefix_with("IGNORE")
            )
            result: Any = self.db.execute(stmt)
            rowcount = getattr(result, "rowcount", 0)
            if rowcount > 0:
                counter += 1
        return counter
