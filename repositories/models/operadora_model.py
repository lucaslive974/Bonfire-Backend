from sqlalchemy import Column, Integer, String

from repositories.models.Base import Base


class OperadoraModel(Base):
    __tablename__ = "operadora"

    ID = Column(Integer, primary_key=True)
    NOME = Column(String(100), nullable=True)
    CONCESSIONARIA = Column(String(100), nullable=True)

    def __init__(
        self, ID=None, NOME=None, CONCESSIONARIA=None, nome=None, concessionaria=None
    ):
        self.ID = ID
        self.NOME = NOME or nome
        self.CONCESSIONARIA = CONCESSIONARIA or concessionaria
