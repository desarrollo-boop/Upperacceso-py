Iris Gate — Módulo Python OCR y Cámara
Módulo desarrollado en Python para complementar el sistema web Iris Gate, utilizado para el control y administración de accesos en UPPER LOGISTICS, PIA 41, Querétaro.
Este componente se encarga de capturar imágenes mediante webcam, aplicar reconocimiento óptico de caracteres, procesar la información detectada y comunicarse con el sistema web desarrollado en PHP.
Tecnologías utilizadas
numpy 1.26.4
opencv-python 4.6.0.66
paddlepaddle 2.6.2
paddleocr 2.7.3
flask
flask-cors
python-detenv
Entorno de desarrollo
Ruta utilizada durante el desarrollo:
C:\xampp\UpperAcceso
Entorno virtual:
C:\xampp\UpperAcceso\.venv
Ejecutable utilizado:
C:\xampp\UpperAcceso\.venv\Scripts\python.exe
Funcionalidades principales
- Captura mediante webcam.
- Lectura OCR de INE.
- Lectura OCR de credenciales de trabajo.
- Detección del tipo de documento.
- Extracción de nombres y apellidos.
- Extracción de CURP.
- Extracción de vigencia.
- Identificación de empresa.
- Identificación de departamento o cargo.
- Envío de datos hacia APIs PHP.
- Evaluación de accesos.
- Captura de fotografías mediante Flask.
- Comunicación con el dashboard de Seguridad.
Archivos principales
main.py
Contiene el flujo OCR utilizado durante el registro de colaboradores y visitantes.
Realiza:
1. Apertura de webcam.
2. Captura del documento.
3. Ejecución de PaddleOCR.
4. Detección del tipo de documento.
5. Procesamiento mediante el parser correspondiente.
6. Guardado temporal de imagen.
7. Envío de información al sistema PHP.
main_seguridad.py
Contiene el flujo OCR utilizado en el panel de Seguridad.
Permite:
1. Leer la credencial.
2. Detectar el documento.
3. Extraer la información.
4. Enviar los datos a evaluar_acceso.php.
5. Recibir el resultado de acceso.
6. Mostrar si el acceso fue permitido o denegado.
foto.py
Servicio Flask utilizado para capturar fotografías mediante webcam.
Durante desarrollo utiliza una dirección local similar a:
http://127.0.0.1:5000
Backend/parser.py
Procesa información obtenida de documentos INE, incluyendo nombres, apellidos, CURP y vigencia.
Backend/parsert.py
Procesa información obtenida de credenciales de trabajo, incluyendo nombre completo, empresa y departamento o cargo.
detector_documento.py
Permite determinar el tipo de documento leído por OCR.
Tipos manejados actualmente:
INE
TRABAJO
Credenciales de trabajo probadas
Durante el desarrollo se han realizado pruebas con credenciales de:
UPPER LOGISTICS
INNOVET
ABFORTI
La precisión puede variar según iluminación, enfoque, posición del documento y calidad de impresión.
Flujo OCR de registro
Webcam
   ↓
main.py
   ↓
PaddleOCR
   ↓
Detección de documento
   ↓
Parser
   ↓
Datos estructurados
   ↓
API PHP
   ↓
Formulario web
Flujo OCR de Seguridad
Webcam
   ↓
main_seguridad.py
   ↓
PaddleOCR
   ↓
Extracción de datos
   ↓
evaluar_acceso.php
   ↓
Base de datos
   ↓
Permitido / Denegado
   ↓
Dashboard de Seguridad
Webcam
Durante desarrollo se utiliza normalmente:
cv2.VideoCapture(0)
El índice 0 representa la cámara principal conectada al equipo.
Entorno virtual
Crear:
cd C:\xampp\UpperAcceso
python -m venv .venv
Activar:
.venv\Scripts\activate
Desactivar:
deactivate
Instalación de dependencias
Con el entorno virtual activo:
pip install -r requerimientos.txt

Variables de entorno
Ejemplo:
OCR_API_KEY=clave
Para producción también se recomienda manejar la URL del sistema web mediante una variable:
IRIS_GATE_URL=http://localhost/Upper-acceso
En producción:
IRIS_GATE_URL=https://dominio-del-sistema.com

Comunicación con PHP
URL:
http://localhost/Upper-acceso/api/

Archivos que no deben subirse al repositorio
.env
.env.*
.venv/
__pycache__/
*.pyc

Consideraciones sobre el OCR
La precisión puede verse afectada por:
- Mala iluminación.
- Reflejos.
- Movimiento.
- Desenfoque.
- Distancia del documento.
- Tamaño del texto.
- Diseño de la credencial.
- Posición del documento frente a la cámara.
El OCR se encuentra funcional, aunque todavía puede recibir mejoras de precisión.

Producción
El sistema PHP podrá ejecutarse en un servidor remoto.
Este módulo Python necesita acceso físico a la webcam, por lo que deberá ejecutarse en la computadora donde se encuentre conectada la cámara.

Arquitectura prevista:
PC de Seguridad
│
├── Webcam
├── Python
├── OpenCV
├── PaddleOCR
└── HTTPS
      ↓
Servidor Iris Gate
      ↓
PHP
      ↓
MariaDB

Mejoras pendientes
- Mejorar precisión OCR.
- Optimizar regiones de lectura.
- Mejorar reconocimiento de credenciales UPPER.
- Normalizar nombres.
- Validar confianza OCR.
- Configurar URLs mediante .env.
- Implementar comunicación segura mediante HTTPS.
- Preparar el módulo como agente local para producción.
- Mejorar manejo de errores de cámara y conexión.

Estado del proyecto
El módulo se encuentra en una versión funcional de desarrollo previa a la adaptación para producción.
Actualmente existe integración entre Python, PaddleOCR, OpenCV, Flask y el sistema web desarrollado en PHP.
Proyecto
Iris Gate
Sistema Inteligente de Control de Acceso
UPPER LOGISTICS — PIA 41
Querétaro, México