from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import override

import jwt
import requests
from keycloak import KeycloakOpenID

from classes.Config import config
from core.cache.interface import ICache
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
    def __init__(self, cache: ICache):
        logger.info("::Configuring Keycloak Local Validator::")
        self.cache = cache
        
        self.keycloakOpenId = KeycloakOpenID(
            f"{config.KEYCLOAK_ISSUER}/auth",
            config.KEYCLOAK_REALM_NAME or "",
            config.KEYCLOAK_CLIENT_ID,
            config.KEYCLOAK_CLIENT_SECRET,
        )
        
        # O endpoint padrão do Keycloak para JWKS (Chaves Públicas)
        realm = config.KEYCLOAK_REALM_NAME or ""
        issuer = config.KEYCLOAK_ISSUER or ""
        self.certs_url = f"{issuer}/realms/{realm}/protocol/openid-connect/certs"
        
        logger.info("::Keycloak authenticator initialized::")

    def _get_public_keys(self) -> dict:
        """Fetch JWKS from our application Cache or Keycloak."""
        cache_key = "keycloak_jwks"
        keys = self.cache.get(cache_key)
        
        if keys is not None:
            return keys
            
        try:
            logger.info("::Fetching JWKS from Keycloak (Cache Miss)::")
            response = requests.get(self.certs_url, timeout=10)
            response.raise_for_status()
            keys = response.json()
            
            # Cache the JSON Web Key Set for 24 hours
            self.cache.set(cache_key, keys, ttl_seconds=86400)
            return keys
        except Exception as e:
            logger.error(f"::Failed to fetch Keycloak JWKS: {e}::")
            return {}

    @override
    def getTimestamp(self) -> float:
        return datetime.now(timezone.utc).timestamp()

    @override
    def isAuthenticated(self, token: str) -> bool:
        try:
            # 1. Decode header without verifying to extract 'kid'
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")
            if not kid:
                logger.error("Token header does not contain 'kid'")
                return False

            jwks = self._get_public_keys()
            
            # 3. Find the specific public key used for this token
            public_key = None
            for jwk_data in jwks.get("keys", []):
                if jwk_data.get("kid") == kid:
                    # Convert the JWK dictionary to an RSA key object
                    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk_data)
                    break

            if not public_key:
                logger.error("Public key not found in cached JWKS")
                return False

            # 4. Verify signature and expiration locally
            jwt.decode(
                token, 
                key=public_key, 
                algorithms=["RS256"], 
                options={"verify_aud": False} 
            )
            return True
            
        except jwt.ExpiredSignatureError:
            logger.warn("Token expired locally (401)")
            return False
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token signature: {e}")
            return False
        except Exception as e:
            logger.systemLog(f"Unexpected error during token validation: {e}")
            return False

    @override
    def checkConnection(self) -> None:
        try:
            logger.info("::Checking Keycloak connection via JWKS::")
            keys = self._get_public_keys()
            if not keys:
                raise ValueError("Could not retrieve JWKS on startup")
            logger.info("::Keycloak JWKS Cached successfully::")
        except Exception as e:
            logger.error("::Keycloak connection failed::")
            logger.error(str(e))
            raise
