import re
import unicodedata


def normalizar_texto(texto):

    if not texto:
        return ""

    texto = texto.strip()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.upper().strip()


def es_empresa(texto):

    t = normalizar_texto(texto)

    return (
        "ABFORTI" in t
        or "AB FORTI" in t
        or "INNOVET" in t
        or "UPPER LOGISTICS" in t
        or "UPPER" in t
        or "LOGISTICS" in t
        or "LOGISTIC" in t
    )


def obtener_empresa(datos):

    if not datos:
        return ""

    datos = sorted(
        datos,
        key=lambda d: d["y"]
    )

    for d in datos:

        t = normalizar_texto(
            d["texto"]
        )

        if (
            "ABFORTI" in t
            or "AB FORTI" in t
        ):
            return "ABFORTI"

        if "INNOVET" in t:
            return "INNOVET"

        if "UPPER" in t:
            return "UPPER"

    return ""


# =========================================================
# SLOGAN
# =========================================================

def es_slogan(texto):

    t = normalizar_texto(texto)

    return (
        "CREASTE" in t
        or "PROTEGEMOS" in t
    )


# =========================================================
# RUIDO OCR
# =========================================================

def es_ruido(texto):

    t = normalizar_texto(texto)

    if not t:
        return True

    # Ejemplos:
    # 0
    # 1
    # |
    # .
    if len(t) <= 1:
        return True

    if re.fullmatch(
        r"[\d\W_]+",
        t
    ):
        return True

    return False


# =========================================================
# DETECTAR CARGO / DEPARTAMENTO
# =========================================================

def es_departamento(texto):

    t = normalizar_texto(texto)

    palabras_cargo = [
        "ING.",
        "ING ",
        "ING DE",
        "DESARROLLO",
        "COMERCIAL",
        "TECNOLOG",
        "INFORMACION",
        "GESTION",
        "CAPITAL HUMANO",
        "RECURSOS HUMANOS",
        "ADMINISTRACION",
        "OPERACIONES",
        "LOGISTICA",
        "SISTEMAS",
        "VENTAS",
        "CONTABILIDAD",
        "FINANZAS",
        "MERCADOTECNIA",
        "MEXICO"
    ]

    for palabra in palabras_cargo:

        if palabra in t:
            return True

    return False


# =========================================================
# LÍNEAS ÚTILES
# =========================================================

def obtener_lineas_utiles(datos):

    lineas = []

    datos_ordenados = sorted(
        datos,
        key=lambda d: (
            d["y"],
            d["x"]
        )
    )

    for d in datos_ordenados:

        texto = d["texto"].strip()

        if not texto:
            continue

        if es_empresa(texto):
            continue

        if es_slogan(texto):
            continue

        if es_ruido(texto):
            continue

        lineas.append(d)

    return lineas


# =========================================================
# NOMBRE
# =========================================================

def obtener_nombre(datos):

    if not datos:
        return ""

    lineas = obtener_lineas_utiles(
        datos
    )

    candidatos = []

    for d in lineas:

        texto = d["texto"].strip()

        # El cargo NO debe formar
        # parte del nombre
        if es_departamento(texto):
            continue

        candidatos.append(d)

    if not candidatos:
        return ""

    # Nos interesan las últimas líneas
    # de texto no pertenecientes a empresa/cargo.
    #
    # ABFORTI puede tener 2.
    # INNOVET y UPPER normalmente 1.

    if len(candidatos) > 2:
        candidatos = candidatos[-2:]

    candidatos = sorted(
        candidatos,
        key=lambda d: d["y"]
    )

    lineas_nombre = [
        d["texto"].strip()
        for d in candidatos
    ]

    print(
        "CANDIDATOS DE NOMBRE:",
        lineas_nombre
    )

    return " ".join(
        lineas_nombre
    ).strip()


# =========================================================
# DEPARTAMENTO / CARGO
# =========================================================

def obtener_departamento(datos):

    if not datos:
        return ""

    lineas = obtener_lineas_utiles(
        datos
    )

    for d in lineas:

        texto = d["texto"].strip()

        if es_departamento(texto):
            return texto

    return ""