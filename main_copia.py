import cv2
import time
#extra para el guardado de fotos
import os
import uuid
from datetime import datetime
from paddleocr import PaddleOCR
from Backend.parser import extraer as extraer_ine
from Backend.parsert import extraer as extraer_trabajo
from Backend.detector_documento import detectar
from Backend.api import enviar_datos

CARPETA_DOCUMENTOS = r"C:\xampp\htdocs\Upper-Acceso\frontend\documentos"
def guardar_imagen(frame):
    carpeta = os.path.join(CARPETA_DOCUMENTOS, "temp")
    os.makedirs(carpeta, exist_ok=True)
    nombre = f"{uuid.uuid4()}.jpg"
    #uuid es para guardarlo con nombres como en código
    ruta_absoluta = os.path.join(carpeta, nombre)
    cv2.imwrite(ruta_absoluta, frame)
    ruta_relativa = os.path.join( "frontend","documentos", "temp", nombre)
    return ruta_relativa
#IMPORTANTE: pip install requests esto es para la conexion del API y que funciones llamando el http://
#Iniciando OCR
ocr = PaddleOCR(
    use_angle_cls=True,
    lang="es"
)
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cam.isOpened():
    print("No se pudo abrir la cámara.")
    exit()
ultimo_resultado = {}
ultimo_enviado = {}
tipo_documento = "DESCONOCIDO"
ultimo_ocr = 0
intervalo = 2.0
print("Presiona Q para salir.")
while True:
    ret, frame = cam.read()
    if not ret:
        break
    ahora = time.time()
    if ahora - ultimo_ocr >= intervalo:
        ultimo_ocr = ahora
        resultado = ocr.ocr(frame, cls=True)
        datos = []
        if resultado and resultado[0]:
            for linea in resultado[0]:
                caja = linea[0]
                texto = linea[1][0]
                confianza = linea[1][1]
                x = sum(p[0] for p in caja) / 4
                y = sum(p[1] for p in caja) / 4
                datos.append({
                    "texto": texto,
                    "x": x,
                    "y": y,
                    "confianza": confianza
                })
            tipo_documento = detectar(datos)
            if tipo_documento == "INE":
                ultimo_resultado = extraer_ine(datos)
            elif tipo_documento == "TRABAJO":
                ultimo_resultado = extraer_trabajo(datos)
            else:
                ultimo_resultado = {}
                #Parte importante para cambiar.
                # el guardado de imagenes y capturas de los documentos
            if ultimo_resultado:
                #es para la comparació de los datos que va obteniendo el OCR
                datos_comparacion = ultimo_resultado.copy()
                if datos_comparacion != ultimo_enviado:
                    ruta = guardar_imagen(frame)
                    #aqui se agrega la ruta del resultado
                    ultimo_resultado["ruta_imagen"] = ruta
                    enviar_datos(ultimo_resultado)
                    #aqui solo se fuarda los datos del ocr para las comparaciones
                    ultimo_enviado = datos_comparacion
    y = 30
                    
    cv2.putText(
        frame,
        f"Documento: {tipo_documento}",
        (20, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 255),
        2
    )
    y += 40
    # INE
    if tipo_documento == "INE":
        campos = [
            ("Nombre(s)", ultimo_resultado.get("nombres", "")),
            ("Apellido P.", ultimo_resultado.get("apellido_paterno", "")),
            ("Apellido M.", ultimo_resultado.get("apellido_materno", "")),
            ("CURP", ultimo_resultado.get("curp", "")),
            #("Clave", ultimo_resultado.get("clave_elector", "")),
            #("Nacimiento", ultimo_resultado.get("fecha_nacimiento", "")),
            ("Vigencia", ultimo_resultado.get("vigencia", "")),
            #("Domicilio", ultimo_resultado.get("domicilio", ""))
        ]
        for titulo, valor in campos:
            cv2.putText(
                frame,
                f"{titulo}: {valor}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.60,
                (0, 255, 0),
                2
            )
            y += 30
    # CREDENCIAL DE TRABAJO
    elif tipo_documento == "TRABAJO":
        campos = [
            ("Empresa", ultimo_resultado.get("empresa", "")),
            ("Nombre(s)", ultimo_resultado.get("nombres", "")),
            ("Apellido P.", ultimo_resultado.get("apellido_paterno", "")),
            ("Apellido M.", ultimo_resultado.get("apellido_materno", "")),
            ("Departamento", ultimo_resultado.get("departamento", "")),
        ]
        for titulo, valor in campos:
            cv2.putText(
                frame,
                f"{titulo}: {valor}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.60,
                (255, 255, 0),
                2
            )
            y += 30
    # DOCUMENTO DESCONOCIDO
    else:
        cv2.putText(
            frame,
            "Documento no reconocido",
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 0, 255),
            2
        )
    # MOSTRAR VIDEO
    cv2.imshow("Sistema OCR", frame)
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()