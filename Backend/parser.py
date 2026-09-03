#solo comentaré los cambios, que para esta lectura de ocr no es necesario
from Backend.regiones import (
    obtener_nombre,
    #obtener_domicilio,
    obtener_curp,
    #obtener_clave,
    #obtener_fecha,
    obtener_vigencia
)

def extraer(datos):
    # Ordenar por posición (de arriba hacia abajo y de izquierda a derecha)
    datos = sorted(datos, key=lambda d: (d["y"], d["x"]))
    nombre = obtener_nombre(datos)
    # Extraer información
    resultado = {
        "tipo_documento": "INE",
        "numero_documento": "",
        "ruta_imagen": "",
        "nombre": obtener_nombre(datos),
        #"domicilio": obtener_domicilio(datos),
        "curp": obtener_curp(datos),
        #"clave_elector": obtener_clave(datos),
        #"fecha_nacimiento": obtener_fecha(datos),
        "vigencia": obtener_vigencia(datos)
    }
    #Es un ejemplo de la lectura que hace, no se hace de su uso pero es una explicativa
    """dom = resultado["domicilio"]
    reemplazos = {
        "C-": "C. - ",
        "C-": "C. - ",
        "S/N": " S/N ",
        "SE-": "S- ",
        "SE-": "S-",
        "SE-": "SEC- ",
        "SAN-": "SAN- ",
        "J-": "J- ",
        "DI-": "DI-",
        ".O-": ", O-"
    } """

    """ for viejo, nuevo in reemplazos.items():
        dom = dom.replace(viejo, nuevo)
    # Eliminar espacios repetidos
    dom = " ".join(dom.split())
    resultado["domicilio"] = dom"""
    partes = nombre.split()
    resultado["apellido_paterno"] = ""
    resultado["apellido_materno"] = ""
    resultado["nombres"] = ""
    if len(partes) >= 3:
        resultado["apellido_paterno"] = partes[0]
        resultado["apellido_materno"] = partes[1]
        resultado["nombres"] = " ".join(partes[2:])
    elif len(partes) == 2:
        resultado["apellido_paterno"] = partes[0]
        resultado["nombres"] = partes[1]
    elif len(partes) == 1:
        resultado["nombres"] = partes[0]
    return resultado