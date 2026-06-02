from typing import List, Dict, Any
from sqlalchemy.orm import Session
from classes.Operadora import Operadora

class ConsorcioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Operadora]:
        """Retorna todas as operadoras (consórcios)."""
        return self.db.query(Operadora).all()

    def get_by_id(self, id_consorcio: int) -> Operadora | None:
        """Busca uma operadora pelo ID."""
        return self.db.query(Operadora).filter(Operadora.ID == id_consorcio).first()

    def insert_bulk(self, consorcios_data: List[Dict[str, Any]]) -> int:
        """Insere ou atualiza (merge) uma lista de consórcios no banco de dados."""
        counter = 0
        for data in consorcios_data:
            id_consorcio = data.get("ID") or data.get("id")
            if id_consorcio is not None:
                consorcio = Operadora(
                    ID=int(id_consorcio),
                    NOME=data.get("NOME") or data.get("nome"),
                    CONCESSIONARIA=data.get("CONCESSIONARIA") or data.get("concessionaria")
                )
                self.db.merge(consorcio)
                counter += 1
        return counter

    def update_bulk(self, consorcios_data: List[Dict[str, Any]]) -> int:
        """Atualiza campos de uma lista de consórcios no banco de dados."""
        counter = 0
        for data in consorcios_data:
            id_consorcio = data.get("ID") or data.get("id")
            if id_consorcio is not None:
                try:
                    id_consorcio_int = int(id_consorcio)
                except (ValueError, TypeError):
                    continue
                consorcio = self.get_by_id(id_consorcio_int)
                if consorcio:
                    if "NOME" in data or "nome" in data:
                        val = data.get("NOME") or data.get("nome")
                        consorcio.NOME = str(val) if val else None
                    if "CONCESSIONARIA" in data or "concessionaria" in data:
                        val = data.get("CONCESSIONARIA") or data.get("concessionaria")
                        consorcio.CONCESSIONARIA = str(val) if val else None
                    self.db.merge(consorcio)
                    counter += 1
        return counter

    def delete(self, id_consorcio: int) -> int:
        """Exclui um consórcio pelo ID."""
        deleted = self.db.query(Operadora).filter(Operadora.ID == id_consorcio).delete()
        return deleted
