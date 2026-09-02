import io
from typing import BinaryIO

import pytest
from flask import Flask, current_app, jsonify, request

from exceptions.CustomExceptions import CustomException
from core.parsers.core import DocumentExtractor
from core.parsers.exceptions import DocumentParsingError


class MockExtractor(DocumentExtractor):
    def __init__(self, succeed=True):
        self.succeed = succeed

    def extract(self, file_stream: BinaryIO) -> dict:
        if not self.succeed:
            raise DocumentParsingError("Parsing Error")
        return {
            "rows_processed": 2,
            "warnings": ["A minor issue"],
            "status": "completed",
        }


class MockParserFactory:
    def create_primeira_instancia_parser(self) -> DocumentExtractor:
        return MockExtractor(succeed=True)

    def create_segunda_instancia_parser(self) -> DocumentExtractor:
        return MockExtractor(succeed=True)

    def create_infracoes_csv_parser(self) -> DocumentExtractor:
        return MockExtractor(succeed=True)

    def create_infracoes_xls_parser(self, ignore: bool = False) -> DocumentExtractor:
        return MockExtractor(succeed=False)


@pytest.fixture
def test_app():
    app = Flask("TestApp")

    @app.errorhandler(CustomException)
    def _handle_custom_exception(e):
        return jsonify(dict(e)), e.status

    @app.errorhandler(DocumentParsingError)
    def _handle_doc_exception(e):
        return jsonify({"error": str(e)}), 422

    if not hasattr(app, "extensions"):
        app.extensions = {}
    app.extensions["parser_factory"] = MockParserFactory()

    @app.route("/upload/primeira", methods=["POST"])
    def upload_primeira():
        file = request.files["document"]
        factory = current_app.extensions["parser_factory"]
        extractor = factory.create_primeira_instancia_parser()
        metrics = extractor.extract(file.stream)
        return jsonify(metrics), 200

    @app.route("/upload/xls", methods=["POST"])
    def upload_xls():
        file = request.files["document"]
        factory = current_app.extensions["parser_factory"]
        extractor = factory.create_infracoes_xls_parser()
        metrics = extractor.extract(file.stream)
        return jsonify(metrics), 200

    return app


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_successful_extraction(client):
    data = {"document": (io.BytesIO(b"dummy content"), "test.docx")}
    response = client.post(
        "/upload/primeira", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert response.json["rows_processed"] == 2


def test_parsing_error(client):
    data = {"document": (io.BytesIO(b"dummy content"), "test.xls")}
    response = client.post("/upload/xls", data=data, content_type="multipart/form-data")
    assert response.status_code == 422
    assert response.json["error"] == "Parsing Error"
