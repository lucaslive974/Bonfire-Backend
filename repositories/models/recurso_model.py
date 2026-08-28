from sqlalchemy import Column, Integer, String, Boolean, Date
from repositories.models.Base import Base


class RecursoPrimeiraInstanciaModel(Base):
    __tablename__ = 'recurso_primeira_instancia'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    NUM_AI = Column(String(15), unique=True, nullable=True)
    NUM_ATA = Column(Integer, nullable=True)
    NUM_RECURSO = Column(String(15), nullable=True)
    NOM_CONC = Column(String(100), nullable=True)
    RESULTADO = Column(Boolean, nullable=False)
    DAT_PUBL = Column(Date, nullable=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class RecursoSegundaInstanciaModel(Base):
    __tablename__ = 'recurso_segunda_instancia'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    NUM_AI = Column(String(15), unique=True, nullable=True)
    NUM_RECURSO = Column(String(15), nullable=True)
    NOM_CONC = Column(String(100), nullable=True)
    RESULTADO = Column(Boolean, nullable=False)
    DAT_PUBL = Column(Date, nullable=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
