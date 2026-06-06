#!/usr/bin/python3

# Encriptación con werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.context import CryptContext


contexto = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000

    )

texto="esto es un texto de prueba"

texto_encriptado1=generate_password_hash(texto, "pbkdf2:sha256:30000")
# texto_encriptado2=generate_password_hash(texto, "sha256")
# texto_encriptado3=generate_password_hash(texto, "sha256", 30)
# texto_encriptado4=generate_password_hash(texto, "pbkdf2:sha256")
# texto_encriptado5=generate_password_hash(texto, "pbkdf2:sha256:30", 100)
texto_encriptado2 = contexto.hash(texto)

print(texto_encriptado1)
print(texto_encriptado2)
# print(texto_encriptado2)
# print(texto_encriptado3)
# print(texto_encriptado4)
# print(texto_encriptado5)
# 
print(check_password_hash(texto_encriptado1, texto))
print(contexto.verify(texto, texto_encriptado2))
# print(check_password_hash(texto_encriptado2, texto))
# print(check_password_hash(texto_encriptado3, texto))
# print(check_password_hash(texto_encriptado4, texto))
# print(check_password_hash(texto_encriptado5, texto))
