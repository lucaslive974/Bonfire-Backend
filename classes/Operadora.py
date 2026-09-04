from typing import Any, Dict, Iterator, Tuple


class Operadora:
    """Pure domain entity for Operadora (Consórcio)."""

    def __init__(
        self,
        ID: int | str | None = None,
        NOME: str | None = None,
        CONCESSIONARIA: str | None = None,
        **kwargs: Any,
    ):
        self._id: int | None = None
        self._name: str | None = None
        self._concessionaire: str | None = None

        raw_id = ID if ID is not None else kwargs.get("id")
        if raw_id is not None:
            self.set_id(raw_id)

        raw_name = NOME or kwargs.get("name")
        if raw_name is not None:
            self.set_name(raw_name)

        raw_conc = CONCESSIONARIA or kwargs.get("concessionaire")
        if raw_conc is not None:
            self.set_concessionaire(raw_conc)

    # --- Getters & Setters ---

    def get_id(self) -> int | None:
        return self._id

    def set_id(self, value: int | str | None) -> None:
        self._id = int(value) if value is not None else None

    def get_name(self) -> str | None:
        return self._name

    def set_name(self, value: str | None) -> None:
        self._name = str(value) if value is not None else None

    def get_concessionaire(self) -> str | None:
        return self._concessionaire

    def set_concessionaire(self, value: str | None) -> None:
        self._concessionaire = str(value) if value is not None else None

    # --- Properties ---

    id = property(get_id, set_id)
    ID = id

    name = property(get_name, set_name)
    NOME = name

    concessionaire = property(get_concessionaire, set_concessionaire)
    CONCESSIONARIA = concessionaire

    def to_dict(self) -> Dict[str, Any]:
        """Convert domain entity to dictionary representation."""
        return {
            "ID": self._id,
            "NOME": self._name,
            "CONCESSIONARIA": self._concessionaire,
        }

    as_dict = to_dict

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Allow dict(instance) conversion."""
        yield from self.to_dict().items()
