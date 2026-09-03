from flask import Flask, Response, current_app, jsonify, request
from flask_cors import CORS

from core.auth import Authenticator, KeyCloakAuthenticator
from core.cache import InMemoryCache
from core.parsers.factory import ParserFactory
from exceptions.CustomExceptions import CustomException
from routes.spec import spec
from routes.v1 import autoinfracao, consorcio, linha, recursos, veiculos
from utils.logger import http_logger, logger


class BonfireApp(Flask):
    _authController: Authenticator

    def __init__(self, name: str) -> None:
        logger.info("::Initializing bonfire application::")
        super().__init__(name)
        CORS(self)

        logger.info("::Registering routes::")
        secured_blueprints = [
            autoinfracao.AutoInfracaoBlueprint,
            recursos.RecursoPrimeiraInstanciaBlueprint,
            recursos.RecuroSegundaInstanciaBlueprint,
            veiculos.veiculoBlueprint,
            linha.linhaBlueprint,
            consorcio.consorcioBlueprint,
        ]

        def _blueprint_auth():
            if hasattr(current_app, "checkAuth"):
                return current_app.checkAuth()
            return None

        for bp in secured_blueprints:
            if not bp._got_registered_once:
                bp.before_request(_blueprint_auth)
            # Register versioned routes at /v1/...
            self.register_blueprint(bp, url_prefix="/v1")
            # Register legacy un-prefixed routes for backward compatibility
            self.register_blueprint(bp, name=f"{bp.name}_legacy")

        # Initialize Application Cache
        self.extensions["cache"] = InMemoryCache()

        # Initialize Data Access and Domain Services
        from repositories.manager import SQLAlchemyRepositoryManager
        from services.factory import ServiceFactory

        db_manager = SQLAlchemyRepositoryManager()
        self.extensions["db_manager"] = db_manager
        # Initialize Document Parser Factory
        if not hasattr(self, "extensions"):
            self.extensions = {}
        parser_factory = ParserFactory(db_manager)
        self.extensions["parser_factory"] = parser_factory

        self.extensions["service_factory"] = ServiceFactory(db_manager, parser_factory)

        db_manager.check_connection()
        self._authController = KeyCloakAuthenticator(cache=self.extensions["cache"])
        self._authController.checkConnection()

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

        @self.after_request
        def _(response: Response):
            return self.logRequest(response)

        # Register OpenAPI SpecTree
        spec.register(self)

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


def createBonfireApp():
    return BonfireApp("__main__")
