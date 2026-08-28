from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from repositories.models.Base import Base


class LinhaModel(Base):
    __tablename__ = 'linha'

    COD_LINH = Column(String(10), primary_key=True)
    ID_OPERADORA = Column(Integer, ForeignKey('operadora.ID'), nullable=True)
    COMPARTILHADA = Column(Boolean, nullable=False, default=False)
    LINH_ATIV_EMPR = Column(Boolean, nullable=False, default=True)
    DAT_BAIX = Column(DateTime, nullable=True)

    # Relationship
    operadora = relationship("OperadoraModel", backref="linhas")

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
