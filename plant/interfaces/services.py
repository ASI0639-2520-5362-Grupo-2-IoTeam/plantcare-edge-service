from flask import Blueprint, request, jsonify
from flasgger import swag_from
from plant.application.services import PlantApplicationService
from plant.application.forwarding_service import ForwardingService
from plant.domain.services import PlantService
from plant.infrastructure.repositories import SQLAlchemyPlantRepository
from shared.database import get_db_session

# --- Simulación del contexto IAM ---
# En un sistema real, harías una llamada a tu servicio IAM.
# Por ahora, simularemos que obtenemos los datos del dispositivo.
def get_device_info(device_id: str) -> dict:
    """
    Simula la obtención de información de un dispositivo desde el contexto IAM.
    """
    if device_id == "wokwi-esp32-1":
        return {"id": device_id, "name": "Wokwi Lab Station 1", "location": "Development Lab"}
    return None
# ------------------------------------


plant_blueprint = Blueprint("plant", __name__)

@plant_blueprint.route("/plants", methods=["POST"])
def add_plant_data():
    """
    Endpoint para añadir nuevos datos de una planta y reenviarlos al backend central.
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
        description: Datos guardados localmente y reenviados exitosamente.
      400:
        description: Error en la petición (JSON inválido o falta de cabecera).
      401:
        description: Dispositivo no autorizado.
      502:
        description: Datos guardados localmente, pero falló el reenvío al backend central.
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

    # 3. Reenviar los datos al backend de Spring Boot
    forwarding_service = ForwardingService()
    success, response_data = forwarding_service.forward_data(saved_plant_data, device_info)

    if not success:
        # Si falla el reenvío, se devuelve un error 502 (Bad Gateway).
        # Los datos ya están guardados localmente, lo cual es bueno.
        return jsonify({
            "message": "Datos guardados localmente, pero falló el reenvío al backend central.",
            "local_data": saved_plant_data,
            "forwarding_error": response_data
        }), 502

    return jsonify({
        "message": "Datos guardados y reenviados exitosamente.",
        "local_data": saved_plant_data,
        "backend_response": response_data
    }), 200
