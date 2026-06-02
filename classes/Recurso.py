from sqlalchemy import Column, Integer, String, Boolean, Date
from classes.Base import Base

class RecursoPrimeiraInstancia(Base):
    __tablename__ = 'recurso_primeira_instancia'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    NUM_AI = Column(String(15), unique=True, nullable=True)
    NUM_ATA = Column(Integer, nullable=True)
    NUM_RECURSO = Column(String(15), nullable=True)
    NOM_CONC = Column(String(100), nullable=True)
    RESULTADO = Column(Boolean, nullable=False)
    DAT_PUBL = Column(Date, nullable=True)

    def to_dict(self) -> dict:
        return {
            'ID': self.ID,
            'NUM_AI': self.NUM_AI,
            'NUM_ATA': self.NUM_ATA,
            'NUM_RECURSO': self.NUM_RECURSO,
            'NOM_CONC': self.NOM_CONC,
            'RESULTADO': self.RESULTADO,
            'DAT_PUBL': self.DAT_PUBL.isoformat() if self.DAT_PUBL is not None else None
        }

class RecursoSegundaInstancia(Base):
    __tablename__ = 'recurso_segunda_instancia'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    NUM_AI = Column(String(15), unique=True, nullable=True)
    NUM_RECURSO = Column(String(15), nullable=True)
    NOM_CONC = Column(String(100), nullable=True)
    RESULTADO = Column(Boolean, nullable=False)
    DAT_PUBL = Column(Date, nullable=True)

    def to_dict(self) -> dict:
        return {
            'ID': self.ID,
            'NUM_AI': self.NUM_AI,
            'NUM_RECURSO': self.NUM_RECURSO,
            'NOM_CONC': self.NOM_CONC,
            'RESULTADO': self.RESULTADO,
            'DAT_PUBL': self.DAT_PUBL.isoformat() if self.DAT_PUBL is not None else None
        }