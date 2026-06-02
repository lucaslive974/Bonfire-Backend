import json
from flask import Blueprint
from handlers import consorcios
from flask import jsonify

consorcioBlueprint = Blueprint('consorcio', __name__)
keys_to_chek = ["nome", "compartilhado"]

@consorcioBlueprint.route("/consorcio", methods=["GET"])
def execute_route_get_consorcio():
    response = consorcios.get_consorcios()
    return jsonify({"consorcios": json.loads(response)})