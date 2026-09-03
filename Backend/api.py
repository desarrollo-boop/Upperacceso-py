import os
import requests
from dotenv import load_dotenv

load_dotenv()
URL_API = "http://localhost/Upper-acceso/api/enviar_datos.php"
API_KEY = os.getenv("OCR_API_KEY")

def enviar_datos(datos):
    try:
        if not API_KEY:
            print("Error: no se encontró OCR_API_KEY en el archivo .env")
            return

        headers = {
            "X-API-KEY": API_KEY
        }

        respuesta = requests.post(
            URL_API,
            json=datos,
            headers=headers,
            timeout=5
        )
        if respuesta.status_code == 200:
            print ("Datos enviados de manera correcta")
        elif respuesta.status_code == 401:
            print("Error: API Key incorrecta o no autorizada.")
        else:
            print("Error:", respuesta.status_code)
            print(respuesta.text)
    except Exception as e:
        print("No fue posible la conexion con PHP.")
        print(e)