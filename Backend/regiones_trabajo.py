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


def obtener_empresa(datos):

    if not datos:
        return ""

    datos = sorted(
        datos,
        key=lambda d: d["y"]
    )

    for d in datos:

        texto = normalizar_texto(
            d["texto"]
        )

        if (
            "ABFORTI" in texto
            or "AB FORTI" in texto
        ):
            return "ABFORTI"

        if "INNOVET" in texto:
            return "INNOVET"

        if "UPPER" in texto:
            return "UPPER"

    return ""


def es_empresa_o_logo(texto):

    texto = normalizar_texto(
        texto
    )

    if (
        "ABFORTI" in texto
        or "AB FORTI" in texto
        or "INNOVET" in texto
        or "UPPER" in texto
        or "LOGISTICS" in texto
        or "LOGISTIC" in texto
    ):
        return True

    return False

def es_slogan(texto):

    texto = normalizar_texto(
        texto
    )

    if (
        "LO CREASTE" in texto
        or "PROTEGEMOS" in texto
        or "CREASTE" in texto
    ):
        return True

    return False

def es_ruido(texto):

    texto = normalizar_texto(
        texto
    )

    if not texto:
        return True


    if len(texto) <= 1:
        return True

    if re.fullmatch(
        r"[\d\W_]+",
        texto
    ):
        return True

    return False


def es_departamento(texto):

    texto = normalizar_texto(
        texto
    )

    palabras = [

        # INNOVET
        "ING ",
        "ING.",
        "DESARROLLO",
        "COMERCIAL",

        # ABFORTI
        "TECNOLOG",
        "INFORMACION",

        # UPPER
        "GESTION",
        "CAPITAL HUMANO",

        # Otros posibles cargos
        "ADMINISTRACION",
        "RECURSOS HUMANOS",
        "SISTEMAS",
        "VENTAS",
        "OPERACIONES",
        "LOGISTICA",
        "FINANZAS",
        "CONTABILIDAD"
    ]

    for palabra in palabras:

        if palabra in texto:
            return True

    return False


def obtener_departamento(datos):

    if not datos:
        return ""

    datos = sorted(
        datos,
        key=lambda d: d["y"]
    )

    candidatos = []

    for d in datos:

        texto = d["texto"].strip()

        if not texto:
            continue

        if es_empresa_o_logo(texto):
            continue

        if es_slogan(texto):
            continue

        if es_ruido(texto):
            continue

        if es_departamento(texto):

            candidatos.append(d)

    if not candidatos:
        return ""

    candidatos = sorted(
        candidatos,
        key=lambda d: d["y"]
    )

    return candidatos[-1]["texto"].strip()


def obtener_nombre(datos):

    if not datos:
        return ""

    datos = sorted(
        datos,
        key=lambda d: d["y"]
    )

    departamento = obtener_departamento(
        datos
    )

    y_departamento = None

    if departamento:

        departamento_normalizado = (
            normalizar_texto(
                departamento
            )
        )

        for d in datos:

            if (
                normalizar_texto(
                    d["texto"]
                )
                ==
                departamento_normalizado
            ):

                y_departamento = d["y"]

                break


    candidatos = []


    for d in datos:

        texto = d["texto"].strip()

        if not texto:
            continue


        # --------------------------
        # EMPRESA / LOGO
        # --------------------------

        if es_empresa_o_logo(texto):
            continue



        if es_slogan(texto):
            continue


        if es_ruido(texto):
            continue



        if es_departamento(texto):
            continue

        if (
            y_departamento is not None
            and d["y"] >= y_departamento
        ):
            continue


        candidatos.append(d)


    if not candidatos:
        return ""


    candidatos = sorted(
        candidatos,
        key=lambda d: d["y"]
    )


    if len(candidatos) > 2:

        candidatos = candidatos[-2:]


    lineas_nombre = [

        d["texto"].strip()

        for d in candidatos

    ]


    print(
        "CANDIDATOS DE NOMBRE:",
        lineas_nombre
    )


    nombre = " ".join(
        lineas_nombre
    )


    return nombre.strip()