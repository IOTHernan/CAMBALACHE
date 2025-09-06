#!/bin/bash
# Ejemplo: descarga e instala un wheel desde Google Drive

# ID del archivo (obtenelo del enlace de Google Drive)
WHEEL_ID="1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"  # <-- Cambia esto por tu ID real
WHEEL_NAME="mi_paquete-1.0.0-cp310-cp310-manylinux_2_17_x86_64.whl"  # Cambia esto si tu wheel tiene otro nombre

# Descargar el wheel
echo "Descargando $WHEEL_NAME desde Google Drive..."
wget --no-check-certificate "https://drive.google.com/uc?export=download&id=${WHEEL_ID}" -O ${WHEEL_NAME}

# Instalar el wheel en el entorno actual (deberías tener la venv activada)
echo "Instalando $WHEEL_NAME..."
pip install ${WHEEL_NAME}

# Limpieza opcional
rm ${WHEEL_NAME}

echo "¡Listo!"