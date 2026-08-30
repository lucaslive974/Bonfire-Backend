from os import getenv

from exceptions.CustomExceptions import ErrMissingRequiredEnv


class Config:
    DB_DRIVER: str = "mysql"
    DB_HOST: str = "bonfire-db"
    DB_PORT: str = "3306"
    DB_NAME: str = "bonfire"
    DB_USER: str = "bonfire"
    DB_PASSWORD: str | None = None

    # auth
    KEYCLOAK_ISSUER: str = "http://keycloak:8080"
    KEYCLOAK_CLIENT_ID: str = "bonfire"
    KEYCLOAK_CLIENT_SECRET: str | None = None
    KEYCLOAK_REALM_NAME: str | None = None

    def __init__(self):
        for env in self:
            value = getenv(env, self[env])
            if not value:
                raise ErrMissingRequiredEnv("ERROR::Missing required env: " + env)

            self[env] = value

    def __iter__(self):
        for attr in self.__class__.__dict__:
            if not attr.startswith("_"):
                val = getattr(self, attr)
                if not callable(val):
                    yield attr

    def __getitem__(self, item: str):
        try:
            val = getattr(self, item)
            if callable(val):
                raise AttributeError
            return val
        except AttributeError:
            raise KeyError(f"Variável de configuração '{item}' não encontrada.")

    def __setitem__(self, key: str, value):
        try:
            if not hasattr(self, key) or key.startswith("_"):
                raise AttributeError

            if callable(getattr(self, key)):
                raise AttributeError

            setattr(self, key, value)

        except AttributeError:
            raise KeyError(f"Não é permitido definir/alterar a variável '{key}'.")


config = Config()
