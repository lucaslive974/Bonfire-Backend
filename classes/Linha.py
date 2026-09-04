from datetime import datetime
from typing import Any, Dict, Iterator, Tuple

from exceptions.CustomExceptions import ErrUpdateData


class Linha:
    """Pure domain entity for Bus Line."""

    def __init__(
        self,
        COD_LINH: str | None = None,
        ID_OPERADORA: int | None = None,
        COMPARTILHADA: bool | None = None,
        LINH_ATIV_EMPR: bool | None = None,
        DAT_BAIX: datetime | str | None = None,
        **kwargs: Any,
    ):
        self._line_code: str | None = None
        self._operator_id: int | None = None
        self._is_shared: bool | None = None
        self._is_active: bool | None = None
        self._deregistration_date: datetime | None = None

        raw_code = COD_LINH if COD_LINH is not None else kwargs.get("line_code")
        if raw_code is not None:
            self.set_line_code(raw_code)

        raw_op = ID_OPERADORA if ID_OPERADORA is not None else kwargs.get("operator_id")
        if raw_op is not None:
            self.set_operator_id(raw_op)

        raw_shared = (
            COMPARTILHADA if COMPARTILHADA is not None else kwargs.get("shared")
        )
        if raw_shared is not None:
            self.set_shared(raw_shared)

        raw_date = (
            DAT_BAIX if DAT_BAIX is not None else kwargs.get("deregistration_date")
        )
        if raw_date is not None:
            self.set_deregistration_date(raw_date)

        raw_active = (
            LINH_ATIV_EMPR if LINH_ATIV_EMPR is not None else kwargs.get("active")
        )
        if raw_active is not None:
            self._is_active = bool(raw_active)

    # --- Getters & Setters ---

    def get_line_code(self) -> str | None:
        """Return bus line code."""
        return self._line_code

    def set_line_code(self, value: str | None) -> None:
        """Set bus line code."""
        self._line_code = str(value) if value is not None else None

    def get_operator_id(self) -> int | None:
        """Return operator ID."""
        return self._operator_id

    def set_operator_id(self, value: int | str | None) -> None:
        """Set operator ID."""
        self._operator_id = int(value) if value is not None else None

    def is_shared(self) -> bool:
        """Check if bus line is shared."""
        return bool(self._is_shared)

    def set_shared(self, value: bool | None) -> None:
        """Set shared status."""
        self._is_shared = bool(value) if value is not None else None

    get_shared = is_shared

    def is_active(self) -> bool:
        """Check if line is active in the company."""
        return bool(self._is_active)

    def activate(self) -> None:
        """Reactivate line and clear deregistration date."""
        self._is_active = True
        self._deregistration_date = None

    def deactivate(self, deregistration_date: datetime | str | None = None) -> None:
        """Deactivate line and record deregistration date."""
        if self._is_active is False:
            raise ErrUpdateData(
                f"Linha {self._line_code} já se encontra baixada",
                400,
            )
        self._is_active = False
        if isinstance(deregistration_date, str):
            try:
                self._deregistration_date = datetime.fromisoformat(deregistration_date)
            except ValueError:
                self._deregistration_date = datetime.now()
        elif isinstance(deregistration_date, datetime):
            self._deregistration_date = deregistration_date
        else:
            self._deregistration_date = datetime.now()

    def get_deregistration_date(self) -> datetime | None:
        """Return deregistration date."""
        return self._deregistration_date

    def set_deregistration_date(self, value: datetime | str | None) -> None:
        """Set deregistration date."""
        if isinstance(value, str):
            try:
                self._deregistration_date = datetime.fromisoformat(value)
            except ValueError:
                self._deregistration_date = None
        elif isinstance(value, datetime):
            self._deregistration_date = value
        else:
            self._deregistration_date = None

    # --- Properties ---

    line_code = property(get_line_code, set_line_code)
    COD_LINH = line_code

    operator_id = property(get_operator_id, set_operator_id)
    ID_OPERADORA = operator_id

    shared = property(is_shared, set_shared)
    COMPARTILHADA = shared

    def _set_active_prop(self, value: bool) -> None:
        if value:
            self.activate()
        else:
            self.deactivate()

    active = property(lambda self: self._is_active, _set_active_prop)
    LINH_ATIV_EMPR = active

    deregistration_date = property(get_deregistration_date, set_deregistration_date)
    DAT_BAIX = deregistration_date

    def to_dict(self) -> Dict[str, Any]:
        """Serialize entity to dictionary matching database schema."""
        return {
            "COD_LINH": self._line_code,
            "ID_OPERADORA": self._operator_id,
            "COMPARTILHADA": self.is_shared(),
            "LINH_ATIV_EMPR": self.is_active(),
            "DAT_BAIX": (
                self._deregistration_date.isoformat()
                if self._deregistration_date is not None
                else None
            ),
        }

    as_dict = to_dict

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Allow dict(instance) conversion."""
        yield from self.to_dict().items()
