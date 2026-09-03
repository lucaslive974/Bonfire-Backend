from flask import Blueprint, current_app

from exceptions.CustomExceptions import ErrIncompleteData
from routes.spec import spec
from routes.v1.schemas.common import MutationResponseDTO, create_api_response
from routes.v1.schemas.linha import LinhaListRequestDTO, LinhaListResponseDTO

linhaBlueprint = Blueprint("linha", __name__)


def _get_service():
    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    return factory.get_linha_service()


@linhaBlueprint.route("/linha", methods=["GET"])
@spec.validate(
    resp=create_api_response(LinhaListResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Linhas"],
)
def executeRouteGetLinha():
    service = _get_service()
    result = service.get_linha()
    return LinhaListResponseDTO(linha=result), 200


@linhaBlueprint.route("/linha", methods=["POST"])
@spec.validate(
    json=LinhaListRequestDTO,
    resp=create_api_response(MutationResponseDTO, success_code=201),
    security={"BearerAuth": []},
    tags=["Linhas"],
)
def executeRoutePostLinha(json: LinhaListRequestDTO):
    jsonData = json.model_dump()
    service = _get_service()
    response = service.insert_linha(jsonData)
    return (
        MutationResponseDTO(message="linhas inseridas com sucesso", counter=response),
        201,
    )


@linhaBlueprint.route("/linha", methods=["PATCH"])
@spec.validate(
    json=LinhaListRequestDTO,
    resp=create_api_response(MutationResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Linhas"],
)
def executeRouteUpdateLinha(json: LinhaListRequestDTO):
    jsonData = json.model_dump()
    service = _get_service()
    response = service.update_linha(jsonData)
    return (
        MutationResponseDTO(message="linha atualizada com sucesso", counter=response),
        200,
    )


@linhaBlueprint.route("/linha/<string:COD_LINH>", methods=["DELETE"])
@spec.validate(
    resp=create_api_response(MutationResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Linhas"],
)
def executeRouteDeleteLinha(COD_LINH: str):
    service = _get_service()
    response = service.delete_linha(COD_LINH)
    return (
        MutationResponseDTO(message="linha deletada com sucesso", counter=response),
        200,
    )
