from typing import Any, Dict, List, Tuple

import pandas as pd

from exceptions.CustomExceptions import ErrReadingFile
from repositories.autoinfracao_repository import AutoInfracaoRepository
from repositories.database import get_db


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
            data_frame = pd.read_csv(csv, header=0, delimiter=";")
            values = data_frame["NUM_AI"].unique().tolist()
        except Exception as e:
            raise ErrReadingFile(f"Erro ao ler o arquivo CSV. {e}", 500)

        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            rows_counter, counter, rows_not_present = repo.check_presence(values)
            return rows_counter, counter, rows_not_present
