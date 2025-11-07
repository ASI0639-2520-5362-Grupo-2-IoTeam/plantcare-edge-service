from flask import Flask
from flasgger import Swagger
from plant.interfaces.services import plant_blueprint
from shared.database import engine
from plant.infrastructure.models import Base

# Crear tablas de la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar e inicializar Swagger
swagger = Swagger(app)

# Registrar el Blueprint de las plantas
app.register_blueprint(plant_blueprint)

@app.route("/")
def read_root():
    """
    Endpoint principal de la aplicación.
    Este endpoint es para verificar que el servicio está funcionando.
    ---
    responses:
      200:
        description: Un mensaje de bienvenida.
        examples:
          text/plain: "Welcome to the Plant Care Edge Service"
    """
    return "Welcome to the Plant Care Edge Service"

if __name__ == '__main__':
    app.run(debug=True)
