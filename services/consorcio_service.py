import json
from typing import List, Dict, Any
from repositories.database import get_db
from repositories.consorcio_repository import ConsorcioRepository
from exceptions.CustomExceptions import ErrUpdateData


class ConsorcioService:
    """Serviço de domínio para casos de uso de Consórcio / Operadora."""

    @staticmethod
    def get_consorcios() -> str:
        """Retorna todos os consórcios cadastrados em formato JSON string."""
        with get_db() as db:
            repo = ConsorcioRepository(db)
            consorcios = repo.get_all()
            data = [c.as_dict() for c in consorcios]
            return json.dumps(data)

    @staticmethod
    def insert_consorcios(consorcios_data: List[Dict[str, Any]]) -> int:
        """Insere ou atualiza (merge) uma lista de consórcios no banco de dados."""
        with get_db() as db:
            repo = ConsorcioRepository(db)
            count = repo.insert_bulk(consorcios_data)
            return count

    @staticmethod
    def update_consorcios(consorcios_data: List[Dict[str, Any]]) -> int:
        """Atualiza uma lista de consórcios no banco de dados."""
        with get_db() as db:
            repo = ConsorcioRepository(db)
            count = repo.update_bulk(consorcios_data)
            return count

    @staticmethod
    def delete_consorcio(id_consorcio: str | int) -> int:
        """Deleta um consórcio no banco de dados pelo seu ID."""
        try:
            id_consorcio_int = int(id_consorcio)
        except ValueError:
            raise ErrUpdateData("ID do consórcio inválido", 400)

        with get_db() as db:
            repo = ConsorcioRepository(db)
            count = repo.delete(id_consorcio_int)
            return count
