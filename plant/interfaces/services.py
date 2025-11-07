from flask import Blueprint, request, jsonify
from plant.application.services import PlantApplicationService
from plant.domain.services import PlantService
from plant.infrastructure.repositories import SQLAlchemyPlantRepository
from shared.database import get_db_session

plant_blueprint = Blueprint("plant", __name__)


@plant_blueprint.route("/plants", methods=["POST"])
def add_plant_data():
    """
    Endpoint for adding new plant data.
    """
    db_session = next(get_db_session())
    plant_repository = SQLAlchemyPlantRepository(db_session=db_session)
    plant_service = PlantService()
    plant_application_service = PlantApplicationService(
        plant_service=plant_service, plant_repository=plant_repository
    )

    data = request.get_json()
    result = plant_application_service.add_plant_data(data)
    return jsonify(result)
