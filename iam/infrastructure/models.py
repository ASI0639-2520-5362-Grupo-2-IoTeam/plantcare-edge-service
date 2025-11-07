from peewee import Model, CharField, DateTimeField
from shared.infrastructure.database import db

class Device(Model):
    """
    Represents a device model for the 'devices' table in the IAM context.

    Attributes:
        device_id (str): Unique identifier for the device.
        api_key (str): API key for the device.
        created_at (datetime): Timestamp when the device was created.
    """
    device_id = CharField(primary_key=True)
    api_key = CharField()
    created_at = DateTimeField()

    class Meta:
        """Metadata for the Device model."""
        database = db
        table_name = 'devices'