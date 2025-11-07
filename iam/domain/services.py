from iam.domain.entities import Device
from typing import Optional

class AuthService:
    """
    Constructor for AuthService
    """
    def __init__(self):
        pass

    @staticmethod
    def authenticate(device: Optional[Device])->bool:
        """
        Authenticate a device based on its presence.
        :param device: Device object or None
        :return: True if the device is valid, False otherwise
        """
        return device is not None