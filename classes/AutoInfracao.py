from sqlalchemy import Column, String, Integer, DateTime, Float
from classes.Base import Base

class AutoInfracao(Base):
    __tablename__ = 'auto_infracao'

    NUM_AI = Column(String(10), primary_key=True)
    NUM_NOTF = Column(String(10), unique=True, nullable=True)
    TIP_PENL = Column(String(20), nullable=True)
    NOM_CONC = Column(String(100), nullable=True)
    COD_LINH = Column(String(10), nullable=True)
    NOM_LINH = Column(String(100), nullable=True)
    NUM_VEIC = Column(Integer, nullable=True)
    IDN_PLAC_VEIC = Column(String(10), nullable=True)
    DAT_OCOR_INFR = Column(DateTime, nullable=True)
    DES_LOCA = Column(String(255), nullable=True)
    COD_IRRG_FISC = Column(Integer, nullable=True)
    ARTIGO = Column(String(20), nullable=True)
    DES_OBSE = Column(String(255), nullable=True)
    NUM_MATR_FISC = Column(Integer, nullable=True)
    QTE_PONT = Column(Integer, nullable=True)
    DAT_EMIS_NOTF = Column(DateTime, nullable=True)
    DAT_LIMT_RECU = Column(DateTime, nullable=True)
    VAL_INFR = Column(Float, nullable=True)
    DAT_CANC = Column(DateTime, nullable=True)

    def __init__(self, **kwargs):
        # Support kwargs initialization
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        return {
            'NUM_NOTF': self.NUM_NOTF,
            'TIP_PENL': self.TIP_PENL,
            'NUM_AI': self.NUM_AI,
            'NOM_CONC': self.NOM_CONC,
            'COD_LINH': self.COD_LINH,
            'NOM_LINH': self.NOM_LINH,
            'NUM_VEIC': self.NUM_VEIC,
            'IDN_PLAC_VEIC': self.IDN_PLAC_VEIC,
            'DAT_OCOR_INFR': self.DAT_OCOR_INFR.isoformat() if self.DAT_OCOR_INFR is not None else None,
            'DES_LOCA': self.DES_LOCA,
            'COD_IRRG_FISC': self.COD_IRRG_FISC,
            'ARTIGO': self.ARTIGO,
            'DES_OBSE': self.DES_OBSE,
            'NUM_MATR_FISC': self.NUM_MATR_FISC,
            'QTE_PONT': self.QTE_PONT,
            'DAT_EMIS_NOTF': self.DAT_EMIS_NOTF.isoformat() if self.DAT_EMIS_NOTF is not None else None,
            'DAT_LIMT_RECU': self.DAT_LIMT_RECU.isoformat() if self.DAT_LIMT_RECU is not None else None,
            'VAL_INFR': self.VAL_INFR,
            'DAT_CANC': self.DAT_CANC.isoformat() if self.DAT_CANC is not None else None
        }
