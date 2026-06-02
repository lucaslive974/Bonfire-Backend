from flask import Blueprint, jsonify, request
from tempfile import NamedTemporaryFile
from exceptions.CustomExceptions import *
from handlers import recursos

RecursoPrimeiraInstanciaBlueprint = Blueprint('recursoPrimeiraInstancia', __name__)

@RecursoPrimeiraInstanciaBlueprint.route("/recurso/primeiraInstancia/resultado", methods=["POST"])
def postResultadoPrimeiraInstancia():
    try:
        if 'file' not in request.files:
            raise ErrIncompleteData("Arquivo de resultado de primeira instancia não está presente na requisição", 400)

        file = request.files['file']
        temp_file = NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        recurso_primeira_instancia_list = recursos.parseDocx(temp_file)
        response = recursos.insertPrimeiraInstancia(recurso_primeira_instancia_list)
        return jsonify({"message": "itens Extraídos e armazenados com sucesso!", "counter": response}), 200

    except CustomException as e:
        return jsonify(e.to_json()), e.status     

@RecursoPrimeiraInstanciaBlueprint.route("/recurso/primeiraInstancia", methods=["GET"])
def getRecursoPrimeiraInstancia():
    try:
        date = request.args.get('date')
        ata = request.args.get('ata')
        result = recursos.getPrimeiraInstancia(date, ata)
        return jsonify({"recurses": result }), 200    
    except CustomException as e:
        return jsonify(e.to_json()), e.status


RecuroSegundaInstanciaBlueprint = Blueprint('recursoSegundaInstancia', __name__)

@RecuroSegundaInstanciaBlueprint.route("/recurso/segundaInstancia/resultado", methods=["POST"])
def postResultadoSegundaInstancia():
    try:
        if 'file' not in request.files:
            raise ErrIncompleteData("Arquivo de resultado de segunda instancia não está presente na requisição", 400)

        file = request.files['file']
        temp_file = NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        response = recursos.insertSegundaInstancia(recursos.parseDocx(temp_file, False))
        return jsonify({"message": "itens Extraídos e armazenados com sucesso!", "counter": response}), 200

    except CustomException as e:
        return jsonify(e.to_json()), e.status


@RecursoPrimeiraInstanciaBlueprint.route("/recurso/segundaInstancia", methods=["GET"])
def getRecursoSegundaInstancia():
    try:
        date = request.args.get('date')
        result = recursos.getSegundaInstancia(date)
        return jsonify({"recurses": result }), 200
    except CustomException as e:
        return jsonify(e.to_json()), e.status