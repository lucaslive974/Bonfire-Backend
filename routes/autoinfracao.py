from flask import Blueprint, jsonify, request
from exceptions.CustomExceptions import CustomException, ErrIncompleteData
from handlers import infracoes

AutoInfracaoBlueprint = Blueprint('infracao', __name__)

@AutoInfracaoBlueprint.route("/infracao/csv", methods=["POST"])
def post_csv():
    try:
        if 'file' not in request.files:
            raise ErrIncompleteData("Arquivo CSV de infrações não está presente na requisição", 400)
        file = request.files['file']
        response = infracoes.insert_infracoes_csv(file)
        return jsonify({"message": f"{response} autos de infração importados"}), 200

    except CustomException as e:
        return jsonify(e.to_json()), e.status

@AutoInfracaoBlueprint.route("/infracao/xls", methods=["POST"])
def post_xls():
    try:
        if 'file' not in request.files:
            raise ErrIncompleteData("Arquivo XLS de infrações não está presente na requisição", 400)
        file = request.files['file']
        insert_ignore_val = request.args.get("insert_ignore", "true")
        insert_ignore = str(insert_ignore_val).lower() == "true"
        response = infracoes.insert_infracoes_xls(file, insert_ignore)
        return jsonify({"message": f"{response} autos inseridos com sucesso"}), 200
    except CustomException as e:

        return jsonify(e.to_json()), e.status


@AutoInfracaoBlueprint.route("/infracao", methods=["GET"])
def get_infracoes():
    try:
        date = request.args.get('date')
        ai = request.args.get('ai')
        result = infracoes.get_infracoes(date, ai)
        return jsonify({"autos": result}), 200
    
    except CustomException as e:
        return jsonify(e.to_json()), e.status


@AutoInfracaoBlueprint.route("/infracao/check", methods=["POST"])
def check_infracoes():
    try:
        if 'file' not in request.files:
            raise ErrIncompleteData("Arquivo CSV de infrações não está presente na requisição", 400)
        file = request.files['file']
        db_rows, file_rows, rows_not_present = infracoes.check_infracoes(file)
        return jsonify({"db_rows": f"{db_rows} Entries found in Database", "file_rows": f"{file_rows} Rows present in File", "Not Present": f"{rows_not_present}"}), 200
    except CustomException as e:
        return jsonify(e.to_json()), e.status