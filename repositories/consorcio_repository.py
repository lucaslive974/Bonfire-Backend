from typing import List
from sqlalchemy.orm import Session
from classes.Operadora import Operadora

class ConsorcioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Operadora]:
        return self.db.query(Operadora).all()
