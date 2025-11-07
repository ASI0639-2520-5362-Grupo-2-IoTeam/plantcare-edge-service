from abc import ABC, abstractmethod
from plant.domain.entities import Plant
from plant.infrastructure.models import PlantModel
from sqlalchemy.orm import Session


class PlantRepository(ABC):
    """
    Abstract base class for a plant repository.
    """

    @abstractmethod
    def save(self, plant: Plant) -> Plant:
        """
        Saves a plant entity to the repository.

        Args:
            plant: The plant entity to save.

        Returns:
            The saved plant entity.
        """
        pass


class SQLAlchemyPlantRepository(PlantRepository):
    """
    SQLAlchemy implementation of the plant repository.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, plant: Plant) -> Plant:
        """
        Saves a plant entity to the database.
        """
        plant_model = PlantModel(
            temperature=plant.temperature,
            humidity=plant.humidity,
            light=plant.light,
            soil_humidity=plant.soil_humidity,
        )
        self.db_session.add(plant_model)
        self.db_session.commit()
        self.db_session.refresh(plant_model)
        return Plant(
            id=plant_model.id,
            temperature=plant_model.temperature,
            humidity=plant_model.humidity,
            light=plant_model.light,
            soil_humidity=plant_model.soil_humidity,
            created_at=plant_model.created_at,
        )
