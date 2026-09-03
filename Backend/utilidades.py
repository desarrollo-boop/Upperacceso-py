import re
#aqui solo estan funciones que pueden ser llamadas por otros archivos, así que no hay necesidad de eliminar algo
def limpiar(texto):
    texto = texto.upper()
    texto = texto.replace("Á", "A")
    texto = texto.replace("É", "E")
    texto = texto.replace("Í", "I")
    texto = texto.replace("Ó", "O")
    texto = texto.replace("Ú", "U")

    texto = texto.replace("DOMCILIO", "DOMICILIO")
    texto = texto.replace("DOMICLIO", "DOMICILIO")
    texto = texto.replace("SEXOM", "SEXO M")
    texto = texto.replace("SEXOH", "SEXO H")

    texto = " ".join(texto.split())
    return texto

def distancia_y(a, b):
    return abs(a["y"] - b["y"])
def distancia_x(a, b):
    return abs(a["x"] - b["x"])
def esta_debajo(a, b):
    return a["y"] > b["y"]
def esta_derecha(a, b):
    return a["x"] > b["x"]
def buscar_etiqueta(datos, palabra):
    palabra = limpiar(palabra)
    for d in datos:
        if palabra in limpiar(d["texto"]):
            return d
    return None
def obtener_region(datos, ymin, ymax):
    region = []
    for d in datos:
        if ymin <= d["y"] <= ymax:
            region.append(d)
    return sorted(region, key=lambda x: (x["y"], x["x"]))
def regex_curp():
    return re.compile(r"[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}")
def regex_fecha():
    return re.compile(r"\d{2}/\d{2}/\d{4}")
def regex_vigencia():
    return re.compile(r"\d{4}-\d{4}")