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
        Adds new plant data and returns a dictionary representation without the internal ID.
        """
        plant = self.plant_service.process_plant_data(data)
        saved_plant = self.plant_repository.save(plant)
        # Manually create dictionary to exclude 'id'
        return {
            "device_id": saved_plant.device_id,
            "temperature": saved_plant.temperature,
            "humidity": saved_plant.humidity,
            "light": saved_plant.light,
            "soil_humidity": saved_plant.soil_humidity,
            "created_at": saved_plant.created_at
        }

    def get_all_plant_data(self) -> List[Dict]:
        """
        Retrieves all plant data records, excluding the internal ID from the representation.
        """
        all_plants = self.plant_repository.get_all()
        # Manually create list of dictionaries to exclude 'id'
        return [
            {
                "device_id": plant.device_id,
                "temperature": plant.temperature,
                "humidity": plant.humidity,
                "light": plant.light,
                "soil_humidity": plant.soil_humidity,
                "created_at": plant.created_at
            }
            for plant in all_plants
        ]
