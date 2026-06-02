from warnings import deprecated
from typing import List, Tuple, Any, Dict

import numpy as np
import pandas as pd
from sqlalchemy import insert
from handlers.log import logger

from repositories.database import get_db
from repositories.autoinfracao_repository import AutoInfracaoRepository
from exceptions.CustomExceptions import ErrGetData, ErrInsertData, ErrReadingFile


def insert_ignore_mysql(table, conn, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]
    stmt = insert(table.table).values(data).prefix_with("IGNORE")
    result = conn.execute(stmt)
    return result.rowcount


def get_infracoes(date: Any, ai: Any) -> List[Dict[str, Any]]:
    """Recupera os autos de infração"""
    try:
        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            infracoes = repo.get_infracoes(date, ai)
            return [inf.to_dict() for inf in infracoes]
    except Exception as e:
        logger.systemLog(e)
        raise ErrGetData("Erro ao recuperar dados", 500)


def check_infracoes(csv: Any) -> Tuple[int, int, List[str]]:
    """Realiza a verificação dos autos de infração no banco de dados"""
    try:
        data_frame = pd.read_csv(csv, header=0, delimiter=';')
        values = data_frame['NUM_AI'].unique().tolist()
    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile("Erro ao ler o arquivo CSV", 500)

    try:
        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            rows_counter, counter, rows_not_present = repo.check_presence(values)
            return rows_counter, counter, rows_not_present
    except Exception as e:
        logger.systemLog(e)
        raise ErrGetData("Erro ao validar os dados no banco de dados", 500)


def insert_infracoes_csv(csv: Any) -> int:
    """Insere os autos de infração no banco de dados a partir de um arquivo CSV"""
    try:
        data_frame = pd.read_csv(csv, header=0, encoding="latin_1", delimiter=';')
        data_frame['DAT_OCOR_INFR'] = data_frame['DAT_OCOR_INFR'].astype(str) + " " + data_frame['HORA'].astype(str)
        data_frame['DAT_OCOR_INFR'] = pd.to_datetime(data_frame['DAT_OCOR_INFR'], format="%d/%m/%Y %H:%M")
        data_frame['DAT_EMIS_NOTF'] = pd.to_datetime(data_frame['DAT_EMIS_NOTF'], format="%d/%m/%Y")
        data_frame['DAT_LIMT_RECU'] = pd.to_datetime(data_frame['DAT_LIMT_RECU'], format="%d/%m/%Y")
        data_frame["VAL_INFR"] = data_frame['VAL_INFR'].map(lambda x: pd.to_numeric(str(x).replace(',', '.')))
        if 'DAT_CANC' in data_frame.columns and not bool(data_frame['DAT_CANC'].isnull().all()):
            data_frame['DAT_CANC'] = pd.to_datetime(data_frame['DAT_CANC'], format="%d/%m/%Y")
        data_frame = data_frame.drop(columns=['HORA'])
    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile(f"Erro ao processar o arquivo CSV. {e}", 500)

    try:
        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            count = repo.insert_bulk_df(data_frame, insert_ignore_mysql)
            logger.systemLog(f"INFO: {count} autos processados. FILE: {csv}")
            return count
    except Exception as e:
        logger.systemLog(e)
        raise ErrInsertData(f'Erro ao inserir os autos de primeira instância - {csv}', 500)


def insert_infracoes_xls(xls: Any, ignore: bool) -> int:
    """Insere os autos de infração no banco de dados a partir de um arquivo XLS"""
    try:
        data_frame = pd.read_excel(xls, header=0)
    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile(f'Problema ao processar o arquivo no Load: {xls}', 500)

    try:
        data_frame['DAT_OCOR_INFR'] = data_frame['DAT_OCOR_INFR'].astype(str) + " " + data_frame['HORA'].astype(str)
        data_frame['DAT_OCOR_INFR'] = pd.to_datetime(data_frame['DAT_OCOR_INFR'], format="%Y-%m-%d %H:%M:%S")
        data_frame['DAT_EMIS_NOTF'] = pd.to_datetime(data_frame['DAT_EMIS_NOTF'], format="%Y-%m-%d")
        data_frame['DAT_LIMT_RECU'] = pd.to_datetime(data_frame['DAT_LIMT_RECU'], format="%Y-%m-%d")
        if 'DAT_CANC' in data_frame.columns and not bool(data_frame['DAT_CANC'].isnull().all()):
            data_frame['DAT_CANC'] = pd.to_datetime(data_frame['DAT_CANC'], format="%Y-%m-%d")

        data_frame = data_frame.drop(columns=['HORA'])
        data_frame.replace([np.nan], [None], inplace=True)
    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile(f'Problema ao corrigir datas e manipular colunas: {xls}', 500)

    try:
        rows_to_insert = [row.to_dict() for _, row in data_frame.iterrows()]
        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            count = repo.insert_bulk_rows(rows_to_insert, ignore=ignore)
            return count
    except Exception as e:
        logger.systemLog(e)
        raise ErrInsertData(f'Erro ao inserir o auto de infração no banco de dados', 500)


@deprecated("use insert_infracoes_xls instead")
def insert_cmn_infracoes_xls(xls: Any) -> int:
    """Insere os autos de infração no banco de dados a partir de um arquivo XLS"""
    try:
        data_frame = pd.read_excel(xls, header=0)
    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile(f'Problema ao processar o arquivo no Load: {xls}', 500)

    try:
        data_frame['DAT_OCOR_INFR'] = data_frame['DAT_OCOR_INFR'].astype(str) + " " + data_frame['HORA'].astype(str)
        data_frame['DAT_OCOR_INFR'] = pd.to_datetime(data_frame['DAT_OCOR_INFR'], format="%d/%m/%Y %H:%M")
        data_frame['DAT_EMIS_NOTF'] = pd.to_datetime(data_frame['DAT_EMIS_NOTF'], format="%d/%m/%Y")
        data_frame['DAT_LIMT_RECU'] = pd.to_datetime(data_frame['DAT_LIMT_RECU'], format="%d/%m/%Y")
        if 'DAT_CANC' in data_frame.columns and not bool(data_frame['DAT_CANC'].isnull().all()):
            data_frame['DAT_CANC'] = pd.to_datetime(data_frame['DAT_CANC'], format="%d/%m/%Y")

        data_frame = data_frame.drop(columns=['HORA'])
    except Exception as e:
        logger.systemLog(e)
        raise ErrReadingFile(f'Problema ao corrigir datas e manipular colunas: {xls}', 500)

    try:
        with get_db() as db:
            repo = AutoInfracaoRepository(db)
            count = repo.insert_bulk_df(data_frame, insert_ignore_mysql)
            logger.systemLog(f"INFO: {count} autos processados - {xls}")
            return count
    except Exception as e:
        logger.systemLog(e)
        raise ErrInsertData(f'Erro ao inserir os autos de primeira instância - {xls}', 500)
