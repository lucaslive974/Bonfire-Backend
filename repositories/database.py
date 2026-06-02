from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from exceptions.CustomExceptions import ErrInvalidDbConfig, ErrCreatingDbConnection
from classes.Config import config
from handlers.log import logger

_engine = None
_SessionLocal = None


def get_engine():
    """Lazily initializes and returns the SQLAlchemy engine."""
    global _engine
    if _engine is None:
        db_config = config.envs
        driver = db_config.get("DB_DRIVER")
        host = db_config.get("DB_HOST")
        port = db_config.get("DB_PORT")
        database = db_config.get("DB_NAME")
        user = db_config.get("DB_USER")
        password = db_config.get("DB_PASSWORD")

        if None in (driver, host, database, user, password):
            raise ErrInvalidDbConfig(
                "Algumas configurações do banco de dados estão ausentes ou configuradas incorretamente",
                401,
            )

        db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

        try:
            # Use SQLAlchemy connection pool, pre-ping to check connection viability
            _engine = create_engine(db_url, pool_recycle=3600, pool_pre_ping=True)
        except Exception as e:
            logger.systemLog(e)
            raise ErrCreatingDbConnection(
                "Não foi possível estabelecer uma conexão com o banco de dados", 500
            )
    return _engine


def get_session_local():
    """Lazily initializes and returns the scoped session factory."""
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
    return _SessionLocal


def print_connection_data():
    db_config = config.envs
    logger.info(f"""
|===============================================
|Database Information                        
|Driver: {db_config.get("DB_DRIVER")}         
|Host: {db_config.get("DB_HOST")}             
|Port: {db_config.get("DB_PORT")}             
|Database: {db_config.get("DB_NAME")}     
|User: {db_config.get("DB_USER")}
|Password: **************
|===============================================
    """)


def check_database_connection():
    logger.info("::Testing database connection::")
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print_connection_data()
            logger.info("::Database connection succesfull::")
    except Exception as e:
        logger.systemLog(e)
        raise ErrCreatingDbConnection("Erro ao conectar no banco de dados", 500)


@contextmanager
def get_db():
    """Provides a transactional scope around a series of operations."""
    session_factory = get_session_local()
    db = session_factory()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
