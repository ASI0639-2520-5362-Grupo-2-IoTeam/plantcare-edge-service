from flask import Flask
from plant.interfaces.services import plant_blueprint
from shared.database import engine
from plant.infrastructure.models import Base

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.register_blueprint(plant_blueprint)


@app.route("/")
def read_root():
    return "Welcome to the Plant Care Edge Service"
