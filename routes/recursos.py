from flask import Blueprint, jsonify, request
from tempfile import NamedTemporaryFile
from exceptions.CustomExceptions import ErrIncompleteData
from services.recurso_service import RecursoService

RecursoPrimeiraInstanciaBlueprint = Blueprint('recursoPrimeiraInstancia', __name__)

from flask import current_app
from services.document_parser.core import ExtractionObserver
from services.document_parser.exceptions import UnsupportedFormatError, DocumentParsingError

@RecursoPrimeiraInstanciaBlueprint.route("/recurso/primeiraInstancia/resultado", methods=["POST"])
def postResultadoPrimeiraInstancia():
    if 'file' not in request.files:
        raise ErrIncompleteData("Arquivo de resultado de primeira instancia não está presente na requisição", 400)

    file = request.files['file']
    factory = current_app.extensions.get('parser_factory')
    
    if not factory:
        raise ErrIncompleteData("ParserFactory not configured", 500)
    
    extractor = factory.create_primeira_instancia_parser()
    observer = ExtractionObserver()
    extractor.extract(file.stream, observer)
    
    return jsonify({
        "message": "itens Extraídos e armazenados com sucesso!", 
        "counter": observer.metrics.get("rows_processed", 0)
    }), 200

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
    factory = current_app.extensions.get('parser_factory')
    
    if not factory:
        raise ErrIncompleteData("ParserFactory not configured", 500)
        
    extractor = factory.create_segunda_instancia_parser()
    observer = ExtractionObserver()
    extractor.extract(file.stream, observer)
    
    return jsonify({
        "message": "itens Extraídos e armazenados com sucesso!", 
        "counter": observer.metrics.get("rows_processed", 0)
    }), 200


@RecursoPrimeiraInstanciaBlueprint.route("/recurso/segundaInstancia", methods=["GET"])
def getRecursoSegundaInstancia():
    date = request.args.get('date')
    result = RecursoService.get_segunda_instancia(date)
    return jsonify({"recurses": result }), 200
