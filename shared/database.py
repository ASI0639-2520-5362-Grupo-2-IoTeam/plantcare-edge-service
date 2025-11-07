from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:JjRCdGmBhdwimMqGtkJuUyIWIQJLdUtd@trolley.proxy.rlwy.net:31272/railway"

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
