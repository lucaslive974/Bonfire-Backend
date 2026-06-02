from sqlalchemy import Column, Integer, String
from classes.Base import Base

class Operadora(Base):
    __tablename__ = 'operadora'

    ID = Column(Integer, primary_key=True)
    NOME = Column(String(100), nullable=True)
    CONCESSIONARIA = Column(String(100), nullable=True)

    def __init__(self, ID=None, NOME=None, CONCESSIONARIA=None, nome=None, concessionaria=None):
        # Support both current constructor style and ORM initialization
        self.ID = ID
        self.NOME = NOME or nome
        self.CONCESSIONARIA = CONCESSIONARIA or concessionaria

    def to_dict(self) -> dict:
        return {
            'ID': self.ID,
            'NOME': self.NOME,
            'CONCESSIONARIA': self.CONCESSIONARIA
        }