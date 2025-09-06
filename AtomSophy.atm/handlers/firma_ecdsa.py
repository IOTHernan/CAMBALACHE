from ecdsa import SigningKey, NIST256p
import hashlib

# Ruta del archivo a firmar
archivo = "diploma.svg"

# --- Función para cargar el contenido y obtener su hash SHA-256 ---
def hash_archivo(ruta):
    with open(ruta, "rb") as f:
        contenido = f.read()
    return hashlib.sha256(contenido).digest()

# --- Generar claves (solo para demo; en producción guardá las claves seguras) ---
def generar_claves():
    sk = SigningKey.generate(curve=NIST256p)
    vk = sk.get_verifying_key()
    return sk, vk

# --- Firmar el hash ---
def firmar(sk, hash_msg):
    return sk.sign(hash_msg)

# --- Verificar firma ---
def verificar(vk, firma, hash_msg):
    return vk.verify(firma, hash_msg)

# --- Demo completa ---
if __name__ == "__main__":
    # Generar claves (una sola vez)
    sk, vk = generar_claves()

    # Hashear archivo
    hash_msg = hash_archivo(archivo)

    # Firmar
    firma = firmar(sk, hash_msg)
    print(f"Firma (hex): {firma.hex()}")

    # Verificar
    valid = verificar(vk, firma, hash_msg)
    print("¿Firma válida?", valid)
