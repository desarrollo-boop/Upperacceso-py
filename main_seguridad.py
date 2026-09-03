import cv2
import time
import requests
import sys
import threading
from paddleocr import PaddleOCR
from Backend.parser import extraer as extraer_ine
from Backend.parsert import extraer as extraer_trabajo
from Backend.detector_documento import detectar
from flask import Flask, Response, jsonify, request

URL_API_SEGURIDAD = "http://localhost/Upper-acceso/api/evaluar_acceso.php"
INTERVALO_OCR = 2.0
print("Inicializando OCR...")
app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang="es")
print("OCR listo.")

cam = None
camara_activa = False
frame_actual = None
ultimo_ocr = 0
tipo_documento = "DESCONOCIDO"
ultimo_resultado = {}
id_usuario = None
lock = threading.Lock()

def abrir_camara():
    global cam
    global camara_activa

    if cam is not None and cam.isOpened():
        return True
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cam.isOpened():
        cam = None
        return False
    camara_activa = True
    return True

def generar_frames():
    global cam
    global camara_activa
    global frame_actual
    while camara_activa:
        if cam is None:
            break
        ret, frame = cam.read()
        if not ret or frame is None:
            continue
        frame_actual = frame.copy()
        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            continue
        frame_bytes = buffer.tobytes()
        yield(
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )
    cerrar_camara() 

@app.route("/iniciar", methods=["POST"])
def iniciar():
    global camara_activa
    global id_usuario
    global ultimo_ocr
    global tipo_documento
    global ultimo_resultado
    global frame_actual
    datos = request.get_json(silent=True) or {}
    id_recibido = datos.get("id_usuario")
    if not id_recibido:
        return jsonify({
            "ok": False,
            "mensaje": "No se recibió id_usuario."
        }), 400
    try:
        id_usuario = int(id_recibido)
    except (ValueError, TypeError):
        return jsonify({
            "ok": False,
            "mensaje": "El id_usuario recibido no es válido."
        }), 400
    ultimo_ocr = 0
    tipo_documento = "DESCONOCIDO"
    ultimo_resultado = {}
    frame_actual = None
    if not abrir_camara():
        return jsonify({
            "ok": False,
            "mensaje": "No fue posible abrir la cámara."
        }), 500
    hilo_ocr = threading.Thread(
        target=ejecutar_ocr,
        daemon=True
    )
    hilo_ocr.start()
    print(f"Usuario de Seguridad: {id_usuario}")
    return jsonify({
        "ok": True,
        "mensaje": "Cámara y OCR inciados."
    })

@app.route("/video")
def video():
    if not abrir_camara():
        return ("No fue posible abrir la cámara.", 500)
    return Response(generar_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
 
def datos_validados(datos, tipo):
    if not datos:
        return False
    if tipo == "INE":
        curp = str(datos.get("curp", "")).strip()
        nombres = str(datos.get("nombres", "")).strip()
        apellido_paterno = str(datos.get("apellido_paterno", "")).strip()
        apellido_materno = str(datos.get("apellido_materno", "")).strip()
        if curp:
            return True
        if (nombres and apellido_paterno and apellido_materno):
            return True
        return False
    if tipo == "TRABAJO":
        nombres = str(datos.get("nombres", "")).strip()
        apellido_paterno = str(datos.get("apellido_paterno", "")).strip()
        apellido_materno = str(datos.get("apellido_materno", "")).strip()
        empresa = str(datos.get("empresa", "")).strip()
        if (nombres and apellido_paterno and apellido_materno and empresa):
            return True
        return False
    return False

def evaluar_acceso(datos):
    try:
        respuesta = requests.post(
            URL_API_SEGURIDAD,
            json=datos,
            timeout=5
        )

        if respuesta.status_code != 200:
            print(f"ERROR PHP: código HTTP {respuesta.status_code}")
            print(respuesta.text)
            return None
        try: 
            return respuesta.json()
        except ValueError:
            print("ERROR: PHP no devolvió JSON válido.")
            print(respuesta.text)
            return None

    except requests.exceptions.RequestException as e:
        print("ERROR: No fue posible conectar con PHP.")
        print(e)
        return None
def ejecutar_ocr():
    global ultimo_ocr
    global tipo_documento
    global ultimo_resultado
    global frame_actual
    global camara_activa

    while camara_activa:
        if frame_actual is None:
            time.sleep(0.1)
            continue
        frame = frame_actual.copy()
        ahora = time.time()
        if ahora - ultimo_ocr >= INTERVALO_OCR:
            ultimo_ocr = ahora
            print("Ejecutando OCR...")
            resultado = ocr.ocr(frame, cls=True)
            datos=[]
            if resultado and resultado[0]:
                for linea in resultado[0]:
                    caja = linea [0]
                    texto = linea[1][0]
                    confianza = linea[1][1]
                    x = sum(
                        punto[0]
                        for punto in caja
                    ) / 4
                    y = sum (
                        punto[1]
                        for punto in caja
                    ) / 4
                    datos.append({
                        "texto": texto,
                        "x": x,
                        "y": y,
                        "confianza": confianza
                    })
                if datos:
                    tipo_documento = detectar(datos)
                    print(f"Documento detectado: {tipo_documento}")
                    if tipo_documento == "INE":
                        ultimo_resultado = extraer_ine(datos)
                    elif tipo_documento == "TRABAJO":
                        ultimo_resultado = extraer_trabajo(datos)
                    else:
                        ultimo_resultado = {}
                    if datos_validados(ultimo_resultado, tipo_documento):
                        print("Datos obtenidos correctamente:")
                        print(ultimo_resultado)
                        ultimo_resultado["tipo_documento"] = tipo_documento
                        ultimo_resultado["id_usuario"] = id_usuario
                        print("Consultando acceso...")
                        respuesta = evaluar_acceso(ultimo_resultado)
                        if respuesta is None:
                            print("No se pudo consultar el resultado de acceso")
                            print("El escaneo continuará...")
                            continue
                        print("Respuesta del sitema:")
                        print(respuesta)
                        if respuesta.get("acceso") is True:
                            print("ACCESO PERMITIDO")
                        else:
                            print("ACCESO DENEGADO")
                        camara_activa = False
                        break
                    else:
                        print("Documento detectado, pero no se obtivieron datos suficientas.")

        y = 30

        cv2.putText(frame, f"Documento: {tipo_documento}",
                    (20,y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 255), 2)
        y += 40
        if tipo_documento == "INE":
            campos = [("Nombre(s)", ultimo_resultado.get("nombres", "")),
                      ("Apellido P.", ultimo_resultado.get("apellido_paterno", "")),
                      ("Apellido M.", ultimo_resultado.get("apellido_materno", "")),
                      ("CURP", ultimo_resultado.get("curp", ""))]
            for titulo, valor in campos:
                cv2.putText(frame, f"{titulo}: {valor}",
                            (20, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.60, (0, 255, 0), 2)
                y += 30
        elif tipo_documento == "TRABAJO":
            campos = [("Empresa", ultimo_resultado.get("empresa", "")),
                      ("Nombre(s)", ultimo_resultado.get("nombres", "")),
                      ("Apellido P.", ultimo_resultado.get("apellido_paterno", "")),
                      ("Apellido M.", ultimo_resultado.get("apellido_materno", "")),
                      ("Departamento", ultimo_resultado.get("departamento", ""))]
            for titulo, valor in campos:
                cv2.putText(frame, f"{titulo}: {valor}",
                            (20, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.60, (255, 255, 0), 2)
                y += 30

        else:
            cv2.putText(frame, "Documento no reconocido",
                        (20, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 0, 255), 2)
def cerrar_camara():
    global cam
    global camara_activa
    global frame_actual
    camara_activa = False
    frame_actual = None
    if cam is not None:
        cam.release()
        cam = None
    print("Cámara cerrada.")

print(app.url_map)

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False,
        threaded=True
    )