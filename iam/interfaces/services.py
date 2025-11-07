from flask import Blueprint, request, jsonify

from iam.application.services import AuthApplicationService

iam_api = Blueprint('iam_api', __name__)

# Initialize the AuthApplicationService
auth_service = AuthApplicationService()

def authenticate_request():
    """
    Authenticate a request using the device_id and API key.

    Checks for the presence of the device_id in the body, and API key in the request headers.
    :return: None if authentication is successful, else a JSON response with an error message.
    """
    device_id = request.json.get('device_id') if request.json else None
    api_key = request.headers.get('X-API-Key')
    if not device_id or not api_key:
        return jsonify({'error': 'Missing device_id or API key'}), 401
    if not auth_service.authenticate(device_id, api_key):
        return jsonify({'error': 'Invalid device_id or API key'}), 401
    return None