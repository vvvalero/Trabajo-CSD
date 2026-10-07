"""GGH de juguete (seccion 2.1 del PDF) para probar los ataques con ejemplos propios."""
from __future__ import annotations


def keygen(n: int):
    """B, U unimodular, B' = U B. Clave privada <B, U>, publica <B'>."""
    raise NotImplementedError  # TODO


def encrypt(x, B_pub, e):
    """c = x B' + e"""
    raise NotImplementedError  # TODO


def decrypt(c, B_priv, U):
    """y = round(c B^-1);  x = y U^-1"""
    raise NotImplementedError  # TODO
