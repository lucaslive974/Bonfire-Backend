import json
from repositories.database import get_db
from repositories.consorcio_repository import ConsorcioRepository
from handlers.log import logger
from exceptions.CustomExceptions import ErrGetData

def get_consorcios() -> str:
    """Retorna todos os consórcios cadastrados."""
    try:
        with get_db() as db:
            repo = ConsorcioRepository(db)
            consorcios = repo.get_all()
            data = [c.to_dict() for c in consorcios]
            return json.dumps(data)
    except Exception as e:
        logger.systemLog(e)
        raise ErrGetData('Erro ao recuperar os consórcios', 500)
