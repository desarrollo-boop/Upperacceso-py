import re
import unicodedata
from Backend.regiones_trabajo import(
    obtener_empresa,
    obtener_nombre,
    obtener_departamento,
)

def limpiar_texto(texto):
    if not texto:
        return ""
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

def normalizar(texto):
    if not texto:
        return ""
    texto = limpiar_texto(texto)
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto
                    if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^A-Za-z0-9Ññ\s]", " ", texto)
    return texto.upper().strip()
def separar_nombre(nombre):
    resultado ={
        "nombres": "",
        "apellido_paterno": "",
        "apellido_materno": ""
    }
    if not nombre:
        return resultado
    nombre = limpiar_texto(nombre)
    partes = nombre.split()
    print ("NOMBRE OCR:",
           repr(nombre))
    print ("PARTES:", partes)

    if len(partes) >= 4:
        resultado["nombres"] = " ".join(
            partes[:-2]
        )
        resultado["apellido_paterno"] = (
            partes[-2]
        )
        resultado["apellido_materno"] = [
            partes[-1]
        ]
    elif len(partes) == 3:
        resultado["nombres"] = (
            partes[0]
        )
        resultado["apellido_paterno"] = (
            partes[1]
        )
        resultado["apellido_materno"] = (
            partes[2]
        )
    elif len(partes) == 2:
        resultado["nombre"] = (
            partes[0]
        )
        resultado["apellido_paterno"] = (
            partes[1]
        )
        resultado["nombres"] = (
            partes[0]
        )
    elif len(partes) == 1:
        resultado["nombres"] = partes[0]
        resultado["apellido_paterno"] = ""
        resultado["apellido_materno"] = ""
    return resultado

def extraer(
        datos, frame=None, ocr=None
):
    resultado_vacio = {
        "tipo_documento":
            "TRABAJO",
        "numero_documento":
            "",
        "ruta_imagen":
            "",
        "empresa":
            "",
        "nombre_completo":
            "",
        "nombres":
            "", 
        "apellido_paterno":
            "",
        "apellido_materno":
            "",
        "curp":
            "",
        "departamento":
            "",
        "vigencia":
            ""
    }

    if not datos:
        return resultado_vacio

    datos = sorted(
        datos,
        key=lambda d: (
            d["y"],
            d["x"]
        )
    )
    empresa = (
        obtener_empresa(
            datos
        )
        or ""
    )
    empresa = limpiar_texto(
        empresa
    )
    nombre_completo = (
        obtener_nombre(datos) or ""
    )
    nombre_completo = limpiar_texto(nombre_completo)
    departamento = (
        obtener_departamento(datos) or ""
    )
    departamento = limpiar_texto(departamento)
    datos_nombre = separar_nombre(nombre_completo)

    resultado = {
        "tipo_documento":
            "TRABAJO",
        "numero_docuemento":
            "",
        "ruta_imagen":
            "",
        "empresa":
            empresa,
        "nombre_completo":
            nombre_completo,
        "nombres":
            datos_nombre["nombres"],
        "apellido_paterno":
            datos_nombre["apellido_paterno"],
        "apellido_materno":
            datos_nombre["apellido_materno"],
        "curp":
            "",
        "departamento":
            departamento,
        "vigencia":
            ""
    }

    print(
        "\n===RESULTADO==="
    )
    print("EMPRESA:", repr(empresa))
    print("NOMBRE COMPLETO:", repr(nombre_completo))
    print("NOMBRE NORMALIZADO", repr(normalizar(nombre_completo)))
    print("NOMBRES:", repr(resultado["nombres"]))
    print("PATERNO:", repr(resultado["apellido_paterno"]))
    print("MATERNO:", repr(resultado["apellido_materno"]))
    print("DEPARTAMENTO:", repr(departamento))
    print("DEPARTAMENTO NORMALIZADO", repr(normalizar(departamento)))
    print("==============\n")
    return resultado