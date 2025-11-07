from typing import Optional

from iam.domain.services import AuthService
from iam.infrastructure.models import Device
from iam.infrastructure.repositories import DeviceRepository

class AuthApplicationService:
    """
    Application service for handling authentication and device management.
    This service interacts with the domain services and repositories to perform its operations.
    """
    def __init__(self):
        """
        Initialize the AuthApplicationService with necessary repositories and services.
        """
        self.device_repository = DeviceRepository()
        self.auth_service = AuthService()

    def authenticate(self, device_id: str, api_key: str)->bool:
        """
        Authenticate a device using its ID and API key.
        :param device_id: The ID of the device.
        :param api_key: The API key of the device.
        :return: True if authentication is successful, False otherwise.
        """
        device: Optional[Device] = self.device_repository.find_by_id_and_api_key(device_id, api_key)
        return self.auth_service.authenticate(device)

    def get_or_create_test_device(self)->Device:
        """
        Retrieve or create a test device for development purposes.
        :return: A Device instance representing the test device.
        """
        return self.device_repository.get_or_create_test_device()

    def get_device_by_id_and_api_key(self, device_id: str, api_key: str)-> Optional[Device]:
        """
        Retrieve a device by its ID and API key.
        :param device_id: The ID of the device.
        :param api_key: The API key of the device.
        :return: A Device instance if found, None otherwise.
        """
        return self.device_repository.find_by_id_and_api_key(device_id, api_key)