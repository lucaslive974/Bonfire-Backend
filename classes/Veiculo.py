from sqlalchemy import Column, Integer, String, Boolean
from classes.Base import Base

class Veiculo(Base):
    __tablename__ = 'veiculos'

    NUM_VEIC = Column(Integer, primary_key=True)
    IDN_PLAC_VEIC = Column(String(10), unique=True, nullable=True)
    VEIC_ATIV_EMPR = Column(Boolean, nullable=False, default=True)

    def __init__(self, num_veiculo=None, placa=None, NUM_VEIC=None, IDN_PLAC_VEIC=None, VEIC_ATIV_EMPR=True):
        # Support both current constructor style and ORM initialization
        self.NUM_VEIC = NUM_VEIC or num_veiculo
        self.IDN_PLAC_VEIC = IDN_PLAC_VEIC or placa
        self.VEIC_ATIV_EMPR = VEIC_ATIV_EMPR

    def to_dict(self) -> dict:
        return {
            'NUM_VEIC': self.NUM_VEIC,
            'IDN_PLAC_VEIC': self.IDN_PLAC_VEIC,
            'VEIC_ATIV_EMPR': self.VEIC_ATIV_EMPR
        }