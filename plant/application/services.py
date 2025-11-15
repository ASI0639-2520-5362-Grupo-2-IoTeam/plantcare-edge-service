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

    def _plant_to_dto(self, plant) -> Dict:
        """
        Converts a Plant object to a dictionary (DTO) with original field names.
        """
        return {
            "device_id": plant.device_id,
            "air_temperature_celsius": plant.temperature,
            "air_humidity_percent": plant.humidity,
            "luminosity_lux": plant.light,
            "soil_moisture_percent": plant.soil_humidity,
            "created_at": plant.created_at
        }

    def add_plant_data(self, data: dict) -> dict:
        """
        Adds new plant data and returns a dictionary representation without the internal ID.
        """
        plant = self.plant_service.process_plant_data(data)
        saved_plant = self.plant_repository.save(plant)
        return self._plant_to_dto(saved_plant)

    def get_all_plant_data(self) -> List[Dict]:
        """
        Retrieves all plant data records, excluding the internal ID from the representation.
        """
        all_plants = self.plant_repository.get_all()
        return [self._plant_to_dto(plant) for plant in all_plants]
