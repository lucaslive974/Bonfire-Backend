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

class Recurso:
    """Legacy compatibility class for parsing DOCX and older handlers"""
    def __init__(self, NUM_ATA, NUM_RECURSO, NUM_AI, NOM_CONC, RESULTADO, DAT_PUBL):
        self.recurso = NUM_RECURSO
        self.ata = NUM_ATA
        self.numAuto = NUM_AI
        self.recorrente = NOM_CONC
        self.resultado = RESULTADO
        self.dat_publ = DAT_PUBL

    def toDict(self):
        return {
            'NUM_RECURSO' : self.recurso,
            'NUM_ATA': self.ata,
            'NUM_AI' : self.numAuto,
            'NOM_CONC' : self.recorrente,
            'RESULTADO' : self.resultado,
            'DAT_PUBL' : self.dat_publ
        }