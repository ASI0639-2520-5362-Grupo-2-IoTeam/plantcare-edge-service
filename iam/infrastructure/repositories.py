from typing import Optional

import peewee

from iam.domain.entities import Device
from iam.infrastructure.models import Device as DeviceModel

class DeviceRepository:
    @staticmethod
    def find_by_id_and_api_key(device_id: str, api_key: str) -> Optional[Device]:
        """
        Finds a device by its ID and API key.
        :param device_id: The ID of the device.
        :param api_key: The API key of the device.
        :return: The device if found, None otherwise.
        """
        try:
            device = DeviceModel.get((DeviceModel.device_id == device_id) & (DeviceModel.api_key == api_key))
            return Device(device_id=device.device_id, api_key=device.api_key, created_at=device.created_at)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def get_or_create_test_device()->Device:
        device, _ = DeviceModel.get_or_create(
            device_id="smart-band-001",
            defaults={ "api_key": "test-api-key-123", "created-at": "2025-10-02-07T10:00:00Z"}
        )
        return Device(device_id=device.device_id, api_key=device.api_key, created_at=device.created_at)