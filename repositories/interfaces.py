from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class IAutoInfracaoRepository(ABC):
    @abstractmethod
    def get_infracoes(self, date: Any, ai: Any) -> List[Any]:
        pass

    @abstractmethod
    def check_presence(self, values: List[str]) -> Tuple[int, int, List[str]]:
        pass

    @abstractmethod
    def insert_bulk_df(self, data_frame: Any, insert_ignore_func: Any = None) -> int:
        pass

    @abstractmethod
    def insert_bulk_rows(self, rows: List[Dict[str, Any]], ignore: bool = False) -> int:
        pass


class IVeiculoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    def get_by_id(self, num_veic: int) -> Any:
        pass

    @abstractmethod
    def insert(self, veiculo: Any) -> bool:
        pass

    @abstractmethod
    def insert_bulk(self, veiculos_data: List[Dict[str, Any]]) -> int:
        pass

    @abstractmethod
    def update_bulk(self, veiculos_data: List[Dict[str, Any]]) -> int:
        pass

    @abstractmethod
    def delete(self, num_veic: int) -> int:
        pass


class ILinhaRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    def get_by_id(self, cod_linh: str) -> Any:
        pass

    @abstractmethod
    def insert_bulk(self, linhas_data: List[Dict[str, Any]]) -> int:
        pass

    @abstractmethod
    def update_bulk(self, linhas_data: List[Dict[str, Any]]) -> int:
        pass

    @abstractmethod
    def delete(self, cod_linh: str) -> int:
        pass


class IConsorcioRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    def get_by_id(self, id_consorcio: int) -> Any:
        pass

    @abstractmethod
    def insert_bulk(self, consorcios_data: List[Dict[str, Any]]) -> int:
        pass

    @abstractmethod
    def update_bulk(self, consorcios_data: List[Dict[str, Any]]) -> int:
        pass

    @abstractmethod
    def delete(self, id_consorcio: int) -> int:
        pass


class IRecursoRepository(ABC):
    @abstractmethod
    def get_primeira_instancia(self, date: Any, ata: Any) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_segunda_instancia(self, date: Any) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def insert_primeira_instancia(self, rows: List[Dict[str, Any]]) -> int:
        pass

    @abstractmethod
    def insert_segunda_instancia(self, rows: List[Dict[str, Any]]) -> int:
        pass


class IRepositorySession(ABC):
    @abstractmethod
    def __enter__(self) -> "IRepositorySession":
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def get_autoinfracao_repository(self) -> IAutoInfracaoRepository:
        pass

    @abstractmethod
    def get_veiculo_repository(self) -> IVeiculoRepository:
        pass

    @abstractmethod
    def get_linha_repository(self) -> ILinhaRepository:
        pass

    @abstractmethod
    def get_consorcio_repository(self) -> IConsorcioRepository:
        pass

    @abstractmethod
    def get_recurso_repository(self) -> IRecursoRepository:
        pass


class IRepositoryManager(ABC):
    @abstractmethod
    def session(self) -> IRepositorySession:
        pass

    @abstractmethod
    def check_connection(self) -> None:
        pass
