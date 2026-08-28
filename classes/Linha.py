from datetime import datetime
from typing import Any, Dict
from classes.Mixins import SerializableMixin
from exceptions.CustomExceptions import ErrUpdateData


class Linha(SerializableMixin):
    """Entidade pura de domínio para Linha."""

    def __init__(
        self,
        COD_LINH: str | None = None,
        ID_OPERADORA: int | None = None,
        COMPARTILHADA: bool = False,
        LINH_ATIV_EMPR: bool = True,
        DAT_BAIX: datetime | str | None = None,
    ):
        self.COD_LINH = str(COD_LINH) if COD_LINH is not None else None
        self.ID_OPERADORA = int(ID_OPERADORA) if ID_OPERADORA is not None else None
        self.COMPARTILHADA = bool(COMPARTILHADA)
        self.LINH_ATIV_EMPR = bool(LINH_ATIV_EMPR)

        if isinstance(DAT_BAIX, str):
            try:
                self.DAT_BAIX: datetime | None = datetime.fromisoformat(DAT_BAIX)
            except ValueError:
                self.DAT_BAIX = None
        else:
            self.DAT_BAIX = DAT_BAIX

    def esta_ativa(self) -> bool:
        """Verifica se a linha está ativa na empresa."""
        return bool(self.LINH_ATIV_EMPR)

    def desativar(self, dat_baix: datetime | str | None = None) -> None:
        """Desativa a linha e registra a data de baixa."""
        if not self.LINH_ATIV_EMPR:
            raise ErrUpdateData(
                f"Linha {self.COD_LINH} já se encontra baixada",
                400,
            )
        self.LINH_ATIV_EMPR = False
        if isinstance(dat_baix, str):
            try:
                self.DAT_BAIX = datetime.fromisoformat(dat_baix)
            except ValueError:
                self.DAT_BAIX = datetime.now()
        elif isinstance(dat_baix, datetime):
            self.DAT_BAIX = dat_baix
        else:
            self.DAT_BAIX = datetime.now()

    def ativar(self) -> None:
        """Reativa a linha e remove a data de baixa."""
        self.LINH_ATIV_EMPR = True
        self.DAT_BAIX = None

    def atualizar(self, dados: Dict[str, Any]) -> None:
        """Atualiza os campos da linha encapsulando regras de negócio de ativação/desativação."""
        if "COMPARTILHADA" in dados:
            self.COMPARTILHADA = bool(dados["COMPARTILHADA"])
        if "ID_OPERADORA" in dados:
            val = dados["ID_OPERADORA"]
            self.ID_OPERADORA = int(val) if val is not None else None
        if "LINH_ATIV_EMPR" in dados:
            novo_status = bool(dados["LINH_ATIV_EMPR"])
            if not novo_status:
                self.desativar(dados.get("DAT_BAIX"))
            else:
                self.ativar()
        elif "DAT_BAIX" in dados:
            dat_baix = dados["DAT_BAIX"]
            if isinstance(dat_baix, str):
                try:
                    self.DAT_BAIX = datetime.fromisoformat(dat_baix)
                except ValueError:
                    self.DAT_BAIX = None
            elif isinstance(dat_baix, datetime):
                self.DAT_BAIX = dat_baix
            else:
                self.DAT_BAIX = None
