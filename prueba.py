def obtener_empresa(datos):

    if not datos:
        return ""

    datos = sorted(
        datos,
        key=lambda d: d["y"]
    )

    for d in datos:

        texto = d["texto"].strip()
        texto_upper = texto.upper()

        if "ABFORTI" in texto_upper or "AB FORTI" in texto_upper:
            return "ABFORTI"

        if "INNOVET" in texto_upper:
            return "INNOVET"

        if "UPPER" in texto_upper:
            return "UPPER"

    # Respaldo
    return datos[0]["texto"].strip()


def obtener_nombre(datos):

    if not datos:
        return ""

    datos = sorted(
        datos,
        key=lambda d: d["y"]
    )

    candidatos = []

    for i, d in enumerate(datos):

        texto = d["texto"].strip()

        if not texto:
            continue

        texto_upper = texto.upper()


        # ==========================
        # IGNORAR EMPRESA
        # ==========================

        if (
            "ABFORTI" in texto_upper
            or "AB FORTI" in texto_upper
            or "INNOVET" in texto_upper
            or "UPPER" in texto_upper
        ):
            continue


        # ==========================
        # IGNORAR SLOGAN
        # ==========================

        if (
            "LO CREASTE" in texto_upper
            or "PROTEGEMOS" in texto_upper
        ):
            continue


        # ==========================
        # IGNORAR ÚLTIMA LÍNEA
        # Departamento / puesto
        # ==========================

        if i == len(datos) - 1:
            continue


        candidatos.append(texto)


    print("CANDIDATOS DE NOMBRE:")
    print(candidatos)


    if not candidatos:
        return ""


    # El nombre puede venir dividido
    # en una o dos líneas
    nombre = " ".join(candidatos)

    return nombre.strip()


def obtener_departamento(datos):

    if not datos:
        return ""

    datos = sorted(
        datos,
        key=lambda d: d["y"]
    )

    return datos[-1]["texto"].strip()