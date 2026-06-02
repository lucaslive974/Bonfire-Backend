import pytest
from unittest.mock import patch
from app import BonfireApp
from flask import Blueprint
from exceptions.CustomExceptions import CustomException


@pytest.fixture
def error_app():
    with patch.object(BonfireApp, "checkAuth", return_value=None):
        application = BonfireApp("test_bonfire_errors")
        application.config.update({"TESTING": True})
        
        # Register a test blueprint with routes that raise exceptions
        test_bp = Blueprint("test_errors", __name__)
        
        @test_bp.route("/test-custom-exception")
        def _raise_custom_exception():  # pyright: ignore [reportUnusedFunction]
            raise CustomException("Custom domain error occurred", status=418, error="TEAPOT_ERROR")
            
        @test_bp.route("/test-generic-exception")
        def _raise_generic_exception():  # pyright: ignore [reportUnusedFunction]
            raise ValueError("Something unexpected went wrong")
            
        application.register_blueprint(test_bp)
        yield application


@pytest.fixture
def error_client(error_app):
    return error_app.test_client()


def test_custom_exception_handling(error_client):
    response = error_client.get("/test-custom-exception")
    assert response.status_code == 418
    data = response.get_json()
    assert data == {
        "error": "TEAPOT_ERROR",
        "message": "Custom domain error occurred",
        "status": 418
    }


def test_generic_exception_handling(error_client):
    response = error_client.get("/test-generic-exception")
    assert response.status_code == 500
    data = response.get_json()
    assert data == {
        "error": "Internal Server Error",
        "message": "Ocorreu um erro interno no servidor."
    }
