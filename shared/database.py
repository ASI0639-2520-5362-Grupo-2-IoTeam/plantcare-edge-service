import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# --- Configuración de la Base de Datos lista para Producción ---

# Intenta obtener la URL completa desde las variables de entorno (típico de Render/Railway)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Si la URL de producción es para MySQL pero no especifica el driver,
    # la modificamos para que use pymysql, que es el que tenemos instalado.
    if DATABASE_URL.startswith("mysql://"):
        DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
else:
    # Si no hay DATABASE_URL, construimos una para desarrollo local
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "plant_database")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


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
