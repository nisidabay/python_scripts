#!/usr/bin/python3
"""Symmetric encryption using Fernet class"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Any
from cryptography.fernet import Fernet


@dataclass
class EncryptMessage:
    """Encryption/Decryption using Fernet"""
    _key: Any = field(default=Fernet.generate_key())

    def __post_init__(self):
        """Generate the fernet key"""

        path = self.key_path()

        if not path.is_file():
            print("[!] Generating new key")
            with open("fernet.key", "wb") as key:
                key.write(self._key)

    @staticmethod
    def key_path() -> Path:
        """Where the key is stored"""

        return Path(__file__).parent.absolute().joinpath("fernet.key")

    @staticmethod
    def open_key():
        """Read the key"""

        with open("fernet.key", "rb") as key:
            key = key.read()

        f_key = Fernet(key)

        return f_key

    def encrypt(self, message: str):
        """Encrypt the message"""

        tmp = message.strip()
        msg = tmp.encode()

        _encrypted = self.open_key().encrypt(msg)
        with open("encrypted_text", "wb") as enc_txt:
            enc_txt.write(_encrypted)

        print(f"message encrypted: {_encrypted}")

    def decrypt(self):
        """ Decrypt the message """

        with open("encrypted_text", "rb") as enc_txt:
            _encrypted = enc_txt.read()

        decrypted = self.open_key().decrypt(_encrypted)
        print(f"message decrypted: {decrypted.decode()}")
