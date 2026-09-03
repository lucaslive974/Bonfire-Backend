from flask import Blueprint, current_app

from exceptions.CustomExceptions import ErrIncompleteData
from routes.spec import spec
from routes.v1.schemas.common import MutationResponseDTO, create_api_response
from routes.v1.schemas.veiculos import (
    VeiculoListRequestDTO,
    VeiculoListResponseDTO,
)

veiculoBlueprint = Blueprint("veiculo", __name__)


def _get_service():
    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    return factory.get_veiculo_service()


@veiculoBlueprint.route("/veiculos", methods=["GET"])
@spec.validate(
    resp=create_api_response(VeiculoListResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Veículos"],
)
def executeRouteGetVeiculo():
    service = _get_service()
    result = service.get_veiculos()
    return VeiculoListResponseDTO(veiculos=result), 200


@veiculoBlueprint.route("/veiculos", methods=["POST"])
@spec.validate(
    json=VeiculoListRequestDTO,
    resp=create_api_response(MutationResponseDTO, success_code=201),
    security={"BearerAuth": []},
    tags=["Veículos"],
)
def executeRoutePostVeiculos(json: VeiculoListRequestDTO):
    jsonData = json.model_dump()
    service = _get_service()
    response = service.insert_veiculos(jsonData)
    return (
        MutationResponseDTO(message="Veículos inseridos com sucesso", counter=response),
        201,
    )


@veiculoBlueprint.route("/veiculos", methods=["PATCH"])
@spec.validate(
    json=VeiculoListRequestDTO,
    resp=create_api_response(MutationResponseDTO, success_code=202),
    security={"BearerAuth": []},
    tags=["Veículos"],
)
def executeRoutePatchVeiculos(json: VeiculoListRequestDTO):
    jsonData = json.model_dump()
    service = _get_service()
    response = service.update_veiculos(jsonData)
    return (
        MutationResponseDTO(
            message="Veículos atualizados com sucesso", counter=response
        ),
        202,
    )


@veiculoBlueprint.route("/veiculos/<string:NUM_VEIC>", methods=["DELETE"])
@spec.validate(
    resp=create_api_response(MutationResponseDTO, success_code=202),
    security={"BearerAuth": []},
    tags=["Veículos"],
)
def executeRouteDeleteVeiculos(NUM_VEIC: str):
    service = _get_service()
    response = service.delete_veiculos(NUM_VEIC)
    return (
        MutationResponseDTO(message="Veículos deletados com sucesso", counter=response),
        202,
    )
