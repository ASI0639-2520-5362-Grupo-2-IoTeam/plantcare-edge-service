from flask import Blueprint, request, jsonify

from plant.application.services import PlantApplicationService
from plant.domain.services import PlantService
from plant.infrastructure.repositories import SQLAlchemyPlantRepository
from shared.database import get_db_session

plant_blueprint = Blueprint("plant", __name__)


def _get_plant_application_service() -> PlantApplicationService:
    """
    Creates and returns an instance of the PlantApplicationService,
    injecting its dependencies.
    """
    db_session = next(get_db_session())
    plant_repository = SQLAlchemyPlantRepository(db_session=db_session)
    plant_service = PlantService()
    return PlantApplicationService(
        plant_service=plant_service, plant_repository=plant_repository
    )


@plant_blueprint.route("/plants", methods=["GET"])
def get_all_plants():
    """
    Retrieves all plant data records.
    Returns a list of all sensor data stored in the database,
    ordered by creation date in descending order.
    ---
    tags:
      - Plants
    responses:
      200:
        description: A list of all plant data records.
        schema:
          type: array
          items:
            $ref: '#/definitions/Plant'
    """
    plant_application_service = _get_plant_application_service()
    all_data = plant_application_service.get_all_plant_data()
    return jsonify(all_data)


@plant_blueprint.route("/plants", methods=["POST"])
def add_plant_data():
    """
    Endpoint to add new plant data.
    ---
    tags:
      - Plants
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: "#/definitions/PlantData"
    responses:
      200:
        description: Data successfully saved locally.
        schema:
          $ref: '#/definitions/Plant'
      400:
        description: Invalid JSON or missing required fields.
    definitions:
      PlantData:
        type: object
        required:
          - device_id
          - air_temperature_celsius
          - air_humidity_percent
          - luminosity_lux
          - soil_moisture_percent
        properties:
          device_id:
            type: string
            description: The unique ID of the IoT device.
            example: "esp32-100100C40A24"
          air_temperature_celsius:
            type: number
            description: The air temperature recorded in degrees Celsius.
            example: 25.5
          air_humidity_percent:
            type: number
            description: The air humidity recorded as a percentage.
            example: 60.2
          luminosity_lux:
            type: integer
            description: The light level recorded in lux.
            example: 850
          soil_moisture_percent:
            type: integer
            description: The soil moisture recorded as a percentage.
            example: 75
      Plant:
        type: object
        properties:
          device_id:
            type: string
          temperature:
            type: number
          humidity:
            type: number
          light:
            type: integer
          soil_humidity:
            type: integer
          created_at:
            type: string
            format: date-time
    """
    data = request.get_json()
    required_fields = [
        "device_id",
        "air_temperature_celsius",
        "air_humidity_percent",
        "luminosity_lux",
        "soil_moisture_percent",
    ]

    if not data or not all(k in data for k in required_fields):
        return jsonify({"message": "Invalid JSON or missing required fields."}), 400

    plant_application_service = _get_plant_application_service()
    saved_plant_data = plant_application_service.add_plant_data(data)

    return jsonify(saved_plant_data), 200

