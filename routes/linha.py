import json
from flask import Blueprint, jsonify, request
from services.linha_service import LinhaService
from utils.validators import checkKeysInJson

linhaBlueprint = Blueprint('linha', __name__)
keys_to_check = ["COD_LINH", "ID_OPERADORA", "COMPARTILHADA",  "LINH_ATIV_EMPR"]

@linhaBlueprint.route("/linha", methods=["GET"])
def executeRouteGetLinha():
    result = LinhaService.get_linha()
    return jsonify({"linha": json.loads(result)})

@linhaBlueprint.route("/linha", methods=["POST"])
def executeRoutePostLinha():
    jsonData = request.get_json()
    checkKeysInJson(jsonData, keys_to_check, "linha")
    response = LinhaService.insert_linha(jsonData)
    return jsonify({"message": "linhas inseridas com sucesso", "counter": response}), 201

@linhaBlueprint.route("/linha", methods=["PATCH"])
def executeRouteUpdateLinha():
    jsonData = request.get_json()
    checkKeysInJson(jsonData, keys_to_check, "linha")
    response = LinhaService.update_linha(jsonData)
    return jsonify({"message": "linha atualizada com sucesso", "counter": response}), 200

@linhaBlueprint.route("/linha/<string:COD_LINH>", methods=["DELETE"])
def executeRouteDeleteLinha(COD_LINH):
    response = LinhaService.delete_linha(COD_LINH)
    return jsonify({"message": "linha deletada com sucesso", "counter": response}), 200
