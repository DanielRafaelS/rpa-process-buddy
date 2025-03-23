from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pathlib import Path

Base = declarative_base()
_engine = None
_SessionLocal = None


def get_database_url() -> str:
    """
    Builds the SQLite database URL and ensures the data directory exists.

    Returns:
        str: SQLite connection URL.
    """
    db_file = Path("data/database.sqlite")
    db_file.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{db_file}"


def get_engine() -> any:
    """
    Creates and returns the SQLAlchemy engine.

    Returns:
        Engine: SQLAlchemy engine instance.
    """
    global _engine
    if _engine is None:
        _engine = create_engine(
            get_database_url(),
            connect_args={"check_same_thread": False}
        )
    return _engine


def get_session() -> Session:
    """
    Creates and returns a new database session.

    Returns:
        Session: SQLAlchemy session object.
    """
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal()


def create_tables() -> None:
    """
    Creates database tables based on the defined models.
    """
    Base.metadata.create_all(bind=get_engine())
