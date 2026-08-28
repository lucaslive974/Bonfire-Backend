from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from classes.Base import Base


class Linha(Base):
    __tablename__ = 'linha'

    COD_LINH = Column(String(10), primary_key=True)
    ID_OPERADORA = Column(Integer, ForeignKey('operadora.ID'), nullable=True)
    COMPARTILHADA = Column(Boolean, nullable=False, default=False)
    LINH_ATIV_EMPR = Column(Boolean, nullable=False, default=True)
    DAT_BAIX = Column(DateTime, nullable=True)

    # Relationship
    operadora = relationship("Operadora", backref="linhas")

    def __init__(
        self,
        COD_LINH=None,
        ID_OPERADORA=None,
        COMPARTILHADA=False,
        LINH_ATIV_EMPR=True,
        DAT_BAIX=None,
    ):
        self.COD_LINH = COD_LINH
        self.ID_OPERADORA = ID_OPERADORA
        self.COMPARTILHADA = COMPARTILHADA
        self.LINH_ATIV_EMPR = LINH_ATIV_EMPR
        self.DAT_BAIX = DAT_BAIX

    def to_dict(self) -> dict:
        return {
            'COD_LINH': self.COD_LINH,
            'ID_OPERADORA': self.ID_OPERADORA,
            'COMPARTILHADA': self.COMPARTILHADA,
            'LINH_ATIV_EMPR': self.LINH_ATIV_EMPR,
            'DAT_BAIX': self.DAT_BAIX.isoformat() if self.DAT_BAIX is not None else None,
        }