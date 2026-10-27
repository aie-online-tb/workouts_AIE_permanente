"""
Autor: The Bridge
Descripción: Módulo pequeño para practicar imports y recarga (reload).
"""

import math


def media(nums):
    """
    Calcula la media aritmética de una lista de números.

    Args:
        nums (list[float] | list[int]): lista de números

    Returns:
        float: media
    """
    if not nums:
        raise ValueError("La lista 'nums' no puede estar vacía.")
    return sum(nums) / len(nums)


def desv_std(nums):
    """
    Calcula la desviación estándar **poblacional** de una lista de números.

    Fórmula: sqrt( mean( (x - mean(x))^2 ) )

    Args:
        nums (list[float] | list[int]): lista de números

    Returns:
        float: desviación estándar poblacional
    """
    if not nums:
        raise ValueError("La lista 'nums' no puede estar vacía.")
    m = media(nums)
    var = sum((x - m) ** 2 for x in nums) / len(nums)
    return math.sqrt(var)


if __name__ == "__main__":
    # Pruebas rápidas (solo al ejecutar este fichero directamente)
    datos = [10, 12, 9, 15, 14]
    print("Pruebas mini_stats.py")
    print("media ->", media(datos))
    print("desv_std ->", desv_std(datos))

