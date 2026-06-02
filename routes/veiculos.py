import json
from flask import Blueprint, jsonify, request
from handlers import veiculos
from handlers import globais

veiculoBlueprint = Blueprint('veiculo', __name__)
keys_to_check = ["NUM_VEIC", "IDN_PLAC_VEIC", "VEIC_ATIV_EMPR"]

@veiculoBlueprint.route("/veiculos", methods=["GET"])
def executeRouteGetVeiculo():
    result = veiculos.getVeiculos()
    return jsonify({"veiculos": json.loads(result)})

@veiculoBlueprint.route("/veiculos", methods=["POST"])
def executeRoutePostVeiculos():
    jsonData = request.get_json()
    globais.checkKeysInJson(jsonData, keys_to_check, "veiculo")
    response = veiculos.insertVeiculos(jsonData)
    return jsonify({"message": "Veículos inseridos com sucesso", "counter": response}), 201
    
    
@veiculoBlueprint.route("/veiculos", methods=["PATCH"])
def executeRoutePatchVeiculos():
    jsonData = request.get_json()
    globais.checkKeysInJson(jsonData, keys_to_check, "veiculo")
    response = veiculos.updateVeiculos(jsonData)
    return jsonify({"message": "Veículos atualizados com sucesso", "counter": response}), 202    

@veiculoBlueprint.route("/veiculos/<string:NUM_VEIC>", methods=["DELETE"])
def executeRouteDeleteVeiculos(NUM_VEIC):
    response = veiculos.deleteVeiculos(NUM_VEIC)
    return jsonify({"message": "Veículos deletados com sucesso", "counter": response}), 202
