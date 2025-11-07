import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# --- Configuración de la Base de Datos lista para Producción ---

# Lee las credenciales desde variables de entorno.
# Proporciona valores por defecto para el desarrollo local.
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "plant_database")

# Construye la URL de la base de datos.
# Railway puede proporcionar una URL completa o partes individuales.
# Este enfoque es flexible.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

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
