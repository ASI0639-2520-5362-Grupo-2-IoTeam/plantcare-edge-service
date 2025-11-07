import requests
import os

# Lee la URL del backend de Spring Boot desde una variable de entorno.
# Es una buena práctica no tener URLs hardcodeadas en el código.
SPRING_BOOT_BACKEND_URL = os.getenv("SPRING_BOOT_URL", "http://localhost:8080/api/v1/plant-data")

class ForwardingService:
    """
    Este servicio se encarga de reenviar los datos procesados
    al backend central de Spring Boot.
    """

    def forward_data(self, plant_data: dict, device_info: dict):
        """
        Combina los datos de la planta y del dispositivo y los envía
        al backend de Spring Boot.

        Args:
            plant_data (dict): El diccionario con los datos de la planta ya guardados.
            device_info (dict): El diccionario con la información del dispositivo.
        """
        
        # Construye el payload combinado
        combined_payload = {
            "device": device_info,
            "sensorReadings": {
                "temperature": plant_data.get("temperature"),
                "humidity": plant_data.get("humidity"),
                "light": plant_data.get("light"),
                "soilHumidity": plant_data.get("soil_humidity")
            },
            "timestamp": plant_data.get("created_at").isoformat() if plant_data.get("created_at") else None
        }

        try:
            # Realiza la petición POST al backend de Spring Boot
            response = requests.post(
                SPRING_BOOT_BACKEND_URL,
                json=combined_payload,
                headers={"Content-Type": "application/json"},
                timeout=5  # Es bueno tener un timeout
            )

            # Verifica si la petición fue exitosa (códigos 2xx)
            response.raise_for_status() 

            print(f"Datos reenviados exitosamente a Spring Boot. Status: {response.status_code}")
            return True, response.json()

        except requests.exceptions.RequestException as e:
            # Maneja errores de conexión, timeouts, etc.
            print(f"Error al reenviar datos a Spring Boot: {e}")
            return False, str(e)
