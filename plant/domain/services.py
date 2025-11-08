from plant.domain.entities import Plant


class PlantService:
    """
    Domain service for handling plant-related operations.
    """

    def process_plant_data(self, data: dict) -> Plant:
        """
        Processes raw plant data and returns a Plant entity.

        Args:
            data: A dictionary containing the plant data.

        Returns:
            A Plant entity.
        """
        return Plant(
            id=None,  # The ID will be assigned by the database
            device_id=data["device_id"],  # <-- AÑADIDO
            temperature=data["temperature"],
            humidity=data["humidity"],
            light=data["light"],
            soil_humidity=data["soil_humidity"],
            created_at=None  # The creation date will be assigned by the database
        )
