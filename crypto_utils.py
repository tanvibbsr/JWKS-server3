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


def decrypt_private_key(_, encrypted_hex):
    encrypted = bytes.fromhex(encrypted_hex)

    # If you stored IV inside encryption, you must handle it differently
    return encrypted.decode(errors="ignore")