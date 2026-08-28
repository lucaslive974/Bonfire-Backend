from typing import List, Tuple, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import insert
from classes.AutoInfracao import AutoInfracao
from repositories.models.autoinfracao_model import AutoInfracaoModel


def insert_ignore_mysql(table, conn, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]
    stmt = insert(table.table).values(data).prefix_with("IGNORE")
    result = conn.execute(stmt)
    return result.rowcount


class AutoInfracaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: AutoInfracaoModel | None) -> AutoInfracao | None:
        if model is None:
            return None
        return AutoInfracao(**model.__dict__)

    def _to_model(self, entity: AutoInfracao) -> AutoInfracaoModel:
        return AutoInfracaoModel(**entity.as_dict())

    def get_infracoes(self, date: Any, ai: Any) -> List[AutoInfracao]:
        query = self.db.query(AutoInfracaoModel)
        if ai is not None:
            query = query.filter(AutoInfracaoModel.NUM_AI.like(f"%{ai}%"))
        if date is not None:
            query = query.filter(AutoInfracaoModel.DAT_EMIS_NOTF >= date)
        models = query.limit(200).all()
        return [self._to_domain(m) for m in models if m is not None]

    def check_presence(self, values: List[str]) -> Tuple[int, int, List[str]]:
        existing = self.db.query(AutoInfracaoModel.NUM_AI).filter(AutoInfracaoModel.NUM_AI.in_(values)).all()
        existing_set = {r[0] for r in existing}
        
        rows_counter = len(existing_set)
        counter = len(values)
        rows_not_present = [v for v in values if v not in existing_set]
        
        return rows_counter, counter, rows_not_present

    def insert_bulk_df(self, data_frame: Any, insert_ignore_func: Any = None) -> int:
        if insert_ignore_func is None:
            insert_ignore_func = insert_ignore_mysql
        conn = self.db.connection()
        count = data_frame.to_sql('auto_infracao', conn, if_exists='append', index=False, method=insert_ignore_func)
        return count

    def insert_bulk_rows(self, rows: List[Dict[str, Any]], ignore: bool = False) -> int:
        counter = 0
        for row in rows:
            if ignore:
                stmt = insert(AutoInfracaoModel).values(row).prefix_with("IGNORE")
                result: Any = self.db.execute(stmt)
                rowcount = getattr(result, "rowcount", 0)
                if rowcount > 0:
                    counter += 1
            else:
                ai_model = AutoInfracaoModel(**row)
                self.db.add(ai_model)
                counter += 1
        return counter
