from abc import abstractmethod, ABC
from datetime import datetime, timezone
from typing import override, Any

from keycloak import KeycloakOpenID
from classes.Config import config
from utils.logger import logger


class Authenticator(ABC):
    @abstractmethod
    def isAuthenticated(self, token: str) -> bool:
        pass

    @abstractmethod
    def getTimestamp(self) -> float:
        pass

    @abstractmethod
    def checkConnection(self) -> None:
        pass


class KeyCloakAuthenticator(Authenticator):
    def __init__(self):
        logger.info("::Configuring Keycloak session::")
        self.keycloakOpenId = KeycloakOpenID(
            f"{config.KEYCLOAK_ISSUER}/auth",
            config.KEYCLOAK_REALM_NAME or "",
            config.KEYCLOAK_CLIENT_ID,
            config.KEYCLOAK_CLIENT_SECRET,
        )
        logger.info("::Keycloak connection established::")

    @override
    def getTimestamp(self) -> float:
        return datetime.now(timezone.utc).timestamp()

    @override
    def isAuthenticated(self, token: str) -> bool:
        try:
            token_info: dict[str, Any] = self.keycloakOpenId.decode_token(token)
            now = self.getTimestamp()

            # Safely get the exp, ensuring it defaults to 0 if not present
            exp_val = token_info.get('exp', 0)
            exp = float(exp_val) if isinstance(exp_val, (int, float, str)) else 0.0

            return bool(now < exp)
        except Exception as e:
            logger.systemLog(f"Erro na autenticação do token: {e}")
            return False

    @override
    def checkConnection(self) -> None:
        try:
            logger.info("::Checking Keycloak connection::")
            # Try to get well-known info from the server
            _ = self.keycloakOpenId.well_known()
        except Exception as e:
            logger.error("::Keycloak connection failed::")
            logger.error(str(e))
            raise
