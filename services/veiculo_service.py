from typing import Any, Dict, List

from exceptions.CustomExceptions import ErrUpdateData
from repositories.interfaces import IRepositoryManager


class VeiculoService:
    """Serviço de domínio para casos de uso de Veículos."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def get_veiculos(self) -> List[Dict[str, Any]]:
        """Recupera os veículos do banco de dados."""
        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            veiculos = repo.get_all()
            return [v.as_dict() for v in veiculos]

    def insert_veiculos(self, veiculos_data: List[Dict[str, Any]]) -> int:
        """Insere uma lista de veículos no banco de dados."""
        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            count = repo.insert_bulk(veiculos_data)
            return count

    def update_veiculos(self, veiculos_data: List[Dict[str, Any]]) -> int:
        """Atualiza uma lista de veículos no banco de dados."""
        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            count = repo.update_bulk(veiculos_data)
            return count

    def delete_veiculos(self, num_veic: str | int) -> int:
        """Deleta um veículo no banco de dados pelo seu número."""
        try:
            num_veic_int = int(num_veic)
        except ValueError:
            raise ErrUpdateData("Número do veículo inválido", 400)

        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            count = repo.delete(num_veic_int)
            return count
