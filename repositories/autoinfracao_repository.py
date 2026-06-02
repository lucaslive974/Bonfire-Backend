from typing import List, Tuple, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import insert
from classes.AutoInfracao import AutoInfracao

class AutoInfracaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_infracoes(self, date: Any, ai: Any) -> List[AutoInfracao]:
        query = self.db.query(AutoInfracao)
        if ai is not None:
            query = query.filter(AutoInfracao.NUM_AI.like(f"%{ai}%"))
        if date is not None:
            query = query.filter(AutoInfracao.DAT_EMIS_NOTF >= date)
        return query.limit(200).all()

    def check_presence(self, values: List[str]) -> Tuple[int, int, List[str]]:
        # Efficiently queries presence using the IN clause
        existing = self.db.query(AutoInfracao.NUM_AI).filter(AutoInfracao.NUM_AI.in_(values)).all()
        existing_set = {r[0] for r in existing}
        
        rows_counter = len(existing_set)
        counter = len(values)
        rows_not_present = [v for v in values if v not in existing_set]
        
        return rows_counter, counter, rows_not_present

    def insert_bulk_df(self, data_frame: Any, insert_ignore_func: Any) -> int:
        conn = self.db.connection()
        count = data_frame.to_sql('auto_infracao', conn, if_exists='append', index=False, method=insert_ignore_func)
        return count

    def insert_bulk_rows(self, rows: List[Dict[str, Any]], ignore: bool = False) -> int:
        counter = 0
        for row in rows:
            if ignore:
                stmt = insert(AutoInfracao).values(row).prefix_with("IGNORE")
                result: Any = self.db.execute(stmt)
                rowcount = getattr(result, "rowcount", 0)
                if rowcount > 0:
                    counter += 1
            else:
                ai = AutoInfracao(**row)
                self.db.add(ai)
                counter += 1
        return counter
