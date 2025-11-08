from flask import Blueprint, request, jsonify
from flasgger import swag_from
from plant.application.services import PlantApplicationService
from plant.domain.services import PlantService
from plant.infrastructure.repositories import SQLAlchemyPlantRepository
from shared.database import get_db_session

plant_blueprint = Blueprint("plant", __name__)


@plant_blueprint.route("/plants", methods=["GET"])
def get_all_plants():
    """
    Obtiene todos los registros de datos de plantas.
    Devuelve una lista de todos los datos de sensores guardados en la base de datos,
    ordenados por fecha de creación descendente.
    ---
    tags:
      - Plants
    responses:
      200:
        description: Una lista de todos los registros de datos de plantas.
        schema:
          type: array
          items:
            $ref: '#/definitions/Plant'
    """
    db_session = next(get_db_session())
    plant_repository = SQLAlchemyPlantRepository(db_session=db_session)
    plant_service = PlantService()
    plant_application_service = PlantApplicationService(
        plant_service=plant_service, plant_repository=plant_repository
    )

    all_data = plant_application_service.get_all_plant_data()
    return jsonify(all_data)


@plant_blueprint.route("/plants", methods=["POST"])
def add_plant_data():
    """
    Endpoint para añadir nuevos datos de una planta.
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
        description: Datos guardados localmente exitosamente.
      400:
        description: Error en la petición, JSON inválido o datos faltantes.
    definitions:
      PlantData:
        type: object
        required:
          - device_id
          - temperature
          - humidity
          - light
          - soil_humidity
        properties:
          device_id:
            type: string
            description: El ID único del dispositivo IoT.
            example: "esp32-100100C40A24"
          temperature:
            type: number
            description: La temperatura registrada.
            example: 25.5
          humidity:
            type: number
            description: La humedad ambiental registrada.
            example: 60.2
          light:
            type: integer
            description: El nivel de luz registrado.
            example: 850
          soil_humidity:
            type: integer
            description: La humedad del suelo registrada.
            example: 75
      Plant:
        type: object
        properties:
          id:
            type: integer
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
    if not data or not all(k in data for k in ["device_id", "temperature", "humidity", "light", "soil_humidity"]):
        return jsonify({"message": "JSON inválido o faltan campos requeridos."}), 400

    db_session = next(get_db_session())
    plant_repository = SQLAlchemyPlantRepository(db_session=db_session)
    plant_service = PlantService()
    plant_application_service = PlantApplicationService(
        plant_service=plant_service, plant_repository=plant_repository
    )
        
    saved_plant_data = plant_application_service.add_plant_data(data)

    return jsonify({
        "message": "Datos guardados exitosamente.",
        "saved_data": saved_plant_data
    }), 200
