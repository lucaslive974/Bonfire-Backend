from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

from classes.Config import config
from exceptions.CustomExceptions import ErrCreatingDbConnection, ErrInvalidDbConfig
from repositories.autoinfracao_repository import AutoInfracaoRepository
from repositories.consorcio_repository import ConsorcioRepository
from repositories.interfaces import (
    IAutoInfracaoRepository,
    IConsorcioRepository,
    ILinhaRepository,
    IRecursoRepository,
    IRepositoryManager,
    IRepositorySession,
    IVeiculoRepository,
)
from repositories.linha_repository import LinhaRepository
from repositories.recurso_repository import RecursoRepository
from repositories.veiculo_repository import VeiculoRepository
from utils.logger import logger


class SQLAlchemySession(IRepositorySession):
    def __init__(self, session):
        self._session = session

    def __enter__(self) -> "IRepositorySession":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self._session.rollback()
            else:
                self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        finally:
            self._session.close()

    def get_autoinfracao_repository(self) -> IAutoInfracaoRepository:
        return AutoInfracaoRepository(self._session)

    def get_veiculo_repository(self) -> IVeiculoRepository:
        return VeiculoRepository(self._session)

    def get_linha_repository(self) -> ILinhaRepository:
        return LinhaRepository(self._session)

    def get_consorcio_repository(self) -> IConsorcioRepository:
        return ConsorcioRepository(self._session)

    def get_recurso_repository(self) -> IRecursoRepository:
        return RecursoRepository(self._session)


class SQLAlchemyRepositoryManager(IRepositoryManager):
    def __init__(self):
        self._engine = None
        self._session_factory = None

    def _get_engine(self):
        if self._engine is None:
            driver = config.DB_DRIVER
            host = config.DB_HOST
            port = config.DB_PORT
            database = config.DB_NAME
            user = config.DB_USER
            password = config.DB_PASSWORD

            if None in (driver, host, database, user, password):
                raise ErrInvalidDbConfig(
                    "Algumas configurações do banco de dados estão ausentes ou configuradas incorretamente",
                    401,
                )

            import urllib.parse

            escaped_password = urllib.parse.quote_plus(password) if password else ""
            db_url = (
                f"mysql+pymysql://{user}:{escaped_password}@{host}:{port}/{database}"
            )

            try:
                self._engine = create_engine(
                    db_url, pool_recycle=3600, pool_pre_ping=True
                )
            except Exception as e:
                logger.systemLog(e)
                raise ErrCreatingDbConnection(
                    "Não foi possível estabelecer uma conexão com o banco de dados", 500
                )
        return self._engine

    def _get_session_factory(self):
        if self._session_factory is None:
            engine = self._get_engine()
            self._session_factory = scoped_session(
                sessionmaker(autocommit=False, autoflush=False, bind=engine)
            )
        return self._session_factory

    @contextmanager
    def session(self) -> IRepositorySession:
        factory = self._get_session_factory()
        session_instance = factory()
        sql_session = SQLAlchemySession(session_instance)
        with sql_session as s:
            yield s
        # Remove the session from the registry so scoped_session cleans it up
        factory.remove()

    def check_connection(self) -> None:
        logger.info("::Testing database connection::")
        try:
            engine = self._get_engine()
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                self._print_database_connection()
                logger.info("::Database connection successful::")
        except Exception as e:
            logger.systemLog(f"Database connection check failed: {e}")
            raise ErrCreatingDbConnection("Erro ao conectar no banco de dados", 500)

    def _print_database_connection(self) -> None:
        logger.info(
            f"""
|===============================================
| Database Connection Details
| Driver:   {config.DB_DRIVER}
| Host:     {config.DB_HOST}
| Port:     {config.DB_PORT}
| Database: {config.DB_NAME}
| User:     {config.DB_USER}
| Password: **************
|===============================================
"""
        )
