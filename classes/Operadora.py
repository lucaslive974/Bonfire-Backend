from typing import Any, Dict

from classes.Mixins import SerializableMixin


class Operadora(SerializableMixin):
    """Entidade pura de domínio para Operadora (Consórcio)."""

    def __init__(
        self,
        ID: int | str | None = None,
        NOME: str | None = None,
        CONCESSIONARIA: str | None = None,
        nome: str | None = None,
        concessionaria: str | None = None,
    ):
        self.ID = int(ID) if ID is not None else None
        self.NOME = NOME or nome
        self.CONCESSIONARIA = CONCESSIONARIA or concessionaria

    def atualizar(self, dados: Dict[str, Any]) -> None:
        """Atualiza os campos da operadora."""
        if "NOME" in dados or "nome" in dados:
            val = dados.get("NOME") or dados.get("nome")
            self.NOME = str(val) if val is not None else None
        if "CONCESSIONARIA" in dados or "concessionaria" in dados:
            val = dados.get("CONCESSIONARIA") or dados.get("concessionaria")
            self.CONCESSIONARIA = str(val) if val is not None else None
