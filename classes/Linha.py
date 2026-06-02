from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from classes.Base import Base

class Linha(Base):
    __tablename__ = 'linha'

    COD_LINH = Column(String(10), primary_key=True)
    ID_OPERADORA = Column(Integer, ForeignKey('operadora.ID'), nullable=True)
    COMPARTILHADA = Column(Boolean, nullable=False, default=False)
    LINH_ATIV_EMPR = Column(Boolean, nullable=False, default=True)

    # Relationship
    operadora = relationship("Operadora", backref="linhas")

    def __init__(self, num_linha=None, id_operadora=None, compartilhada=False, COD_LINH=None, ID_OPERADORA=None, COMPARTILHADA=False, LINH_ATIV_EMPR=True):
        self.COD_LINH = COD_LINH or num_linha
        self.ID_OPERADORA = ID_OPERADORA or id_operadora
        self.COMPARTILHADA = COMPARTILHADA or compartilhada
        self.LINH_ATIV_EMPR = LINH_ATIV_EMPR

    def to_dict(self) -> dict:
        return {
            'COD_LINH': self.COD_LINH,
            'ID_OPERADORA': self.ID_OPERADORA,
            'COMPARTILHADA': self.COMPARTILHADA,
            'LINH_ATIV_EMPR': self.LINH_ATIV_EMPR
        }