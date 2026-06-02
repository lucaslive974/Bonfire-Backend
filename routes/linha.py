import json
from flask import Blueprint, jsonify, request
from handlers import linha, globais

linhaBlueprint = Blueprint('linha', __name__)
keys_to_check = ["COD_LINH", "ID_OPERADORA", "COMPARTILHADA",  "LINH_ATIV_EMPR"]

@linhaBlueprint.route("/linha", methods=["GET"])
def executeRouteGetLinha():
    result = linha.getLinha()
    return jsonify({"linha": json.loads(result)})

@linhaBlueprint.route("/linha", methods=["POST"])
def executeRoutePostLinha():
    jsonData = request.get_json()
    globais.checkKeysInJson(jsonData, keys_to_check, "linha")
    response = linha.insertLinha(jsonData)
    return jsonify({"message": "linhas inseridas com sucesso", "counter": response}), 201

    
@linhaBlueprint.route("/linha", methods=["PATCH"])
def executeRouteUpdateLinha():
    jsonData = request.get_json()
    globais.checkKeysInJson(jsonData, keys_to_check, "linha")
    response = linha.updateLinha(jsonData)
    return jsonify({"message": "linha atualizada com sucesso", "counter": response}), 200
    

@linhaBlueprint.route("/linha/<string:COD_LINH>", methods=["DELETE"])
def executeRouteDeleteLinha(COD_LINH):
    response = linha.deleteLinha(COD_LINH)
    return jsonify({"message": "linha deletada com sucesso", "counter": response}), 200
    
