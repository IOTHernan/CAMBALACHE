import os
import zipfile
import tarfile

def buscar_import_os(ruta):
    for root, dirs, files in os.walk(ruta):
        for file in files:
            path = os.path.join(root, file)
            try:
                if file.endswith(('.py', '.txt', '.md')):
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        if 'import os' in f.read():
                            print(f"[+] Detectado en: {path}")
                elif file.endswith('.zip'):
                    with zipfile.ZipFile(path, 'r') as zip_ref:
                        for name in zip_ref.namelist():
                            if name.endswith('.py'):
                                with zip_ref.open(name) as f:
                                    if b'import os' in f.read():
                                        print(f"[+] Detectado en ZIP: {path} → {name}")
                elif file.endswith(('.tar.gz', '.tgz')):
                    with tarfile.open(path, 'r:gz') as tar:
                        for member in tar.getmembers():
                            if member.name.endswith('.py'):
                                f = tar.extractfile(member)
                                if f and b'import os' in f.read():
                                    print(f"[+] Detectado en TAR: {path} → {member.name}")
            except Exception as e:
                print(f"[!] Error en {path}: {e}")

# Ejecución
buscar_import_os("C:/ruta/o/home/atm")
