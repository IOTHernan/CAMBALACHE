# #DangerZone #Monitoreo #Watchdog #AnalizeEML #Python #Automatizacion

import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Importamos analize_eml, suponiendo que está en el mismo directorio o path accesible
# Si está en otro módulo, ajustá el import o la ruta
from analize_eml import analize_eml  # Cambiá por tu módulo real

class DangerZoneHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"Archivo creado: {event.src_path}")
            self.analizar(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"Archivo modificado: {event.src_path}")
            self.analizar(event.src_path)

    def analizar(self, filepath):
        try:
            resultado = analize_eml(filepath)
            logging.info(f"Análisis completado para {filepath}")
            logging.info(f"URLs encontradas: {resultado['total_urls_found']}")
            logging.info(f"Nuevas URLs guardadas: {len(resultado['new_urls'])}")
            for url, status in resultado['url_status'].items():
                logging.info(f"{url} --> {status}")
        except Exception as e:
            logging.error(f"Error analizando {filepath}: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("dangerzone.log"),
                                  logging.StreamHandler()])

    path_to_watch = r"H:\CHE\DangerZone"
    event_handler = DangerZoneHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()
    logging.info(f"Monitoreo iniciado en: {path_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
