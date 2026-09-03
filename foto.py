from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import os
import uuid

app = Flask(__name__)
CORS(app)

FOTOS = r"C:\xampp\htdocs\Upper-acceso\frontend\documentos\fotografias"
os.makedirs(FOTOS, exist_ok=True)

cam = None

def generar_video():
    global cam

    while True:

        if cam is None or not cam.isOpened():
            break

        ret, frame = cam.read()

        if not ret:
            print("ERROR_LECTURA")
            break

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


@app.route("/video")
def video():
    global cam

    if cam is None or not cam.isOpened():
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cam.isOpened():
            return "No se pudo abrir la cámara", 500

        print("CAMARA_INICIADA")

    return Response(
        generar_video(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/tomar_foto", methods=["POST"])
def tomar_foto():
    global cam
    ret, frame = cam.read()
    if not ret:
        return jsonify({
            "ok": False,
            "mensaje": "No se pudo tomar la fotografia."
        }), 500

    nombre = f"{uuid.uuid4()}.jpg"
    ruta_absoluta = os.path.join(FOTOS, nombre)

    guardada = cv2.imwrite(ruta_absoluta, frame)

    if not guardada:
        return jsonify({
            "ok": False,
            "mensaje": "No se pudo guardar la fotografia"
        }), 500
    ruta_relativa = os.path.join(
    "frontend",
    "documentos",
    "fotografias",
    nombre
    ).replace("\\", "/")
    
    print("FOTO_GUARDADA:", ruta_relativa)
    cam.release()
    cam = None
    print("CAMARA_LIBERADA")
    return jsonify({
        "ok": True,
        "mensaje": "Fotografía guardada correctamente.",
        "ruta": ruta_relativa,
        "nombre": nombre
        })

@app.route("/")
def inicio():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Prueba cámara</title>    
        </head>
        <body>
            <h1>Cámara funcionando</h1>
            <img
                src="/video"
                width="640"
            >
            <br><br>
            <button
                onclick="tomarFoto()">
                Tomar fotografía
            </button>
            <script>
                async function tomarFoto() {
                    const respuesta = await fetch(
                        "/tomar_foto",
                        {
                            method: "POST"
                        }
                    );
                    const datos = await respuesta.json();
                    console.log(datos);
                    alert(datos.mensaje);
            </script>
        </body>
        </html>
        """
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )