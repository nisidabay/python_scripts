#!/usr/bin/python3
# Método de encriptacion Atbash.
# Diccionario al revés

import string
import argparse


def alfabeto_inverso():
    """ Genera el alfabeto inverso en mayúsculas """

    temp = string.ascii_uppercase
    l_temp = len(temp) + 1
    return temp[-1:-l_temp:-1]


def cifrado(mensaje: str) -> str:
    """ Cifra un texto método atbash """

    alfabeto = string.ascii_lowercase  # abc...
    cifra = alfabeto_inverso()  # ZYX...
    mensaje_cifrado = ""

    for letra in mensaje.lower():
        if letra in alfabeto:
            pos = alfabeto.index(letra)
            mensaje_cifrado += cifra[pos]
        else:  # Añade el espacio
            mensaje_cifrado += letra

    return (mensaje_cifrado)


parser = argparse.ArgumentParser(
    description="Encripta un archivo de texto plano con el método Atbash",
    epilog="Ejemplo: python atbash-cipher.py 'texto'")

# Argumentos
parser.add_argument("mensaje", type=str, help="Texto plano a cifrar.")

# Recoge los argumentos
args = parser.parse_args()

# Función que realiza el cifrado
salida = f"[+] {cifrado(args.mensaje)}"
print(salida)
