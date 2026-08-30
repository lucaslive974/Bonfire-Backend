from sqlalchemy import Boolean, Column, DateTime, Integer, String

from repositories.models.Base import Base


class VeiculoModel(Base):
    __tablename__ = "veiculos"

    NUM_VEIC = Column(Integer, primary_key=True)
    IDN_PLAC_VEIC = Column(String(10), unique=True, nullable=True)
    VEIC_ATIV_EMPR = Column(Boolean, nullable=False, default=True)
    DAT_BAIX = Column(DateTime, nullable=True)

    def __init__(
        self,
        NUM_VEIC=None,
        IDN_PLAC_VEIC=None,
        VEIC_ATIV_EMPR=True,
        DAT_BAIX=None,
    ):
        self.NUM_VEIC = NUM_VEIC
        self.IDN_PLAC_VEIC = IDN_PLAC_VEIC
        self.VEIC_ATIV_EMPR = VEIC_ATIV_EMPR
        self.DAT_BAIX = DAT_BAIX
