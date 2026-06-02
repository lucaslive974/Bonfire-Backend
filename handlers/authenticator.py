from abc import abstractmethod, ABC
from datetime import datetime, timezone
from typing import override, Any

from handlers.log import logger

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


from classes.Config import config
from keycloak import KeycloakOpenID, KeycloakRPTNotFound

class KeyCloakAuthenticator(Authenticator):
    def __init__(self):
        logger.info("::Configuring Keycloak session::")
        self.keycloakOpenId = KeycloakOpenID(f"{config.envs['KEYCLOAK_ISSUER']}/auth",
                                config.envs["KEYCLOAK_REALM_NAME"],
                                config.envs["KEYCLOAK_CLIENT_ID"],
                                config.envs["KEYCLOAK_CLIENT_SECRET"])
        logger.info("::Keycloak connection estabilished::")

    @override
    def getTimestamp(self) -> float:
        return datetime.now(timezone.utc).timestamp()


    @override
    def isAuthenticated(self, token: str) -> bool:
        try:
            [ method, token ] = token.split(' ')
            if method != "Bearer":
                return False

            token_info: dict[str, Any] = self.keycloakOpenId.decode_token(token)
            now = self.getTimestamp()

            # Safely get the exp, ensuring it defaults to 0 if not present
            exp_val = token_info.get('exp', 0)
            exp = float(exp_val) if isinstance(exp_val, (int, float, str)) else 0.0

            return bool(now < exp)
        except:
            return False

    @override
    def checkConnection(self) -> None:
        try:
            logger.info("::Checking Keycloak connection::")
            #Try to get well-know form the server
            _ = self.keycloakOpenId.well_known()
        except KeycloakRPTNotFound as e:
            logger.error("::Keycloak connection failed::")
            logger.error(str(e.error_message))
            raise
