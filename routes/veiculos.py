from flask import Blueprint, current_app, jsonify, request

from exceptions.CustomExceptions import ErrIncompleteData
from utils.validators import checkKeysInJson

veiculoBlueprint = Blueprint("veiculo", __name__)
keys_to_check = ["NUM_VEIC", "IDN_PLAC_VEIC", "VEIC_ATIV_EMPR"]


def _get_service():
    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    return factory.get_veiculo_service()


@veiculoBlueprint.route("/veiculos", methods=["GET"])
def executeRouteGetVeiculo():
    service = _get_service()
    result = service.get_veiculos()
    return jsonify({"veiculos": result}), 200


@veiculoBlueprint.route("/veiculos", methods=["POST"])
def executeRoutePostVeiculos():
    jsonData = request.get_json()
    checkKeysInJson(jsonData, keys_to_check, "veiculo")
    service = _get_service()
    response = service.insert_veiculos(jsonData)
    return jsonify(
        {"message": "Veículos inseridos com sucesso", "counter": response}
    ), 201


@veiculoBlueprint.route("/veiculos", methods=["PATCH"])
def executeRoutePatchVeiculos():
    jsonData = request.get_json()
    checkKeysInJson(jsonData, keys_to_check, "veiculo")
    service = _get_service()
    response = service.update_veiculos(jsonData)
    return jsonify(
        {"message": "Veículos atualizados com sucesso", "counter": response}
    ), 202


@veiculoBlueprint.route("/veiculos/<string:NUM_VEIC>", methods=["DELETE"])
def executeRouteDeleteVeiculos(NUM_VEIC):
    service = _get_service()
    response = service.delete_veiculos(NUM_VEIC)
    return jsonify(
        {"message": "Veículos deletados com sucesso", "counter": response}
    ), 202
