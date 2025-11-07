from plant.domain.services import PlantService
from plant.infrastructure.repositories import PlantRepository


class PlantApplicationService:
    """
    Application service for handling plant-related use cases.
    """

    def __init__(self, plant_service: PlantService, plant_repository: PlantRepository):
        self.plant_service = plant_service
        self.plant_repository = plant_repository

    def add_plant_data(self, data: dict) -> dict:
        """
        Adds new plant data.

        Args:
            data: A dictionary containing the plant data.

        Returns:
            A dictionary containing the saved plant data.
        """
        plant = self.plant_service.process_plant_data(data)
        saved_plant = self.plant_repository.save(plant)
        return saved_plant.__dict__
