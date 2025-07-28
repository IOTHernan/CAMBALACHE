import os
import shutil
import hashlib
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileIndex:
    def __init__(self, path):
        self.path = path
        self.index = self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.index, f, indent=4)

    def update(self, filename, filehash, last_modified, status):
        self.index[filename] = {
            'hash': filehash,
            'last_modified': last_modified,
            'status': status
        }

    def get(self, filename):
        return self.index.get(filename, None)

def hash_file(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def malware_hunter_scan(filepath):
    # Placeholder: Integrar el módulo real de análisis
    logging.info(f"Escaneando archivo para malware: {filepath}")
    # Resultado simulado
    return 'clean'  # o 'infected'

def reorganize_files(src_dir, dest_dir, index_path):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    index = FileIndex(index_path)

    for root, _, files in os.walk(src_dir):
        for file in files:
            src_path = os.path.join(root, file)
            file_hash = hash_file(src_path)
            last_modified = datetime.fromtimestamp(os.path.getmtime(src_path)).isoformat()
            dest_path = os.path.join(dest_dir, file)

            record = index.get(file)
            if not record or record['hash'] != file_hash:
                shutil.copy2(src_path, dest_path)
                status = malware_hunter_scan(dest_path)
                index.update(file, file_hash, last_modified, status)
                logging.info(f'Archivo actualizado y escaneado: {file} ({status})')
            else:
                logging.info(f'Archivo sin cambios: {file}')

    index.save()

if __name__ == "__main__":
    origen = "ruta/a/carpeta/origen"
    destino = "ruta/a/carpeta/destino"
    index_file = "file_index.json"
    reorganize_files(origen, destino, index_file)
