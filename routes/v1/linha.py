from flask import Blueprint

from classes.Linha import Linha
from routes.spec import spec
from routes.v1.dependencies import get_linha_service
from routes.v1.schemas.common import MutationResponseDTO, create_api_response
from routes.v1.schemas.linha import LinhaListRequestDTO, LinhaListResponseDTO

linhaBlueprint = Blueprint("linha", __name__)
_get_service = get_linha_service


@linhaBlueprint.route("/linha", methods=["GET"])
@spec.validate(
    resp=create_api_response(LinhaListResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Linhas"],
)
def executeRouteGetLinha():
    """Get all lines."""
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
    """Insert lines."""
    linhas = [
        Linha(
            COD_LINH=item.COD_LINH,
            ID_OPERADORA=item.ID_OPERADORA,
            COMPARTILHADA=item.COMPARTILHADA
            if item.COMPARTILHADA is not None
            else False,
            LINH_ATIV_EMPR=item.LINH_ATIV_EMPR
            if item.LINH_ATIV_EMPR is not None
            else True,
            DAT_BAIX=item.DAT_BAIX,
        )
        for item in json.root
    ]
    service = _get_service()
    response = service.insert_linha(linhas)
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
    """Update lines."""
    linhas = [
        Linha(
            COD_LINH=item.COD_LINH,
            ID_OPERADORA=item.ID_OPERADORA,
            COMPARTILHADA=item.COMPARTILHADA,
            LINH_ATIV_EMPR=item.LINH_ATIV_EMPR,
            DAT_BAIX=item.DAT_BAIX,
        )
        for item in json.root
    ]
    service = _get_service()
    response = service.update_linha(linhas)
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
    """Delete a line by its line code."""
    service = _get_service()
    response = service.delete_linha(COD_LINH)
    return (
        MutationResponseDTO(message="linha deletada com sucesso", counter=response),
        200,
    )
