import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("NOT_MY_KEY").encode()


def encrypt_private_key(private_key):
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(KEY), modes.CFB(iv))
    encryptor = cipher.encryptor()

    encrypted = encryptor.update(private_key.encode()) + encryptor.finalize()

    return iv.hex(), encrypted.hex()


def decrypt_private_key(iv_hex, encrypted_hex):
    iv = bytes.fromhex(iv_hex)
    encrypted = bytes.fromhex(encrypted_hex)

    cipher = Cipher(algorithms.AES(KEY), modes.CFB(iv))
    decryptor = cipher.decryptor()

    return (decryptor.update(encrypted) + decryptor.finalize()).decode()