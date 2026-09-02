from flask import Blueprint, current_app, jsonify, request

from exceptions.CustomExceptions import ErrIncompleteData

AutoInfracaoBlueprint = Blueprint("infracao", __name__)


@AutoInfracaoBlueprint.route("/infracao/csv", methods=["POST"])
def post_csv():
    if "file" not in request.files:
        raise ErrIncompleteData(
            "Arquivo CSV de infrações não está presente na requisição", 400
        )
    file = request.files["file"]
    factory = current_app.extensions.get("parser_factory")
    if not factory:
        raise ErrIncompleteData("ParserFactory not configured", 500)
    extractor = factory.create_infracoes_csv_parser(ignore=True)
    metrics = extractor.extract(file.stream)
    return jsonify(
        {"message": f"{metrics.get('inserted', 0)} autos de infração importados"}
    ), 200


@AutoInfracaoBlueprint.route("/infracao/xls", methods=["POST"])
def post_xls():
    if "file" not in request.files:
        raise ErrIncompleteData(
            "Arquivo XLS de infrações não está presente na requisição", 400
        )
    file = request.files["file"]
    insert_ignore = str(request.args.get("insert_ignore", "true")).lower() == "true"
    factory = current_app.extensions.get("parser_factory")
    if not factory:
        raise ErrIncompleteData("ParserFactory not configured", 500)
    extractor = factory.create_infracoes_xls_parser(ignore=insert_ignore)
    metrics = extractor.extract(file.stream)
    return jsonify(
        {"message": f"{metrics.get('inserted', 0)} autos inseridos com sucesso"}
    ), 200


@AutoInfracaoBlueprint.route("/infracao", methods=["GET"])
def get_infracoes():
    date = request.args.get("date")
    ai = request.args.get("ai")

    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    service = factory.get_autoinfracao_service()

    return jsonify({"autos": service.get_infracoes(date, ai)}), 200


@AutoInfracaoBlueprint.route("/infracao/check", methods=["POST"])
def check_infracoes():
    if "file" not in request.files:
        raise ErrIncompleteData(
            "Arquivo CSV de infrações não está presente na requisição", 400
        )

    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    service = factory.get_autoinfracao_service()

    db_rows, file_rows, rows_not_present = service.check_infracoes(
        request.files["file"]
    )
    return jsonify(
        {
            "db_rows": f"{db_rows} Entries found in Database",
            "file_rows": f"{file_rows} Rows present in File",
            "Not Present": f"{rows_not_present}",
        }
    ), 200
