from flask import Blueprint

from routes.spec import spec
from routes.v1.dependencies import get_recurso_service
from routes.v1.schemas.common import MutationResponseDTO, create_api_response
from routes.v1.schemas.recursos import (
    RecursoListResponseDTO,
    RecursoPrimeiraInstanciaQueryDTO,
    RecursoPrimeiraInstanciaUploadDTO,
    RecursoSegundaInstanciaQueryDTO,
    RecursoSegundaInstanciaUploadDTO,
)

RecursoPrimeiraInstanciaBlueprint = Blueprint("recurso1", __name__)
RecuroSegundaInstanciaBlueprint = Blueprint("recurso2", __name__)
_get_service = get_recurso_service


@RecursoPrimeiraInstanciaBlueprint.route(
    "/recurso/primeiraInstancia/resultado", methods=["POST"]
)
@spec.validate(
    form=RecursoPrimeiraInstanciaUploadDTO,
    resp=create_api_response(MutationResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Recursos - 1ª Instância"],
)
def post_recursos_primeira_instancia(form: RecursoPrimeiraInstanciaUploadDTO):
    service = _get_service()
    metrics = service.extract_primeira_instancia(form.file.stream)
    return (
        MutationResponseDTO(
            message="itens Extraídos e armazenados com sucesso!",
            counter=metrics.get("inserted", 0),
        ),
        200,
    )


@RecuroSegundaInstanciaBlueprint.route(
    "/recurso/segundaInstancia/resultado", methods=["POST"]
)
@spec.validate(
    form=RecursoSegundaInstanciaUploadDTO,
    resp=create_api_response(MutationResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Recursos - 2ª Instância"],
)
def post_recursos_segunda_instancia(form: RecursoSegundaInstanciaUploadDTO):
    service = _get_service()
    metrics = service.extract_segunda_instancia(form.file.stream)
    return (
        MutationResponseDTO(
            message="itens Extraídos e armazenados com sucesso!",
            counter=metrics.get("inserted", 0),
        ),
        200,
    )


@RecursoPrimeiraInstanciaBlueprint.route("/recurso/primeiraInstancia", methods=["GET"])
@spec.validate(
    query=RecursoPrimeiraInstanciaQueryDTO,
    resp=create_api_response(RecursoListResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Recursos - 1ª Instância"],
)
def get_recursos_primeira_instancia(query: RecursoPrimeiraInstanciaQueryDTO):
    service = _get_service()
    return (
        RecursoListResponseDTO(
            recurses=service.get_primeira_instancia(query.date, query.ata)
        ),
        200,
    )


@RecuroSegundaInstanciaBlueprint.route("/recurso/segundaInstancia", methods=["GET"])
@spec.validate(
    query=RecursoSegundaInstanciaQueryDTO,
    resp=create_api_response(RecursoListResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Recursos - 2ª Instância"],
)
def get_recursos_segunda_instancia(query: RecursoSegundaInstanciaQueryDTO):
    service = _get_service()
    return (
        RecursoListResponseDTO(recurses=service.get_segunda_instancia(query.date)),
        200,
    )
