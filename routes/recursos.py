from flask import Blueprint, current_app, jsonify, request

from exceptions.CustomExceptions import ErrIncompleteData

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
    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    service = factory.get_recurso_service()
    metrics = service.extract_primeira_instancia(file.stream)
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
    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    service = factory.get_recurso_service()
    metrics = service.extract_segunda_instancia(file.stream)
    return jsonify(
        {
            "message": "itens Extraídos e armazenados com sucesso!",
            "counter": metrics.get("inserted", 0),
        }
    ), 200


def _get_service():
    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    return factory.get_recurso_service()


@RecursoPrimeiraInstanciaBlueprint.route("/recurso/primeiraInstancia", methods=["GET"])
def get_recursos_primeira_instancia():
    date = request.args.get("date")
    ata = request.args.get("ata")
    service = _get_service()
    return jsonify({"recurses": service.get_primeira_instancia(date, ata)}), 200


@RecuroSegundaInstanciaBlueprint.route("/recurso/segundaInstancia", methods=["GET"])
def get_recursos_segunda_instancia():
    date = request.args.get("date")
    service = _get_service()
    return jsonify({"recurses": service.get_segunda_instancia(date)}), 200
