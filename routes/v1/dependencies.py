from flask import current_app

from exceptions.CustomExceptions import ErrIncompleteData
from services.autoinfracao_service import AutoInfracaoService
from services.consorcio_service import ConsorcioService
from services.factory import ServiceFactory
from services.linha_service import LinhaService
from services.recurso_service import RecursoService
from services.veiculo_service import VeiculoService


def get_service_factory() -> ServiceFactory:
    """Retrieve the ServiceFactory registered in the Flask application."""
    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    return factory


def get_consorcio_service() -> ConsorcioService:
    return get_service_factory().get_consorcio_service()


def get_veiculo_service() -> VeiculoService:
    return get_service_factory().get_veiculo_service()


def get_linha_service() -> LinhaService:
    return get_service_factory().get_linha_service()


def get_autoinfracao_service() -> AutoInfracaoService:
    return get_service_factory().get_autoinfracao_service()


def get_recurso_service() -> RecursoService:
    return get_service_factory().get_recurso_service()
