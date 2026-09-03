import cv2
import time
import os
import uuid
from paddleocr import PaddleOCR
from Backend.parser import extraer as extraer_ine
from Backend.parsert import extraer as extraer_trabajo
from Backend.detector_documento import detectar
from Backend.api import enviar_datos

CARPETA_DOCUMENTOS = r"C:\xampp\htdocs\Upper-Acceso\frontend\documentos"
INTERVALO_OCR = 2.0
def guardar_imagen(frame):
    carpeta = os.path.join(CARPETA_DOCUMENTOS,"temp")
    os.makedirs(carpeta,exist_ok=True)
    nombre = f"{uuid.uuid4()}.jpg"
    ruta_absoluta = os.path.join(carpeta,nombre)
    cv2.imwrite(ruta_absoluta,frame)
    ruta_relativa = os.path.join("frontend","documentos","temp",nombre)
    return ruta_relativa

print("Inicializando OCR...")
ocr = PaddleOCR(use_angle_cls=True, lang="es")
print("OCR listo.")

print("Iniciando cámara...")
cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
if not cam.isOpened():
    print("ERROR: No se pudo abrir la cámara.")
    raise SystemExit(1)
print("Cámara iniciada correctamente.")
print("Esperando documento...")

ultimo_ocr = 0
tipo_documento = "DESCONOCIDO"
ultimo_resultado = {}

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            print("ERROR: No se pudo leer la cámara.")
            break

        ahora = time.time()
        if ahora - ultimo_ocr >= INTERVALO_OCR:
            ultimo_ocr = ahora
            print("Ejecutando OCR...")
            resultado = ocr.ocr(frame, cls=True)
            datos = []
            if resultado and resultado[0]:
                for linea in resultado[0]:
                    caja = linea[0]
                    texto = linea[1][0]
                    confianza = linea[1][1]
                    x = sum(punto[0]
                        for punto in caja
                    ) / 4
                    y = sum(punto[1]
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
                print(
                    f"Documento detectado: {tipo_documento}"
                )
                if tipo_documento == "INE":
                    ultimo_resultado = extraer_ine(datos)
                elif tipo_documento == "TRABAJO":
                    ultimo_resultado = extraer_trabajo(datos)
                else:
                    ultimo_resultado = {}
                if ultimo_resultado:
                    print("Datos obtenidos:")
                    print(
                        ultimo_resultado
                    )
                    ruta = guardar_imagen(frame)
                    ultimo_resultado["ruta_imagen"] = ruta
                    print(
                        f"Imagen guardada: {ruta}"
                    )
                    try:
                        enviar_datos(
                            ultimo_resultado
                        )
                        print(
                            "Datos enviados correctamente."
                        )
                    except Exception as e:
                        print(
                            f"ERROR al enviar datos: {e}"
                        )
                        break
                    print(
                        "ESCANEO_COMPLETADO"
                    )
                    print(
                        ultimo_resultado
                    )
                    break
        y = 30
        cv2.putText(frame, f"Documento: {tipo_documento}",
            (20, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 255), 2)
        y += 40
        if tipo_documento == "INE":
            campos = [("Nombre(s)", ultimo_resultado.get("nombres", "")),
                ("Apellido P.", ultimo_resultado.get("apellido_paterno", "")),
                ("Apellido M.", ultimo_resultado.get("apellido_materno", "")),
                ("CURP", ultimo_resultado.get("curp", "")),
                ("Vigencia", ultimo_resultado.get("vigencia", ""))]
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
        cv2.imshow("Sistema OCR", frame)
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord("q"):
            print("Escaneo cancelado por el usuario.")
            break
finally:
    print("Cerrando cámara...")
    if cam is not None:
        cam.release()
    cv2.destroyAllWindows()
    print("Cámara cerrada.")