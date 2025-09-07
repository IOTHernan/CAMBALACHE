#!/bin/bash
# ============================================
# CAMBALACHE Setup Script - Codespaces / Cloud
# Autor: Dr. Chapatin
# Fecha: 2025-09-06
# Descripción: Instala VOSK, modelos y dependencias Python
#              para ejecutar AtomSophy en GitHub Codespaces.
# ============================================

echo "💡 Iniciando setup de CAMBALACHE en Codespaces..."

# 1️⃣ Actualizar apt y paquetes base
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y wget unzip build-essential portaudio19-dev

# 2️⃣ Crear carpetas base si no existen
mkdir -p ./models ./logs ./sandbox ./handlers

# 3️⃣ Descargar modelo VOSK pequeño en español si no existe
if [ ! -d "./models/vosk-model-small-es-0.42" ]; then
    echo "📥 Descargando modelo VOSK español..."
    cd ./models
    wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
    unzip vosk-model-small-es-0.42.zip
    rm vosk-model-small-es-0.42.zip
    cd ..
fi

# 4️⃣ Instalar dependencias Python
echo "🐍 Instalando dependencias Python..."
python3 -m pip install --upgrade pip
pip install vosk langdetect transformers torch

# 5️⃣ Mensaje final
echo "✅ Setup completado: VOSK, modelos y dependencias Python listas."
echo "💡 Para ejecutar AtomSophy: python3 main.py"

# ============================================
# Fin del script
# ============================================
