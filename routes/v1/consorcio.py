from flask import Blueprint

from classes.Operadora import Operadora
from routes.spec import spec
from routes.v1.dependencies import get_consorcio_service
from routes.v1.schemas.common import MutationResponseDTO, create_api_response
from routes.v1.schemas.consorcio import (
    ConsorcioListRequestDTO,
    ConsorcioListResponseDTO,
)

consorcioBlueprint = Blueprint("consorcio", __name__)
_get_service = get_consorcio_service


@consorcioBlueprint.route("/consorcio", methods=["GET"])
@spec.validate(
    resp=create_api_response(ConsorcioListResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Consórcio"],
)
def execute_route_get_consorcio():
    """Route to get all consórcios."""
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
    """Route to insert new consórcios."""
    operadoras = [
        Operadora(ID=item.ID, NOME=item.NOME, CONCESSIONARIA=item.CONCESSIONARIA)
        for item in json.root
    ]
    service = _get_service()
    response = service.insert_consorcios(operadoras)
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
    """Route to partially update consórcios."""
    operadoras = [
        Operadora(ID=item.ID, NOME=item.NOME, CONCESSIONARIA=item.CONCESSIONARIA)
        for item in json.root
    ]
    service = _get_service()
    response = service.update_consorcios(operadoras)
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
    """Route to update consórcios (PUT)."""
    operadoras = [
        Operadora(ID=item.ID, NOME=item.NOME, CONCESSIONARIA=item.CONCESSIONARIA)
        for item in json.root
    ]
    service = _get_service()
    response = service.update_consorcios(operadoras)
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
    """Route to delete a consórcio by ID."""
    service = _get_service()
    response = service.delete_consorcio(id_consorcio)
    return (
        MutationResponseDTO(message="Consórcio deletado com sucesso", counter=response),
        200,
    )
