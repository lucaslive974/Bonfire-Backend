from datetime import datetime
from typing import Any, Dict

from classes.Mixins import SerializableMixin
from exceptions.CustomExceptions import ErrUpdateData


class Veiculo(SerializableMixin):
    """Entidade pura de domínio para Veículo."""

    def __init__(
        self,
        NUM_VEIC: int | str | None = None,
        IDN_PLAC_VEIC: str | None = None,
        VEIC_ATIV_EMPR: bool = True,
        DAT_BAIX: datetime | str | None = None,
    ):
        self.NUM_VEIC = int(NUM_VEIC) if NUM_VEIC is not None else None
        self.IDN_PLAC_VEIC = str(IDN_PLAC_VEIC) if IDN_PLAC_VEIC is not None else None
        self.VEIC_ATIV_EMPR = bool(VEIC_ATIV_EMPR)

        if isinstance(DAT_BAIX, str):
            try:
                self.DAT_BAIX: datetime | None = datetime.fromisoformat(DAT_BAIX)
            except ValueError:
                self.DAT_BAIX = None
        else:
            self.DAT_BAIX = DAT_BAIX

    def esta_ativo(self) -> bool:
        """Verifica se o veículo está ativo na empresa."""
        return bool(self.VEIC_ATIV_EMPR)

    def desativar(self, dat_baix: datetime | str | None = None) -> None:
        """Desativa o veículo e registra a data de baixa."""
        if not self.VEIC_ATIV_EMPR:
            raise ErrUpdateData(
                f"Veículo {self.NUM_VEIC} já se encontra baixado",
                400,
            )
        self.VEIC_ATIV_EMPR = False
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
        """Reativa o veículo e remove a data de baixa."""
        self.VEIC_ATIV_EMPR = True
        self.DAT_BAIX = None

    def atualizar(self, dados: Dict[str, Any]) -> None:
        """Atualiza os campos do veículo encapsulando regras de negócio de ativação/desativação."""
        if "IDN_PLAC_VEIC" in dados:
            val = dados["IDN_PLAC_VEIC"]
            self.IDN_PLAC_VEIC = str(val) if val else None
        if "VEIC_ATIV_EMPR" in dados:
            novo_status = bool(dados["VEIC_ATIV_EMPR"])
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
