from sqlalchemy import Column, String, Integer, DateTime, Float
from repositories.models.Base import Base


class AutoInfracaoModel(Base):
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
        for key, value in kwargs.items():
            setattr(self, key, value)
