from typing import List

from classes.Linha import Linha
from exceptions.CustomExceptions import ErrUpdateData
from repositories.interfaces import IRepositoryManager


class LinhaService:
    """Domain service for Bus Line use cases."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def get_linha(self) -> List[Linha]:
        """Retrieve line data from the database as domain entities."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            return repo.get_all()

    def insert_linha(self, linhas: List[Linha]) -> int:
        """Insert a list of line domain entities into the database."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            return repo.insert_bulk(linhas)

    def update_linha(self, linhas: List[Linha]) -> int:
        """Update a list of line domain entities in the database."""
        with self._db_manager.session() as session:
            linha_repo = session.get_linha_repository()
            consorcio_repo = session.get_consorcio_repository()

            operadoras_ids = {
                linha.operator_id for linha in linhas if linha.operator_id is not None
            }
            if operadoras_ids:
                existing_operadoras = consorcio_repo.get_by_ids(list(operadoras_ids))
                existentes_ids = {
                    op.id for op in existing_operadoras if op.id is not None
                }
                faltantes = operadoras_ids - existentes_ids
                if faltantes:
                    faltantes_str = ", ".join(str(f) for f in faltantes)
                    raise ErrUpdateData(
                        message="Operadora inexistente",
                        status=400,
                        error="Bad Request",
                        friendly_message=f"Não é possível atualizar. Os seguintes consórcios/operadoras não existem: {faltantes_str}",
                    )

            cod_linhas = [
                item.line_code for item in linhas if isinstance(item.line_code, str)
            ]
            if not cod_linhas:
                return 0

            existing = linha_repo.get_by_ids(cod_linhas)
            existing_map = {
                linha.line_code: linha
                for linha in existing
                if linha.line_code is not None
            }

            updated_codes = set()
            to_update: List[Linha] = []
            for item in linhas:
                if item.line_code is not None and item.line_code in existing_map:
                    linha = existing_map[item.line_code]
                    if item.shared is not None:
                        linha.set_shared(item.shared)
                    if item.operator_id is not None:
                        linha.set_operator_id(item.operator_id)
                    if item.active is not None:
                        if not item.active:
                            linha.deactivate(item.deregistration_date)
                        else:
                            linha.activate()
                    elif item.deregistration_date is not None:
                        linha.set_deregistration_date(item.deregistration_date)

                    if item.line_code not in updated_codes:
                        to_update.append(linha)
                        updated_codes.add(item.line_code)

            if not to_update:
                return 0

            return linha_repo.update_bulk(to_update)

    def delete_linha(self, cod_linh: str) -> int:
        """Delete a line from the database by its line code."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            return repo.delete(cod_linh)
