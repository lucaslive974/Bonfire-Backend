from sqlalchemy import Column, Integer, String, Boolean, DateTime
from classes.Base import Base


class Veiculo(Base):
    __tablename__ = 'veiculos'

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

    def to_dict(self) -> dict:
        return {
            'NUM_VEIC': self.NUM_VEIC,
            'IDN_PLAC_VEIC': self.IDN_PLAC_VEIC,
            'VEIC_ATIV_EMPR': self.VEIC_ATIV_EMPR,
            'DAT_BAIX': self.DAT_BAIX.isoformat() if self.DAT_BAIX is not None else None,
        }