import io
from typing import BinaryIO, Optional

import pytest
from flask import Flask, current_app, jsonify, request

from exceptions.CustomExceptions import CustomException
from services.document_parser.core import (
    DocumentExtractor,
    DocumentParserFactory,
    ExtractionObserver,
)
from services.document_parser.exceptions import (
    DocumentParsingError,
)


class MockExtractor(DocumentExtractor):
    def __init__(self, succeed=True):
        self.succeed = succeed

    def extract(
        self, file_stream: BinaryIO, observer: Optional[ExtractionObserver] = None
    ) -> None:
        if not self.succeed:
            raise DocumentParsingError("Simulated parsing error")
        if observer:
            observer.on_event("row_processed")
            observer.on_event("row_processed")
            observer.on_event("warning", "A minor issue")
            observer.on_event("status_change", "completed")


class MockParserFactory(DocumentParserFactory):
    def create_primeira_instancia_parser(self) -> DocumentExtractor:
        return MockExtractor(succeed=True)

    def create_segunda_instancia_parser(self) -> DocumentExtractor:
        return MockExtractor(succeed=True)

    def create_infracoes_csv_parser(self) -> DocumentExtractor:
        return MockExtractor(succeed=True)

    def create_infracoes_xls_parser(self, ignore: bool = False) -> DocumentExtractor:
        return MockExtractor(succeed=False)  # Simulate fail for testing


@pytest.fixture
def test_app():
    app = Flask("TestApp")

    @app.errorhandler(CustomException)
    def _handle_custom_exception(e):
        return jsonify(dict(e)), e.status

    if not hasattr(app, "extensions"):
        app.extensions = {}
    app.extensions["parser_factory"] = MockParserFactory()

    @app.route("/upload/primeira", methods=["POST"])
    def upload_primeira():
        if "document" not in request.files:
            return jsonify({"error": "No document"}), 400

        file = request.files["document"]
        factory = current_app.extensions["parser_factory"]
        extractor = factory.create_primeira_instancia_parser()

        observer = ExtractionObserver()
        extractor.extract(file.stream, observer)
        return jsonify(observer.metrics), 200

    @app.route("/upload/xls", methods=["POST"])
    def upload_xls():
        if "document" not in request.files:
            return jsonify({"error": "No document"}), 400

        file = request.files["document"]
        factory = current_app.extensions["parser_factory"]
        extractor = factory.create_infracoes_xls_parser()

        observer = ExtractionObserver()
        extractor.extract(file.stream, observer)
        return jsonify(observer.metrics), 200

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
    assert response.json["warnings"] == ["A minor issue"]
    assert response.json["status"] == "completed"


def test_parsing_error(client):
    data = {"document": (io.BytesIO(b"dummy content"), "test.xls")}
    response = client.post("/upload/xls", data=data, content_type="multipart/form-data")
    assert response.status_code == 422
    assert response.json["error"] == "Parsing Error"
