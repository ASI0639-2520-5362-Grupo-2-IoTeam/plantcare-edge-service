from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class PlantModel(Base):
    """
    SQLAlchemy model for the 'plants' table.
    """
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True)
    device_id = Column(String(50), nullable=False, index=True)  # <-- AÑADIDO
    temperature = Column(Float)
    humidity = Column(Float)
    light = Column(Integer)
    soil_humidity = Column(Integer)
    created_at = Column(DateTime, default=func.now())
