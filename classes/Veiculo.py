from datetime import datetime
from typing import Any, Dict, Iterator, Tuple

from exceptions.CustomExceptions import ErrUpdateData


class Veiculo:
    """Pure domain entity for Vehicle."""

    def __init__(
        self,
        NUM_VEIC: int | str | None = None,
        IDN_PLAC_VEIC: str | None = None,
        VEIC_ATIV_EMPR: bool | None = None,
        DAT_BAIX: datetime | str | None = None,
        **kwargs: Any,
    ):
        self._vehicle_number: int | None = None
        self._license_plate: str | None = None
        self._is_active: bool | None = None
        self._deregistration_date: datetime | None = None

        raw_num = NUM_VEIC if NUM_VEIC is not None else kwargs.get("vehicle_number")
        if raw_num is not None:
            self.set_vehicle_number(raw_num)

        raw_plate = (
            IDN_PLAC_VEIC if IDN_PLAC_VEIC is not None else kwargs.get("license_plate")
        )
        if raw_plate is not None:
            self.set_license_plate(raw_plate)

        raw_date = (
            DAT_BAIX if DAT_BAIX is not None else kwargs.get("deregistration_date")
        )
        if raw_date is not None:
            self.set_deregistration_date(raw_date)

        raw_active = (
            VEIC_ATIV_EMPR if VEIC_ATIV_EMPR is not None else kwargs.get("active")
        )
        if raw_active is not None:
            self._is_active = bool(raw_active)

    # --- Getters & Setters ---

    def get_vehicle_number(self) -> int | None:
        """Return vehicle number."""
        return self._vehicle_number

    def set_vehicle_number(self, value: int | str | None) -> None:
        """Set vehicle number."""
        self._vehicle_number = int(value) if value is not None else None

    def get_license_plate(self) -> str | None:
        """Return license plate."""
        return self._license_plate

    def set_license_plate(self, value: str | None) -> None:
        """Set license plate."""
        self._license_plate = str(value) if value is not None else None

    def is_active(self) -> bool:
        """Check if vehicle is active in the company."""
        return bool(self._is_active)

    def activate(self) -> None:
        """Reactivate vehicle and clear deregistration date."""
        self._is_active = True
        self._deregistration_date = None

    def deactivate(self, deregistration_date: datetime | str | None = None) -> None:
        """Deactivate vehicle and record deregistration date."""
        if self._is_active is False:
            raise ErrUpdateData(
                f"Veículo {self._vehicle_number} já se encontra baixado",
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

    # --- Properties and Aliases ---

    vehicle_number = property(get_vehicle_number, set_vehicle_number)
    NUM_VEIC = vehicle_number

    license_plate = property(get_license_plate, set_license_plate)
    IDN_PLAC_VEIC = license_plate

    def _set_active_prop(self, value: bool) -> None:
        if value:
            self.activate()
        else:
            self.deactivate()

    active = property(lambda self: self._is_active, _set_active_prop)
    VEIC_ATIV_EMPR = active

    deregistration_date = property(get_deregistration_date, set_deregistration_date)
    DAT_BAIX = deregistration_date

    def to_dict(self) -> Dict[str, Any]:
        """Serialize entity to dictionary matching database schema."""
        return {
            "NUM_VEIC": self._vehicle_number,
            "IDN_PLAC_VEIC": self._license_plate,
            "VEIC_ATIV_EMPR": self._is_active,
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
