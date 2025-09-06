# pip install tqdm
# import subprocess
import subprocess
from datetime import datetime
import threading
#import requests
from tqdm import tqdm


def chegit(action):
    if action == 'up':
        try:
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Commit en {date_time}"

            commands = [
                "git add .",
                f"git commit -m '{commit_message}'",
                "git push",
                "git pull"
            ]

            for command in commands:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                print(result.decode())
        except subprocess.CalledProcessError as e:
            print("Error al ejecutar el comando:", e.output.decode())
    else:
        print("Acción no reconocida.")


def descargar_subtitulos( video_url, t_output_file="subtitles.txt"):
    response = requests.get(video_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(t_output_file, 'wb') as f:
        for data in response.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()

    if total_size != 0 and t.n != total_size:
        print("Error: Algo salió mal.")
    else:
        print(f"Subtítulos descargados en {t_output_file}")


def iniciar_descarga(video_url, the_output_file="subtitles.txt"):
    download_thread = threading.Thread(target=descargar_subtitulos, args=(video_url, the_output_file))
    download_thread.start()

# Ejecución directa de funciones
url = input("Ingresa la URL del video de YouTube: ")
output_file = input("Ingresa el nombre del archivo de salida (o presiona Enter para 'subtitles.txt'): ") or "subtitles.txt"

print("Iniciando la descarga de subtítulos...")
iniciar_descarga(url, output_file)
print("Descargando en segundo plano...")
 

 import subprocess
import platform

def ejecutar_powershell(script_name):
    script_path = 'path/to/scripts/powershell_scripts.ps1'
    result = subprocess.run(['powershell.exe', '-File', script_path, '-scriptName', script_name], capture_output=True, text=True)
    print(result.stdout)

def ejecutar_bash(script_name):
    script_path = 'path/to/scripts/bash_scripts.sh'
    result = subprocess.run(['bash', script_path, script_name], capture_output=True, text=True)
    print(result.stdout)

def ejecutar_script(script_name):
    os_system = platform.system()
    if os_system == "Windows":
        ejecutar_powershell(script_name)
    elif os_system == "Linux":
        ejecutar_bash(script_name)
    else:
        raise Exception("Sistema operativo no soportado")

def print_message(msg):
    """Imprime un mensaje en consola."""
    print(f"[INFO] {msg}")

def validate_git_command(command):
    """Valida que el comando de Git sea correcto."""
    # Implementar validación aquí
    return True
