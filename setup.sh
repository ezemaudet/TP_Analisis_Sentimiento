#!/bin/bash

# Actualizamos el sistema
sudo apt update

# Instalamos ffmpeg
sudo apt install ffmpeg -y

# Creamos el entorno virtual (si no existe)
python3 -m venv env

# Activamos el entorno virtual
source env/bin/activate

# Instalamos dependencias de Python
pip install -r requirements.txt

echo "Instalación completada correctamente."
