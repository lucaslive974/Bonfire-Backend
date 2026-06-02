from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import insert
from classes.Recurso import RecursoPrimeiraInstancia, RecursoSegundaInstancia
from classes.AutoInfracao import AutoInfracao

class RecursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_primeira_instancia(self, date: Any, ata: Any) -> List[Dict[str, Any]]:
        query = self.db.query(
            RecursoPrimeiraInstancia.NUM_AI,
            RecursoPrimeiraInstancia.NUM_ATA,
            RecursoPrimeiraInstancia.DAT_PUBL,
            AutoInfracao.COD_LINH,
            AutoInfracao.NUM_VEIC,
            AutoInfracao.IDN_PLAC_VEIC
        ).join(AutoInfracao, RecursoPrimeiraInstancia.NUM_AI == AutoInfracao.NUM_AI)

        if ata is not None:
            query = query.filter(RecursoPrimeiraInstancia.NUM_ATA == ata)
        if date is not None:
            query = query.filter(RecursoPrimeiraInstancia.DAT_PUBL == date)

        results = query.limit(300).all()
        return [
            {
                "NUM_AI": r.NUM_AI,
                "NUM_ATA": r.NUM_ATA,
                "DAT_PUBL": r.DAT_PUBL.strftime("%Y-%m-%d") if r.DAT_PUBL else None,
                "COD_LINH": r.COD_LINH,
                "NUM_VEIC": r.NUM_VEIC,
                "IDN_PLAC_VEIC": r.IDN_PLAC_VEIC
            }
            for r in results
        ]

    def get_segunda_instancia(self, date: Any) -> List[Dict[str, Any]]:
        query = self.db.query(
            RecursoSegundaInstancia.NUM_AI,
            RecursoSegundaInstancia.DAT_PUBL,
            AutoInfracao.COD_LINH,
            AutoInfracao.NUM_VEIC,
            AutoInfracao.IDN_PLAC_VEIC
        ).join(AutoInfracao, RecursoSegundaInstancia.NUM_AI == AutoInfracao.NUM_AI)

        if date is not None:
            query = query.filter(RecursoSegundaInstancia.DAT_PUBL == date)

        results = query.limit(300).all()
        return [
            {
                "NUM_AI": r.NUM_AI,
                "DAT_PUBL": r.DAT_PUBL.strftime("%Y-%m-%d") if r.DAT_PUBL else None,
                "COD_LINH": r.COD_LINH,
                "NUM_VEIC": r.NUM_VEIC,
                "IDN_PLAC_VEIC": r.IDN_PLAC_VEIC
            }
            for r in results
        ]

    def insert_primeira_instancia(self, rows: List[Dict[str, Any]]) -> int:
        counter = 0
        for row in rows:
            stmt = insert(RecursoPrimeiraInstancia).values(row).prefix_with("IGNORE")
            result: Any = self.db.execute(stmt)
            rowcount = getattr(result, "rowcount", 0)
            if rowcount > 0:
                counter += 1
        return counter

    def insert_segunda_instancia(self, rows: List[Dict[str, Any]]) -> int:
        counter = 0
        for row in rows:
            stmt = insert(RecursoSegundaInstancia).values(row).prefix_with("IGNORE")
            result: Any = self.db.execute(stmt)
            rowcount = getattr(result, "rowcount", 0)
            if rowcount > 0:
                counter += 1
        return counter
