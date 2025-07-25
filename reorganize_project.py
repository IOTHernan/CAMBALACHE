import os
import shutil
import glob
import json

def create_dirs(dirs):
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"[+] Directory created: {d}")
        else:
            print(f"[OK] Directory exists: {d}")

def move_files(movimientos):
    for mov in movimientos:
        origen = mov['origen']
        destino = mov['destino']
        
        # Si es wildcard, usar glob
        files_to_move = glob.glob(origen)
        
        if not files_to_move:
            print(f"[!] No files match: {origen}")
            continue
        
        for f in files_to_move:
            filename = os.path.basename(f)
            destino_path = os.path.join(destino, filename) if os.path.isdir(destino) else destino
            
            # Si destino es archivo completo (no dir), crear carpeta padre
            if not os.path.isdir(destino) and not os.path.exists(os.path.dirname(destino)):
                os.makedirs(os.path.dirname(destino))
            
            try:
                shutil.move(f, destino_path)
                print(f"[→] Moved {f} -> {destino_path}")
            except Exception as e:
                print(f"[X] Failed to move {f}: {e}")

def main():
    json_path = 'exportar_proyecto_de_ai.json'
    if not os.path.exists(json_path):
        print(f"[ERROR] Config file not found: {json_path}")
        return
    
    with open(json_path, 'r') as jf:
        config = json.load(jf)
    
    create_dirs(config.get('directorios', []))
    move_files(config.get('movimientos', []))

if __name__ == '__main__':
    main()
