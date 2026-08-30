from datetime import datetime
from typing import Any

from classes.Mixins import SerializableMixin


class AutoInfracao(SerializableMixin):
    """Entidade pura de domínio para Auto de Infração."""

    def __init__(
        self,
        NUM_AI: str | None = None,
        NUM_NOTF: str | None = None,
        TIP_PENL: str | None = None,
        NOM_CONC: str | None = None,
        COD_LINH: str | None = None,
        NOM_LINH: str | None = None,
        NUM_VEIC: int | None = None,
        IDN_PLAC_VEIC: str | None = None,
        DAT_OCOR_INFR: datetime | str | None = None,
        DES_LOCA: str | None = None,
        COD_IRRG_FISC: int | None = None,
        ARTIGO: str | None = None,
        DES_OBSE: str | None = None,
        NUM_MATR_FISC: int | None = None,
        QTE_PONT: int | None = None,
        DAT_EMIS_NOTF: datetime | str | None = None,
        DAT_LIMT_RECU: datetime | str | None = None,
        VAL_INFR: float | None = None,
        DAT_CANC: datetime | str | None = None,
        **kwargs: Any,
    ):
        self.NUM_AI = NUM_AI
        self.NUM_NOTF = NUM_NOTF
        self.TIP_PENL = TIP_PENL
        self.NOM_CONC = NOM_CONC
        self.COD_LINH = COD_LINH
        self.NOM_LINH = NOM_LINH
        self.NUM_VEIC = int(NUM_VEIC) if NUM_VEIC is not None else None
        self.IDN_PLAC_VEIC = IDN_PLAC_VEIC
        self.DAT_OCOR_INFR = self._parse_datetime(DAT_OCOR_INFR)
        self.DES_LOCA = DES_LOCA
        self.COD_IRRG_FISC = int(COD_IRRG_FISC) if COD_IRRG_FISC is not None else None
        self.ARTIGO = ARTIGO
        self.DES_OBSE = DES_OBSE
        self.NUM_MATR_FISC = int(NUM_MATR_FISC) if NUM_MATR_FISC is not None else None
        self.QTE_PONT = int(QTE_PONT) if QTE_PONT is not None else None
        self.DAT_EMIS_NOTF = self._parse_datetime(DAT_EMIS_NOTF)
        self.DAT_LIMT_RECU = self._parse_datetime(DAT_LIMT_RECU)
        self.VAL_INFR = float(VAL_INFR) if VAL_INFR is not None else None
        self.DAT_CANC = self._parse_datetime(DAT_CANC)

        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    @staticmethod
    def _parse_datetime(value: datetime | str | None) -> datetime | None:
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
        return value
