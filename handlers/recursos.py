from typing import List, Dict, Any

from repositories.database import get_db
from repositories.recurso_repository import RecursoRepository
from exceptions.CustomExceptions import ErrNullInsert
from services.parsers import parse_docx_recursos


def getPrimeiraInstancia(date: Any, ata: Any) -> List[Dict[str, Any]]:
    """Retorna os recursos de primeira instância"""
    with get_db() as db:
        repo = RecursoRepository(db)
        return repo.get_primeira_instancia(date, ata)


def getSegundaInstancia(date: Any) -> List[Dict[str, Any]]:
    """Retorna os recursos de segunda instância"""
    with get_db() as db:
        repo = RecursoRepository(db)
        return repo.get_segunda_instancia(date)


def parseDocx(docx: Any, first_instance: bool = True) -> List[Dict[str, Any]]:
    """Realiza o parse do documento DOCX delegando para o parser service (mantém assinatura para retrocompatibilidade)"""
    return parse_docx_recursos(docx, first_instance)


def insertPrimeiraInstancia(recursos_primeira_instancia: List[Dict[str, Any]] | None) -> int:
    """Insere no banco de dados uma lista de recursos de primeira instância"""
    if recursos_primeira_instancia is None:
        raise ErrNullInsert('Lista de recursos vazia, nenhum registro inserido', 400)

    with get_db() as db:
        repo = RecursoRepository(db)
        count = repo.insert_primeira_instancia(recursos_primeira_instancia)
        return count


def insertSegundaInstancia(recursos_segunda_instancia: List[Dict[str, Any]] | None) -> int:
    """Insere no banco de dados uma lista de recursos de segunda instância"""
    if recursos_segunda_instancia is None:
        raise ErrNullInsert('Lista de recursos vazia, nenhum registro inserido', 400)

    with get_db() as db:
        repo = RecursoRepository(db)
        count = repo.insert_segunda_instancia(recursos_segunda_instancia)
        return count
