from flask import Blueprint, current_app, jsonify, request

from exceptions.CustomExceptions import ErrIncompleteData
from services.recurso_service import RecursoService

RecursoPrimeiraInstanciaBlueprint = Blueprint("recurso1", __name__)
RecuroSegundaInstanciaBlueprint = Blueprint("recurso2", __name__)


@RecursoPrimeiraInstanciaBlueprint.route(
    "/recurso/primeiraInstancia/resultado", methods=["POST"]
)
def post_recursos_primeira_instancia():
    if "file" not in request.files:
        raise ErrIncompleteData(
            "Arquivo de resultado de primeira instancia não está presente na requisição",
            400,
        )
    file = request.files["file"]
    factory = current_app.extensions.get("parser_factory")
    if not factory:
        raise ErrIncompleteData("ParserFactory not configured", 500)
    extractor = factory.create_primeira_instancia_parser()
    metrics = extractor.extract(file.stream)
    return jsonify(
        {
            "message": "itens Extraídos e armazenados com sucesso!",
            "counter": metrics.get("inserted", 0),
        }
    ), 200


@RecuroSegundaInstanciaBlueprint.route(
    "/recurso/segundaInstancia/resultado", methods=["POST"]
)
def post_recursos_segunda_instancia():
    if "file" not in request.files:
        raise ErrIncompleteData(
            "Arquivo de resultado de segunda instancia não está presente na requisição",
            400,
        )
    file = request.files["file"]
    factory = current_app.extensions.get("parser_factory")
    if not factory:
        raise ErrIncompleteData("ParserFactory not configured", 500)
    extractor = factory.create_segunda_instancia_parser()
    metrics = extractor.extract(file.stream)
    return jsonify(
        {
            "message": "itens Extraídos e armazenados com sucesso!",
            "counter": metrics.get("inserted", 0),
        }
    ), 200


@RecursoPrimeiraInstanciaBlueprint.route("/recurso/primeiraInstancia", methods=["GET"])
def get_recursos_primeira_instancia():
    date = request.args.get("date")
    ata = request.args.get("ata")
    return jsonify({"recurses": RecursoService.get_primeira_instancia(date, ata)}), 200


@RecuroSegundaInstanciaBlueprint.route("/recurso/segundaInstancia", methods=["GET"])
def get_recursos_segunda_instancia():
    date = request.args.get("date")
    return jsonify({"recurses": RecursoService.get_segunda_instancia(date)}), 200
