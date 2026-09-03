from Backend.utilidades import buscar_etiqueta
#Había hecho limpieza en regiones pero la detección y ubicación si es importante.
def obtener_nombre(datos):
    etiqueta_nombre = buscar_etiqueta(datos, "NOMBRE")
    etiqueta_domicilio = buscar_etiqueta(datos, "DOMICILIO")
    if etiqueta_domicilio is None:
        etiqueta_domicilio = buscar_etiqueta(datos, "DOMCILIO")
    if etiqueta_nombre is None or etiqueta_domicilio is None:
        return ""
    nombre = []
    for d in datos:
        if etiqueta_nombre["y"] < d["y"] < etiqueta_domicilio["y"]:
            texto = d["texto"].upper()
            if "SEXO" in texto:
                continue
            if len(texto) < 2:
                continue
            nombre.append(d)
    nombre.sort(key=lambda x: x["y"])
    return " ".join(x["texto"] for x in nombre)
def obtener_domicilio(datos):
    etiqueta_domicilio = buscar_etiqueta(datos, "DOMICILIO")
    if etiqueta_domicilio is None:
        etiqueta_domicilio = buscar_etiqueta(datos, "DOMCILIO")
    if etiqueta_domicilio is None:
        return ""
    limite = None
    for d in datos:
        t = d["texto"].upper()
        if "CURP" == t:
            limite = d["y"]
            break
        if "CLAVE" in t and "ELECTOR" in t:
            limite = d["y"]
            break
    if limite is None:
        return ""
    domicilio = []
    for d in datos:
        if etiqueta_domicilio["y"] < d["y"] < limite:
            texto = d["texto"].upper()
            if "CURP" in texto:
                continue
            if "CLAVE" in texto:
                continue
            if "REGISTRO" in texto:
                continue
            if "SECCION" in texto:
                continue
            domicilio.append(d)
    domicilio.sort(key=lambda x: x["y"])
    return " ".join(x["texto"] for x in domicilio)
def obtener_clave(datos):
    etiqueta = None
    for d in datos:
        texto = d["texto"].upper().replace(" ", "")
        if "CLAVE" in texto and "ELECTOR" in texto:
            etiqueta = d
            break
    if etiqueta is None:
        return ""
    # Caso 1: la clave viene pegada al texto
    texto = etiqueta["texto"].upper().replace(" ", "")
    if "ELECTOR" in texto:
        pos = texto.find("ELECTOR") + len("ELECTOR")
        clave = texto[pos:]
        if len(clave) >= 18:
            return clave
    # Caso 2: buscar a la derecha
    candidatos = []
    for d in datos:
        if abs(d["y"] - etiqueta["y"]) < 60 and d["x"] > etiqueta["x"]:
            candidatos.append(d)
    candidatos.sort(key=lambda x: x["x"])
    if candidatos:
        return candidatos[0]["texto"]
    return ""
def obtener_curp(datos):
    import re
    patron = r"[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}"
    for d in datos:
        texto = d["texto"].upper().replace(" ", "")
        m = re.search(patron, texto)
        if m:
            return m.group()
    return ""
def obtener_fecha(datos):
    import re
    patron = r"\d{2}/\d{2}/\d{4}"
    for d in datos:
        m = re.search(patron, d["texto"])
        if m:
            return m.group()
    return ""
def obtener_vigencia(datos):
    import re
    patron = r"\d{4}-\d{4}"
    for d in datos:
        m = re.search(patron, d["texto"])
        if m:
            return m.group()
    return ""