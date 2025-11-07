from plant.domain.services import PlantService
from plant.infrastructure.repositories import PlantRepository
from typing import List, Dict

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
        """
        plant = self.plant_service.process_plant_data(data)
        saved_plant = self.plant_repository.save(plant)
        return saved_plant.__dict__

    def get_all_plant_data(self) -> List[Dict]:
        """
        Retrieves all plant data records.
        """
        all_plants = self.plant_repository.get_all()
        return [plant.__dict__ for plant in all_plants]
