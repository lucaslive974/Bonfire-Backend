from flask import Blueprint, current_app

from exceptions.CustomExceptions import ErrIncompleteData
from routes.spec import spec
from routes.v1.schemas.common import MutationResponseDTO, create_api_response
from routes.v1.schemas.consorcio import (
    ConsorcioListRequestDTO,
    ConsorcioListResponseDTO,
)

consorcioBlueprint = Blueprint("consorcio", __name__)


def _get_service():
    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    return factory.get_consorcio_service()


@consorcioBlueprint.route("/consorcio", methods=["GET"])
@spec.validate(
    resp=create_api_response(ConsorcioListResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Consórcio"],
)
def execute_route_get_consorcio():
    """Rota para buscar todos os consórcios"""
    service = _get_service()
    response = service.get_consorcios()
    return ConsorcioListResponseDTO(consorcios=response), 200


@consorcioBlueprint.route("/consorcio", methods=["POST"])
@spec.validate(
    json=ConsorcioListRequestDTO,
    resp=create_api_response(MutationResponseDTO, success_code=201),
    security={"BearerAuth": []},
    tags=["Consórcio"],
)
def execute_route_post_consorcio(json: ConsorcioListRequestDTO):
    """Rota para inserir novos consórcios"""
    jsonData = json.model_dump()
    service = _get_service()
    response = service.insert_consorcios(jsonData)
    return (
        MutationResponseDTO(
            message="Consórcios inseridos com sucesso", counter=response
        ),
        201,
    )


@consorcioBlueprint.route("/consorcio", methods=["PATCH"])
@spec.validate(
    json=ConsorcioListRequestDTO,
    resp=create_api_response(MutationResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Consórcio"],
)
def execute_route_patch_consorcio(json: ConsorcioListRequestDTO):
    """Rota para atualizar parcialmente consórcios"""
    jsonData = json.model_dump()
    service = _get_service()
    response = service.update_consorcios(jsonData)
    return (
        MutationResponseDTO(
            message="Consórcios atualizados com sucesso", counter=response
        ),
        200,
    )


@consorcioBlueprint.route("/consorcio", methods=["PUT"])
@spec.validate(
    json=ConsorcioListRequestDTO,
    resp=create_api_response(MutationResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Consórcio"],
)
def execute_route_put_consorcio(json: ConsorcioListRequestDTO):
    """Rota para atualizar consórcios (PUT)"""
    jsonData = json.model_dump()
    service = _get_service()
    response = service.update_consorcios(jsonData)
    return (
        MutationResponseDTO(
            message="Consórcios atualizados com sucesso", counter=response
        ),
        200,
    )


@consorcioBlueprint.route("/consorcio/<string:id_consorcio>", methods=["DELETE"])
@spec.validate(
    resp=create_api_response(MutationResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Consórcio"],
)
def execute_route_delete_consorcio(id_consorcio: str):
    """Rota para deletar um consórcio pelo ID"""
    service = _get_service()
    response = service.delete_consorcio(id_consorcio)
    return (
        MutationResponseDTO(message="Consórcio deletado com sucesso", counter=response),
        200,
    )
