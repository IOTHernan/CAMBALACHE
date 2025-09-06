
def montar_vhd(vhd_path: str, drive_letter: str = "Z"):
    """
    Monta un archivo VHD en Windows usando PowerShell.
    """
    cmd = f"""
    PowerShell -Command "
    Mount-VHD -Path '{vhd_path}' -PassThru | Get-Disk | 
    Set-Partition -NewDriveLetter {drive_letter}"
    """
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error al montar VHD: {result.stderr}")
    print(f"[*] Disco VHD montado en {drive_letter}:")


def desmontar_vhd(vhd_path: str):
    """
    Desmonta un archivo VHD en Windows usando PowerShell.
    """
    cmd = f"PowerShell -Command Unmount-VHD -Path '{vhd_path}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error al desmontar VHD: {result.stderr}")
    print("[*] Disco VHD desmontado.")


def convertir_vdi_a_raw(vdi_path: str, raw_path: str):  # Bloque con sangría previsto
    cmd = ["VBoxManage", "clonehd", vdi_path, raw_path, "--format", "RAW"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error al convertir VDI a RAW: {result.stderr}")
        print(f"[*] VDI convertido a RAW: {raw_path}")


def montar_raw(raw_path: str, drive_letter: str = "Y"):
    cmd = f"""
    PowerShell -Command "
    Mount-DiskImage -ImagePath '{raw_path}' | Get-Disk | 
    Set-Partition -NewDriveLetter {drive_letter}"
    """
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error al montar RAW: {result.stderr}")
    print(f"[*] RAW montado en {drive_letter}")


def desmontar_raw(raw_path: str):
    cmd = f"PowerShell -Command Dismount-DiskImage -ImagePath '{raw_path}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error al desmontar RAW: {result.stderr}")
    print("[*] RAW desmontado.")


def mount_vdi(vdi_path: str, drive_letter: str = "Z"):
    """
    Convierte un archivo VDI a formato RAW y lo monta como una unidad.

    Parámetros:
        vdi_path (str): Ruta al archivo VDI.
        drive_letter (str): Letra de la unidad para el montaje (por defecto 'Z').
    """
    if not os.path.isfile(vdi_path):
        print(f"[Error] El archivo {vdi_path} no existe.")
        return False

    # Ruta al archivo RAW convertido
    raw_path = vdi_path.replace(".vdi", ".raw")

    # Paso 1: Convertir VDI a RAW
    print(f"[*] Convirtiendo {vdi_path} a {raw_path}...")
    convert_cmd = ["VBoxManage", "clonehd", vdi_path, raw_path, "--format", "RAW"]
    try:
        subprocess.run(convert_cmd, check=True, capture_output=True, text=True)
        print(f"[*] Conversión exitosa: {raw_path}")
    except subprocess.CalledProcessError as e:
        print(f"[Error] Falló la conversión del VDI: {e.stderr}")
        return False

    # Paso 2: Montar RAW usando PowerShell
    print(f"[*] Montando {raw_path} en la unidad {drive_letter}...")
    mount_cmd = f"""
    PowerShell -Command "
    Mount-DiskImage -ImagePath '{raw_path}' | Get-Disk | 
    Set-Partition -NewDriveLetter {drive_letter}"
    """
    try:
        subprocess.run(
            mount_cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"[*] RAW montado correctamente en {drive_letter}:\\")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Error] Falló el montaje del RAW: {e.stderr}")
        return False


# def mount_vdi(vdi_path: str, drive_letter: str = "Z"):  # noqa: F811
#     """
#     Convierte un archivo VDI a formato RAW y lo monta como una unidad.
#     """
#     if not os.path.isfile(vdi_path):
#         print(f"[Error] El archivo {vdi_path} no existe.")
#         return False

#     # Ruta al archivo RAW convertido
#     raw_path = vdi_path.replace(".vdi", ".raw")

#     # Paso 1: Convertir VDI a RAW
#     print(f"[*] Convirtiendo {vdi_path} a {raw_path}...")
#     convert_cmd = ["VBoxManage", "clonehd", vdi_path, raw_path, "--format", "RAW"]
#     try:
#         subprocess.run(convert_cmd, check=True, capture_output=True, text=True)
#         print(f"[*] Conversión exitosa: {raw_path}")
#     except subprocess.CalledProcessError as e:
#         print(f"[Error] Falló la conversión del VDI: {e.stderr}")
#         return False

#     # Paso 2: Montar RAW usando PowerShell
#     print(f"[*] Montando {raw_path} en la unidad {drive_letter}...")
#     mount_cmd = f"""
#     PowerShell -Command "
#     Mount-DiskImage -ImagePath '{raw_path}' | Get-Disk | 
#     Set-Partition -NewDriveLetter {drive_letter}"
#     """
#     try:
#         subprocess.run(
#             mount_cmd, shell=True, check=True, capture_output=True, text=True
#         )
#         print(f"[*] RAW montado correctamente en {drive_letter}:\\")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"[Error] Falló el montaje del RAW: {e.stderr}")
#         return False

