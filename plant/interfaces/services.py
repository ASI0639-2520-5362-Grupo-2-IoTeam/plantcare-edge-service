from flask import Blueprint, request, jsonify
from flasgger import swag_from
from plant.application.services import PlantApplicationService
# from plant.application.forwarding_service import ForwardingService  # Comentado temporalmente
from plant.domain.services import PlantService
from plant.infrastructure.repositories import SQLAlchemyPlantRepository
from shared.database import get_db_session

# --- Simulación del contexto IAM ---
def get_device_info(device_id: str) -> dict:
    if device_id == "wokwi-esp32-1":
        return {"id": device_id, "name": "Wokwi Lab Station 1", "location": "Development Lab"}
    return None
# ------------------------------------


plant_blueprint = Blueprint("plant", __name__)

@plant_blueprint.route("/plants", methods=["POST"])
def add_plant_data():
    """
    Endpoint para añadir nuevos datos de una planta. (Reenvío a backend deshabilitado temporalmente)
    ---
    tags:
      - Plants
    parameters:
      - name: X-Device-Id
        in: header
        type: string
        required: true
        description: El ID único del dispositivo IoT que envía los datos.
        default: wokwi-esp32-1
      - name: body
        in: body
        required: true
        schema:
          $ref: "#/definitions/PlantData"
    responses:
      200:
        description: Datos guardados localmente exitosamente.
      400:
        description: Error en la petición (JSON inválido o falta de cabecera).
      401:
        description: Dispositivo no autorizado.
    definitions:
      PlantData:
        type: object
        required:
          - temperature
          - humidity
          - light
          - soil_humidity
        properties:
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
    # 1. Identificar el dispositivo (Contexto IAM)
    device_id = request.headers.get("X-Device-Id")
    if not device_id:
        return jsonify({"message": "La cabecera X-Device-Id es requerida."}), 400

    device_info = get_device_info(device_id)
    if not device_info:
        return jsonify({"message": "Dispositivo no autorizado."}), 401

    # 2. Procesar y guardar los datos de la planta (Contexto Plant)
    db_session = next(get_db_session())
    plant_repository = SQLAlchemyPlantRepository(db_session=db_session)
    plant_service = PlantService()
    plant_application_service = PlantApplicationService(
        plant_service=plant_service, plant_repository=plant_repository
    )

    data = request.get_json()
    if not data:
        return jsonify({"message": "JSON inválido."}), 400
        
    saved_plant_data = plant_application_service.add_plant_data(data)

    # 3. Reenviar los datos al backend de Spring Boot (SECCIÓN COMENTADA)
    # forwarding_service = ForwardingService()
    # success, response_data = forwarding_service.forward_data(saved_plant_data, device_info)
    #
    # if not success:
    #     return jsonify({
    #         "message": "Datos guardados localmente, pero falló el reenvío al backend central.",
    #         "local_data": saved_plant_data,
    #         "forwarding_error": response_data
    #     }), 502

    # Se devuelve una respuesta de éxito simple.
    return jsonify({
        "message": "Datos guardados localmente exitosamente.",
        "device_info": device_info,
        "saved_data": saved_plant_data
    }), 200
