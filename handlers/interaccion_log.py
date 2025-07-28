# interaccion_log.py

from datetime import datetime

class CopilotLogger:
    def __init__(self, archivo='interacciones.log'):
        self.archivo = archivo

    def registrar(self, evento, contexto=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entrada = f"[{timestamp}] {evento}"
        if contexto:
            entrada += f" | Contexto: {contexto}"
        with open(self.archivo, 'a') as f:
            f.write(entrada + '\n')

# Ejemplo de uso:
logger = CopilotLogger()
logger.registrar("Sincronización CAMBALACHE ↔ Copilot iniciada", "Handlers: 3 activos | Modo sináptico | Usuario: Hernán")
logger.registrar("Sincronización CAMBALACHE ↔ Copilot finalizada", "Handlers: 3 activos | Modo sináptico | Usuario: Hernán")
