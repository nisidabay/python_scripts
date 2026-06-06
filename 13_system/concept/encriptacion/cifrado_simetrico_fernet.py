#!/usr/bin/python3
# Extraido de Youtube: Cifrado Asimétrico con Python. Código facilito
# https://nitratine.net/blog/post/encryption-and-decryption-in-python/

# Symmetric encryption using Fernet class

from pathlib import Path
from dataclasses import dataclass, field
from typing import Any
from cryptography.fernet import Fernet


@dataclass
class EncryptMessage:
    _key: Any = field(default=Fernet.generate_key())

    def __post_init__(self):
        """Generate the fernet key"""

        path = self.key_path()

        if not path.is_file():
            print("[!] Generating new key")
            with open("fernet.key", "wb") as key:
                key.write(self._key)

    def key_path(self):
        """Where the key is stored"""

        return Path(__file__).parent.absolute().joinpath("fernet.key")

    def open_key(self):
        """Read the key"""

        with open("fernet.key", "rb") as key:
            key = key.read()
            self.f_key = Fernet(key)

        return self.f_key

    def encrypt(self):
        """Encrypt the message"""

        message = input("Message you want to encrypt: ").strip()
        msg = message.encode()

        _encrypted = self.open_key().encrypt(msg)
        with open("encrypted_text", "wb") as enc_txt:
            enc_txt.write(_encrypted)

        print(f"message encrypted: {_encrypted}")

    def decrypt(self):
        """ Decrypt the message """

        with open("encrypted_text", "rb") as enc_txt:
            _encrypted = enc_txt.read()

        _decrypted = self.open_key().decrypt(_encrypted)
        print(f"message decrypted: {_decrypted.decode()}")


if __name__ == "__main__":
    # k = EncryptMessage()
    # k.encrypt()
    # k.decrypt()

    f = EncryptMessage()
    f.decrypt()
