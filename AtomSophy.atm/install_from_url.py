import os
import subprocess
import sys

def download_and_install_wheel(url, wheel_name):
    # Descargar el archivo wheel
    print(f"Descargando {wheel_name} desde {url} ...")
    os.system(f"wget --no-check-certificate \"{url}\" -O {wheel_name}")

    # Instalar el wheel
    print(f"Instalando {wheel_name} ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", wheel_name])

    # Eliminar archivo descargado (opcional)
    os.remove(wheel_name)
    print("¡Listo!")

if __name__ == "__main__":
    # Ejemplo para Google Drive
    WHEEL_ID = "1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"  # Cambia esto por tu ID real
    WHEEL_NAME = "mi_paquete-1.0.0-cp310-cp310-manylinux_2_17_x86_64.whl"
    url = f"https://drive.google.com/uc?export=download&id={WHEEL_ID}"

    download_and_install_wheel(url, WHEEL_NAME)