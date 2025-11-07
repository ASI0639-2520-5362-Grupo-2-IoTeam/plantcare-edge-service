import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Lee la URL de la base de datos desde una variable de entorno.
# Proporciona una URL por defecto para desarrollo local si la variable no está definida.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Session:
    """
    Provides a database session to the application.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
