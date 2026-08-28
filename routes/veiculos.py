import json
from flask import Blueprint, jsonify, request
from services.veiculo_service import VeiculoService
from utils.validators import checkKeysInJson

veiculoBlueprint = Blueprint('veiculo', __name__)
keys_to_check = ["NUM_VEIC", "IDN_PLAC_VEIC", "VEIC_ATIV_EMPR"]

@veiculoBlueprint.route("/veiculos", methods=["GET"])
def executeRouteGetVeiculo():
    result = VeiculoService.get_veiculos()
    return jsonify({"veiculos": json.loads(result)})

@veiculoBlueprint.route("/veiculos", methods=["POST"])
def executeRoutePostVeiculos():
    jsonData = request.get_json()
    checkKeysInJson(jsonData, keys_to_check, "veiculo")
    response = VeiculoService.insert_veiculos(jsonData)
    return jsonify({"message": "Veículos inseridos com sucesso", "counter": response}), 201

@veiculoBlueprint.route("/veiculos", methods=["PATCH"])
def executeRoutePatchVeiculos():
    jsonData = request.get_json()
    checkKeysInJson(jsonData, keys_to_check, "veiculo")
    response = VeiculoService.update_veiculos(jsonData)
    return jsonify({"message": "Veículos atualizados com sucesso", "counter": response}), 202

@veiculoBlueprint.route("/veiculos/<string:NUM_VEIC>", methods=["DELETE"])
def executeRouteDeleteVeiculos(NUM_VEIC):
    response = VeiculoService.delete_veiculos(NUM_VEIC)
    return jsonify({"message": "Veículos deletados com sucesso", "counter": response}), 202
