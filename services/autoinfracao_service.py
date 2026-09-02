from typing import Any, Dict, List, Tuple

import pandas as pd

from exceptions.CustomExceptions import ErrReadingFile
from repositories.interfaces import IRepositoryManager


class AutoInfracaoService:
    """Serviço de domínio para casos de uso de Autos de Infração."""

    def __init__(self, db_manager: IRepositoryManager, parser_factory=None):
        self._parser_factory = parser_factory
        self._db_manager = db_manager

    def get_infracoes(self, date: Any, ai: Any) -> List[Dict[str, Any]]:
        """Recupera os autos de infração."""
        with self._db_manager.session() as session:
            repo = session.get_autoinfracao_repository()
            infracoes = repo.get_infracoes(date, ai)
            return [inf.as_dict() for inf in infracoes]

    def check_infracoes(self, csv: Any) -> Tuple[int, int, List[str]]:
        """Realiza a verificação dos autos de infração no banco de dados."""
        try:
            data_frame = pd.read_csv(csv, header=0, delimiter=";")
            values = data_frame["NUM_AI"].unique().tolist()
        except Exception as e:
            raise ErrReadingFile(f"Erro ao ler o arquivo CSV. {e}", 500)

        with self._db_manager.session() as session:
            repo = session.get_autoinfracao_repository()
            rows_counter, counter, rows_not_present = repo.check_presence(values)
            return rows_counter, counter, rows_not_present

    def extract_csv(self, file_stream: Any, ignore: bool = False) -> dict:
        if not self._parser_factory:
            raise RuntimeError("ParserFactory not injected")
        extractor = self._parser_factory.create_infracoes_csv_parser(ignore=ignore)
        return extractor.extract(file_stream)

    def extract_xls(self, file_stream: Any, ignore: bool = False) -> dict:
        if not self._parser_factory:
            raise RuntimeError("ParserFactory not injected")
        extractor = self._parser_factory.create_infracoes_xls_parser(ignore=ignore)
        return extractor.extract(file_stream)
