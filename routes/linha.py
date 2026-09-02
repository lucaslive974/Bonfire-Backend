from flask import Blueprint, current_app, jsonify, request

from exceptions.CustomExceptions import ErrIncompleteData
from utils.validators import checkKeysInJson

linhaBlueprint = Blueprint("linha", __name__)
keys_to_check = ["COD_LINH", "ID_OPERADORA", "COMPARTILHADA", "LINH_ATIV_EMPR"]


def _get_service():
    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    return factory.get_linha_service()


@linhaBlueprint.route("/linha", methods=["GET"])
def executeRouteGetLinha():
    service = _get_service()
    result = service.get_linha()
    return jsonify({"linha": result}), 200


@linhaBlueprint.route("/linha", methods=["POST"])
def executeRoutePostLinha():
    jsonData = request.get_json()
    checkKeysInJson(jsonData, keys_to_check, "linha")
    service = _get_service()
    response = service.insert_linha(jsonData)
    return jsonify(
        {"message": "linhas inseridas com sucesso", "counter": response}
    ), 201


@linhaBlueprint.route("/linha", methods=["PATCH"])
def executeRouteUpdateLinha():
    jsonData = request.get_json()
    checkKeysInJson(jsonData, keys_to_check, "linha")
    service = _get_service()
    response = service.update_linha(jsonData)
    return jsonify(
        {"message": "linha atualizada com sucesso", "counter": response}
    ), 200


@linhaBlueprint.route("/linha/<string:COD_LINH>", methods=["DELETE"])
def executeRouteDeleteLinha(COD_LINH):
    service = _get_service()
    response = service.delete_linha(COD_LINH)
    return jsonify({"message": "linha deletada com sucesso", "counter": response}), 200
