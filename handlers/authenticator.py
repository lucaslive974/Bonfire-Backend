"""Compatibilidade retroativa: delegando para services.authenticator."""
from services.authenticator import Authenticator, KeyCloakAuthenticator

__all__ = [
    "Authenticator",
    "KeyCloakAuthenticator",
]
