"""
Autor: The Bridge
Descripción: Módulo sencillo para practicar docstrings e imports.
"""


def saluda(nombre):
    """
    Devuelve un saludo para la persona indicada.

    Args:
        nombre (str): nombre de la persona

    Returns:
        str: saludo
    """
    nombre_limpio = str(nombre).strip()
    return f"Hola, {nombre_limpio}!"


def despide(nombre):
    """
    Devuelve una despedida para la persona indicada.

    Args:
        nombre (str): nombre de la persona

    Returns:
        str: despedida
    """
    nombre_limpio = str(nombre).strip()
    return f"¡Hasta luego, {nombre_limpio}!"


if __name__ == "__main__":
    print("Pruebas saludos.py")
    print(saluda("Alex"))
    print(despide("Alex"))

