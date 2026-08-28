import json
from typing import List, Dict, Any
from repositories.database import get_db
from repositories.veiculo_repository import VeiculoRepository
from exceptions.CustomExceptions import ErrUpdateData


class VeiculoService:
    """Serviço de domínio para casos de uso de Veículos."""

    @staticmethod
    def get_veiculos() -> str:
        """Recupera os veículos do banco de dados e retorna em formato JSON string."""
        with get_db() as db:
            repo = VeiculoRepository(db)
            veiculos = repo.get_all()
            data = [v.as_dict() for v in veiculos]
            return json.dumps(data)

    @staticmethod
    def insert_veiculos(veiculos_data: List[Dict[str, Any]]) -> int:
        """Insere uma lista de veículos no banco de dados."""
        with get_db() as db:
            repo = VeiculoRepository(db)
            count = repo.insert_bulk(veiculos_data)
            return count

    @staticmethod
    def update_veiculos(veiculos_data: List[Dict[str, Any]]) -> int:
        """Atualiza uma lista de veículos no banco de dados."""
        with get_db() as db:
            repo = VeiculoRepository(db)
            count = repo.update_bulk(veiculos_data)
            return count

    @staticmethod
    def delete_veiculos(num_veic: str | int) -> int:
        """Deleta um veículo no banco de dados pelo seu número."""
        try:
            num_veic_int = int(num_veic)
        except ValueError:
            raise ErrUpdateData("Número do veículo inválido", 400)

        with get_db() as db:
            repo = VeiculoRepository(db)
            count = repo.delete(num_veic_int)
            return count
