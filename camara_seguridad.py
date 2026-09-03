from flask import Flask, Response, jsonify
import cv2
import threading


app = Flask(__name__)
@app.after_request
def agregar_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

camara = None
camara_activa = False
lock = threading.Lock()

def abrir_camara():
    global camara, camara_activa
    with lock:
        if camara is not None and camara.isOpened():
            return True
        camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not camara.isOpened():
            camara = None
            return False
        camara_activa = True
        return True

def generar_frames():
    global camara, camara_activa
    while camara_activa:
        if camara is None:
            break
        ret, frame = camara.read()
        if not ret or frame is None:
            print("No se pudo obetener frame de la cámara.")
            continue
        if frame.size == 0:
            print ("Frame vacío.")
            continue
        try:
            ok, buffer = cv2.imencode(".jpg", frame)
            if not ok:
                print("No se pudo codificar frame.")
                continue
        except cv2.error as error:
            print("Error al codificar frame:")
            print(error)
            continue

        frame_bytes = buffer.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame_bytes +
            b"\r\n"
        )
@app.route("/iniciar", methods=["POST"])
def inciar():
    if abrir_camara():
        return jsonify({
            "ok": True,
            "mensaje": "Cámara inciada."
        })
    return jsonify({
        "ok": False,
        "mensaje": "No fue posible abrir la cámara."
    }), 500

@app.route("/video")
def video():
    if not abrir_camara():
        return "No fue posible abrir cámara.", 500
    return Response(
        generar_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/detener", methods=["POST"])
def detener():
    global camara, camara_activa
    with lock:
        camara_activa = False
        if camara is not None:
            camara.release()
            camara = None
        return jsonify({
            "ok": True,
            "mensaje": "Cámara detenida."
        })
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False,
        threaded=True
    )
