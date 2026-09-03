from Backend.regiones_trabajo import (
    obtener_empresa,
    obtener_nombre,
    obtener_departamento,
)
def extraer(datos):
    datos = sorted(datos, key=lambda d: (d["y"], d["x"]))
    empresa = obtener_empresa(datos)
    nombre = obtener_nombre(datos)
    departamento = obtener_departamento(datos)
    resultado = {
        "tipo_documento": "TRABAJO",
        "numero_documento": "",
        "ruta_imagen": "",
        "empresa": empresa,
        "nombres": "",
        "apellido_paterno": "",
        "apellido_materno": "",
        "curp": "",
        "departamento": departamento,
        "vigencia": ""
    }
    partes = nombre.split()
    if len(partes) >= 4:
        resultado["nombres"] = " ".join(partes[:-2])
        resultado["apellido_paterno"] = partes[-2]
        resultado["apellido_materno"] = partes[-1]
    elif len(partes) == 3:
        resultado["nombres"] = partes[0]
        resultado["apellido_paterno"] = partes[1]
        resultado["apellido_materno"] = partes[2]
    elif len(partes) == 2:
        resultado["nombres"] = partes[0]
        resultado["apellido_paterno"] = partes[1]
    elif len(partes) == 1:
        resultado["nombres"] = partes[0]
    return resultado