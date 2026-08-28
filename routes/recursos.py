from flask import Blueprint, jsonify, request
from tempfile import NamedTemporaryFile
from exceptions.CustomExceptions import ErrIncompleteData
from services.recurso_service import RecursoService

RecursoPrimeiraInstanciaBlueprint = Blueprint('recursoPrimeiraInstancia', __name__)

@RecursoPrimeiraInstanciaBlueprint.route("/recurso/primeiraInstancia/resultado", methods=["POST"])
def postResultadoPrimeiraInstancia():
    if 'file' not in request.files:
        raise ErrIncompleteData("Arquivo de resultado de primeira instancia não está presente na requisição", 400)

    file = request.files['file']
    temp_file = NamedTemporaryFile(delete=False)
    file.save(temp_file.name)

    recurso_primeira_instancia_list = RecursoService.parse_docx(temp_file)
    response = RecursoService.insert_primeira_instancia(recurso_primeira_instancia_list)
    return jsonify({"message": "itens Extraídos e armazenados com sucesso!", "counter": response}), 200

@RecursoPrimeiraInstanciaBlueprint.route("/recurso/primeiraInstancia", methods=["GET"])
def getRecursoPrimeiraInstancia():
    date = request.args.get('date')
    ata = request.args.get('ata')
    result = RecursoService.get_primeira_instancia(date, ata)
    return jsonify({"recurses": result }), 200    


RecuroSegundaInstanciaBlueprint = Blueprint('recursoSegundaInstancia', __name__)

@RecuroSegundaInstanciaBlueprint.route("/recurso/segundaInstancia/resultado", methods=["POST"])
def postResultadoSegundaInstancia():
    if 'file' not in request.files:
        raise ErrIncompleteData("Arquivo de resultado de segunda instancia não está presente na requisição", 400)

    file = request.files['file']
    temp_file = NamedTemporaryFile(delete=False)
    file.save(temp_file.name)

    response = RecursoService.insert_segunda_instancia(RecursoService.parse_docx(temp_file, False))
    return jsonify({"message": "itens Extraídos e armazenados com sucesso!", "counter": response}), 200


@RecursoPrimeiraInstanciaBlueprint.route("/recurso/segundaInstancia", methods=["GET"])
def getRecursoSegundaInstancia():
    date = request.args.get('date')
    result = RecursoService.get_segunda_instancia(date)
    return jsonify({"recurses": result }), 200
