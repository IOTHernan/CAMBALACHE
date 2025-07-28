import os
import logging
from datetime import datetime

# --- Configuración de logging ---
log_folder = "logs"
log_file = os.path.join(log_folder, "lianbot.log")
os.makedirs(log_folder, exist_ok=True)

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("▶️ CAMBALACHE Environment Check Started")

# --- Folders esenciales ---
folders = [
    "logs",
    "bin",
    "bots",
    "data/indexados",
    "configs"
]

def check_and_create_folders():
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.info(f"📁 Created missing folder: {folder}")
            print(f"[INFO] Creado: {folder}")
        else:
            print(f"[OK] Ya existe: {folder}")

def prompt_run_bot():
    try:
        choice = input("\n¿Deseás ejecutar LianBot Document Explorer ahora? (S/N): ").strip().lower()
        if choice == "s":
            print("[⚙️] Ejecutando bot Flask...")
            os.system("python bots/lianbot_docs.py")
        else:
            print("[🔕] Bot no ejecutado.")
    except Exception as e:
        logging.error(f"Error al ejecutar bot: {e}")
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    check_and_create_folders()
    prompt_run_bot()
