import json
from repositories.database import get_db
from repositories.consorcio_repository import ConsorcioRepository

def get_consorcios() -> str:
    """Retorna todos os consórcios cadastrados."""
    with get_db() as db:
        repo = ConsorcioRepository(db)
        consorcios = repo.get_all()
        data = [c.to_dict() for c in consorcios]
        return json.dumps(data)
