from datetime import date, datetime
from typing import Any, Dict, Iterator, Tuple


class SerializableMixin:
    """Mixin para fornecer serialização pythônica rica e suporte a dict(instancia)."""

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Permite a conversão direta de uma instância para dict via dict(instancia)."""
        for key, value in self.as_dict().items():
            yield key, value

    def as_dict(self) -> Dict[str, Any]:
        """Converte os atributos da instância em um dicionário, formatando datas para ISO format."""
        result: Dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if isinstance(value, (datetime, date)):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

    def to_dict(self) -> Dict[str, Any]:
        """Método de conveniência/compatibilidade delegando para as_dict."""
        return self.as_dict()
