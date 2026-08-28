from warnings import deprecated
from typing import List, Tuple, Any, Dict
import pandas as pd

from utils.logger import logger
from repositories.database import get_db
from repositories.autoinfracao_repository import AutoInfracaoRepository
from exceptions.CustomExceptions import ErrReadingFile
from services.parsers import parse_csv_infracoes, parse_xls_infracoes


class AutoInfracaoService:
    """Serviço de domínio para casos de uso de Autos de Infração."""

    @staticmethod
    def get_infracoes(date: Any, ai: Any) -> List[Dict[str, Any]]:
        """Recupera os autos de infração."""
        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            infracoes = repo.get_infracoes(date, ai)
            return [inf.as_dict() for inf in infracoes]

    @staticmethod
    def check_infracoes(csv: Any) -> Tuple[int, int, List[str]]:
        """Realiza a verificação dos autos de infração no banco de dados."""
        try:
            data_frame = pd.read_csv(csv, header=0, delimiter=';')
            values = data_frame['NUM_AI'].unique().tolist()
        except Exception as e:
            raise ErrReadingFile(f"Erro ao ler o arquivo CSV. {e}", 500)

        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            rows_counter, counter, rows_not_present = repo.check_presence(values)
            return rows_counter, counter, rows_not_present

    @staticmethod
    def insert_infracoes_csv(csv: Any) -> int:
        """Insere os autos de infração no banco de dados a partir de um arquivo CSV."""
        data_frame = parse_csv_infracoes(csv)
        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            count = repo.insert_bulk_df(data_frame)
            logger.info(f"INFO: {count} autos processados. FILE: {csv}")
            return count

    @staticmethod
    def insert_infracoes_xls(xls: Any, ignore: bool) -> int:
        """Insere os autos de infração no banco de dados a partir de um arquivo XLS."""
        data_frame = parse_xls_infracoes(xls)
        rows_to_insert = [row.to_dict() for _, row in data_frame.iterrows()]
        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            count = repo.insert_bulk_rows(rows_to_insert, ignore=ignore)
            return count

    @staticmethod
    @deprecated("use insert_infracoes_xls instead")
    def insert_cmn_infracoes_xls(xls: Any) -> int:
        """Insere os autos de infração no banco de dados a partir de um arquivo XLS."""
        data_frame = parse_xls_infracoes(xls)
        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            count = repo.insert_bulk_df(data_frame)
            logger.info(f"INFO: {count} autos processados - {xls}")
            return count
