from repositories.interfaces import IRepositoryManager
from services.autoinfracao_service import AutoInfracaoService
from services.consorcio_service import ConsorcioService
from services.linha_service import LinhaService
from services.recurso_service import RecursoService
from services.veiculo_service import VeiculoService


class ServiceFactory:
    def __init__(self, db_manager: IRepositoryManager, parser_factory=None):
        self._db_manager = db_manager
        self._parser_factory = parser_factory

    def get_autoinfracao_service(self) -> AutoInfracaoService:
        return AutoInfracaoService(self._db_manager, self._parser_factory)

    def get_veiculo_service(self) -> VeiculoService:
        return VeiculoService(self._db_manager)

    def get_linha_service(self) -> LinhaService:
        return LinhaService(self._db_manager)

    def get_consorcio_service(self) -> ConsorcioService:
        return ConsorcioService(self._db_manager)

    def get_recurso_service(self) -> RecursoService:
        return RecursoService(self._db_manager, self._parser_factory)
