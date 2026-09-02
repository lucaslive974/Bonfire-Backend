from typing import Any, Dict, List

from exceptions.CustomExceptions import ErrUpdateData
from repositories.interfaces import IRepositoryManager


class ConsorcioService:
    """Serviço de domínio para casos de uso de Consórcio / Operadora."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def get_consorcios(self) -> List[Dict[str, Any]]:
        """Retorna todos os consórcios cadastrados."""
        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            consorcios = repo.get_all()
            return [c.as_dict() for c in consorcios]

    def insert_consorcios(self, consorcios_data: List[Dict[str, Any]]) -> int:
        """Insere ou atualiza (merge) uma lista de consórcios no banco de dados."""
        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            count = repo.insert_bulk(consorcios_data)
            return count

    def update_consorcios(self, consorcios_data: List[Dict[str, Any]]) -> int:
        """Atualiza uma lista de consórcios no banco de dados."""
        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            count = repo.update_bulk(consorcios_data)
            return count

    def delete_consorcio(self, id_consorcio: str | int) -> int:
        """Deleta um consórcio no banco de dados pelo seu ID."""
        try:
            id_consorcio_int = int(id_consorcio)
        except ValueError:
            raise ErrUpdateData("ID do consórcio inválido", 400)

        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            count = repo.delete(id_consorcio_int)
            return count
