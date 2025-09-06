import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes	
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
# -*- coding: utf-8 -*-	
# Módulo de cifrado y descifrado de datos
# Este módulo proporciona funciones para cifrar y descifrar datos en memoria y archivos
# utilizando AES-256 con PBKDF2 para derivar claves a partir de contraseñas.
# Este código es parte de AtomSophy, un sistema operativo minimalista y educativo.	

# Variables de entorno estilo CP/M+
entorno = {
    "prompt": "ATM> ",
}
backend = default_backend()
salt_size = 16
key_size = 32  # AES-256
iterations = 100_000
block_size = 128


def encrypt_and_save(data: bytes, password: str, output_path: str):
    encrypted = encrypt_bytes(data, password)
    with open(output_path, "wb") as f:
        f.write(encrypted)

def load_and_decrypt(input_path: str, password: str) -> bytes:
    with open(input_path, "rb") as f:
        enc_data = f.read()
    return decrypt_bytes(enc_data, password)


def handle_encrypt_ram(params):
    if len(params) < 2:
        print("Uso: encrypt_ram 'texto o datos' clave")
        return
    texto = params[0]
    clave = params[1]

    data = texto.encode()
    encrypted = encrypt_bytes(data, clave)
    print(f"[encrypt_ram] Datos cifrados en RAM: {encrypted.hex()}")


def handle_decrypt_ram(params):
    if len(params) < 2:
        print("Uso: decrypt_ram datos_hex clave")
        return
    datos_hex = params[0]
    clave = params[1]

    try:
        encrypted = bytes.fromhex(datos_hex)
        decrypted = decrypt_bytes(encrypted, clave)
        print(f"[decrypt_ram] Datos descifrados: {decrypted.decode()}")
    except Exception as e:
        print(f"[x] Error descifrando datos RAM: {e}")


def encrypt_bytes(data: bytes, password: str) -> bytes:

    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding

    salt = os.urandom(salt_size)
    key = derive_key(password.encode(), salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(block_size).padder()
    
    padded_data = padder.update(data) + padder.finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    return salt + iv + encrypted

def decrypt_bytes(enc_data: bytes, password: str) -> bytes:
    salt = enc_data[:salt_size]
    iv = enc_data[salt_size:salt_size+16]
    ciphertext = enc_data[salt_size+16:]
    
    key = derive_key(password.encode(), salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(block_size).unpadder()
    
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data


def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_size,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    return kdf.derive(password)

def encrypt_file(input_path, password, output_path=None):
    if output_path is None:
        output_path = input_path + ".enc"

    salt = os.urandom(salt_size)
    key = derive_key(password.encode(), salt)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(block_size).padder()

    with open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
        # Escribimos la sal y el IV al inicio
        f_out.write(salt)
        f_out.write(iv)

        while True:
            chunk = f_in.read(1024)
            if len(chunk) == 0:
                break
            padded_data = padder.update(chunk)
            enc_data = encryptor.update(padded_data)
            f_out.write(enc_data)

        # Finalizamos padding y cifrado
        padded_data = padder.finalize()
        enc_data = encryptor.update(padded_data) + encryptor.finalize()
        f_out.write(enc_data)

def decrypt_file(input_path, password, output_path=None):
    if output_path is None:
        if input_path.endswith(".enc"):
            output_path = input_path[:-4]
        else:
            output_path = input_path + ".dec"

    with open(input_path, "rb") as f_in:
        salt = f_in.read(salt_size)
        iv = f_in.read(16)
        key = derive_key(password.encode(), salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(block_size).unpadder()

        with open(output_path, "wb") as f_out:
            while True:
                chunk = f_in.read(1024)
                if len(chunk) == 0:
                    break
                dec_data = decryptor.update(chunk)
                data = unpadder.update(dec_data)
                f_out.write(data)

            # Finalizamos descifrado y quitamos padding
            dec_data = decryptor.finalize()
            data = unpadder.update(dec_data) + unpadder.finalize()
            f_out.write(data)

# --- Handler para AtomSophy ---

def handle_encrypt(params):
    if len(params) < 2:
        print("Uso: encrypt archivo clave [--type-encrypt AES]")
        return

    archivo = params[0]
    clave = params[1]

    print(f"[encrypt] Cifrando {archivo} con AES...")
    try:
        encrypt_file(archivo, clave)
        print(f"[encrypt] Archivo cifrado: {archivo}.enc")
    except Exception as e:
        print(f"[x] Error en cifrado: {e}")

def handle_decrypt(params):
    if len(params) < 2:
        print("Uso: decrypt archivo.clave [--type-encrypt AES]")
        return

    archivo = params[0]
    clave = params[1]

    print(f"[decrypt] Descifrando {archivo} con AES...")
    try:
        decrypt_file(archivo, clave)
        print(f"[decrypt] Archivo descifrado guardado.")
    except Exception as e:
        print(f"[x] Error en descifrado: {e}")


def handle_echo(params):
    print(" ".join(params))

def handle_set(params):
    if len(params) >= 2:
        entorno[params[0]] = " ".join(params[1:])
        print(f"{params[0]} = {entorno[params[0]]}")
    else:
        print("Uso: set var valor")



def encrypt_bytes(data: bytes, password: str) -> bytes:
    salt = os.urandom(salt_size)
    key = derive_key(password.encode(), salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(block_size).padder()
    
    padded_data = padder.update(data) + padder.finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    return salt + iv + encrypted

def decrypt_bytes(enc_data: bytes, password: str) -> bytes:
    salt = enc_data[:salt_size]
    iv = enc_data[salt_size:salt_size+16]
    ciphertext = enc_data[salt_size+16:]
    
    key = derive_key(password.encode(), salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(block_size).unpadder()
    
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data


def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_size,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    return kdf.derive(password)

def encrypt_file(input_path, password, output_path=None):
    if output_path is None:
        output_path = input_path + ".enc"

    salt = os.urandom(salt_size)
    key = derive_key(password.encode(), salt)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(block_size).padder()

    with open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
        # Escribimos la sal y el IV al inicio
        f_out.write(salt)
        f_out.write(iv)

        while True:
            chunk = f_in.read(1024)
            if len(chunk) == 0:
                break
            padded_data = padder.update(chunk)
            enc_data = encryptor.update(padded_data)
            f_out.write(enc_data)

        # Finalizamos padding y cifrado
        padded_data = padder.finalize()
        enc_data = encryptor.update(padded_data) + encryptor.finalize()
        f_out.write(enc_data)

def decrypt_file(input_path, password, output_path=None):
    if output_path is None:
        if input_path.endswith(".enc"):
            output_path = input_path[:-4]
        else:
            output_path = input_path + ".dec"

    with open(input_path, "rb") as f_in:
        salt = f_in.read(salt_size)
        iv = f_in.read(16)
        key = derive_key(password.encode(), salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(block_size).unpadder()

        with open(output_path, "wb") as f_out:
            while True:
                chunk = f_in.read(1024)
                if len(chunk) == 0:
                    break
                dec_data = decryptor.update(chunk)
                data = unpadder.update(dec_data)
                f_out.write(data)

            # Finalizamos descifrado y quitamos padding
            dec_data = decryptor.finalize()
            data = unpadder.update(dec_data) + unpadder.finalize()
            f_out.write(data)
