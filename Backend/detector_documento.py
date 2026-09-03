def detectar(datos):
    #para esta función no fue necesario realizar limpieza
    """Detecta si el documento es una INE
    o una credencial de trabajo"""

    texto = " ".join(
        d["texto"] for d in datos
    ).upper()

    if (
        "INSTITUTO NACIONAL ELECTORAL" in texto
        or "CREDENCIAL PARA VOTAR" in texto
        or "CLAVE DE ELECTOR" in texto
        or "CURP" in texto
    ):
        return "INE"
    if (
        "ABFORTI" in texto
        or "AB FORTI" in texto
        or "INNOVET" in texto
        or "UPPER" in texto
        or "DESARROLLO COMERCIAL" in texto
        or "LO CREASTE LO PROTEGEMOS" in texto
    ):
        return "TRABAJO"
    return "DESCONOCIDO"