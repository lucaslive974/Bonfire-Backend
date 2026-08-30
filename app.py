from flask import Flask, Response, jsonify, request
from flask_cors import CORS

from core.auth import Authenticator, KeyCloakAuthenticator
from core.cache import InMemoryCache
from exceptions.CustomExceptions import CustomException
from repositories.database import check_database_connection
from routes import autoinfracao, consorcio, linha, recursos, veiculos
from services.document_parser.factory import PyIngestionParserFactory
from utils.logger import http_logger, logger


class BonfireApp(Flask):
    _authController: Authenticator

    def __init__(self, name: str) -> None:
        logger.info("::Initializing bonfire application::")
        super().__init__(name)
        CORS(self)

        logger.info("::Registering routes::")
        self.register_blueprint(autoinfracao.AutoInfracaoBlueprint)
        self.register_blueprint(recursos.RecursoPrimeiraInstanciaBlueprint)
        self.register_blueprint(recursos.RecuroSegundaInstanciaBlueprint)
        self.register_blueprint(veiculos.veiculoBlueprint)
        self.register_blueprint(linha.linhaBlueprint)
        self.register_blueprint(consorcio.consorcioBlueprint)

        # Initialize Application Cache
        self.extensions["cache"] = InMemoryCache()

        check_database_connection()
        self._authController = KeyCloakAuthenticator(cache=self.extensions["cache"])
        self._authController.checkConnection()

        # Initialize Document Parser Abstract Factory
        if not hasattr(self, "extensions"):
            self.extensions = {}
        self.extensions["parser_factory"] = PyIngestionParserFactory()

        # Custom domain exception handler
        @self.errorhandler(CustomException)
        def _handle_custom_exception(e: CustomException):  # pyright: ignore [reportUnusedFunction]
            logger.systemLog(f"[{e.error}] {e.message}")
            return jsonify(dict(e)), e.status

        # Generic unexpected exception handler
        @self.errorhandler(Exception)
        def _handle_generic_exception(e: Exception):  # pyright: ignore [reportUnusedFunction]
            logger.systemLog(e)
            status_code = getattr(e, "code", 500)
            return jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "Ocorreu um erro interno no servidor.",
                }
            ), status_code

        @self.before_request
        def _():
            return self.checkAuth()

        @self.after_request
        def _(response: Response):
            return self.logRequest(response)

    def logRequest(self, response: Response):
        http_logger.request(request, response.status_code)
        return response

    def checkAuth(self) -> Response | None:
        if request.method == "OPTIONS":
            return None

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response("Unauthorized", status=401)

        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            return Response("Unauthorized", status=401)

        token = parts[1]
        if not self._authController.isAuthenticated(token):
            return Response("Unauthorized", status=401)

        return None
