import json
from flask import Blueprint, jsonify, request
from handlers import consorcios, globais

consorcioBlueprint = Blueprint('consorcio', __name__)
keys_to_check = ["ID", "NOME", "CONCESSIONARIA"]

@consorcioBlueprint.route("/consorcio", methods=["GET"])
def execute_route_get_consorcio():
    """Rota para buscar todos os consórcios"""
    response = consorcios.get_consorcios()
    return jsonify({"consorcios": json.loads(response)})

@consorcioBlueprint.route("/consorcio", methods=["POST"])
def execute_route_post_consorcio():
    """Rota para inserir novos consórcios"""
    jsonData = request.get_json()
    globais.checkKeysInJson(jsonData, keys_to_check, "consorcio")
    response = consorcios.insert_consorcios(jsonData)
    return jsonify({"message": "Consórcios inseridos com sucesso", "counter": response}), 201

@consorcioBlueprint.route("/consorcio", methods=["PATCH"])
def execute_route_patch_consorcio():
    """Rota para atualizar parcialmente consórcios"""
    jsonData = request.get_json()
    globais.checkKeysInJson(jsonData, keys_to_check, "consorcio")
    response = consorcios.update_consorcios(jsonData)
    return jsonify({"message": "Consórcios atualizados com sucesso", "counter": response}), 200

@consorcioBlueprint.route("/consorcio", methods=["PUT"])
def execute_route_put_consorcio():
    """Rota para atualizar consórcios (PUT)"""
    jsonData = request.get_json()
    globais.checkKeysInJson(jsonData, keys_to_check, "consorcio")
    response = consorcios.update_consorcios(jsonData)
    return jsonify({"message": "Consórcios atualizados com sucesso", "counter": response}), 200

@consorcioBlueprint.route("/consorcio/<string:id_consorcio>", methods=["DELETE"])
def execute_route_delete_consorcio(id_consorcio):
    """Rota para deletar um consórcio pelo ID"""
    response = consorcios.delete_consorcio(id_consorcio)
    return jsonify({"message": "Consórcio deletado com sucesso", "counter": response}), 200