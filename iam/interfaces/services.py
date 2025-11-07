from flask import Blueprint, request, jsonify
from functools import wraps

from iam.application.services import AuthApplicationService

iam_api = Blueprint('iam_api', __name__)

# Initialize the AuthApplicationService
auth_service = AuthApplicationService()

def auth_required(f):
    """
    Decorator to protect endpoints with authentication.
    It checks for 'device_id' in the JSON body and 'X-API-Key' in the headers.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        device_id = request.json.get('device_id') if request.json else None
        api_key = request.headers.get('X-API-Key')
        if not device_id or not api_key:
            return jsonify({'error': 'Missing device_id or API key'}), 401
        if not auth_service.authenticate(device_id, api_key):
            return jsonify({'error': 'Invalid device_id or API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@iam_api.route('/register', methods=['POST'])
def register_device():
    """
    Register a new device.
    This endpoint allows for the registration of a new device in the system.
    ---
    tags:
      - IAM
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: DeviceRegistration
          required:
            - device_id
          properties:
            device_id:
              type: string
              description: The unique identifier for the device.
              example: "smart-plant-002"
    responses:
      201:
        description: Device registered successfully.
      400:
        description: Invalid input.
    """
    # Aquí iría tu lógica para registrar un nuevo dispositivo.
    # Por ahora, solo devolvemos un ejemplo de éxito.
    device_id = request.json.get('device_id')
    if not device_id:
        return jsonify({"error": "Missing device_id"}), 400

    # Lógica para crear el dispositivo...
    return jsonify({"message": f"Device {device_id} registered successfully"}), 201