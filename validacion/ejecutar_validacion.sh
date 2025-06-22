#!/bin/bash

# Activar el entorno virtual si es necesario
# source /ruta/a/tu/entorno/bin/activate

echo "Iniciando ejecución completa del pipeline..."

# Ejecutar descarga.py
echo "Ejecutando descargar.py..."
python descargar.py
if [ $? -ne 0 ]; then
  echo "Error al ejecutar descargar.py"
  exit 1
fi

# Ejecutar transcribir.py
echo "Ejecutando transcribir.py..."
python transcribir.py
if [ $? -ne 0 ]; then
  echo "Error al ejecutar transcribir.py"
  exit 1
fi

# Ejecutar openai_transcribir.py
echo "Ejecutando openai_transcribir.py..."
python openai_transcribir.py
if [ $? -ne 0 ]; then
  echo "Error al ejecutar transcribir.py"
  exit 1
fi

# Ejecutar distancia.py
echo "Ejecutando distancia.py..."
python distancia.py
if [ $? -ne 0 ]; then
  echo "Error al ejecutar distancia.py"
  exit 1
fi

# Ejecutar graficos.py
echo "Ejecutando graficos.py..."
python graficos.py
if [ $? -ne 0 ]; then
  echo "Error al ejecutar graficos.py"
  exit 1
fi

echo "Ejecutando llamadas_dia.py..."

python llamadas_dia.py
if [ $? -ne 0 ]; then
  echo "Error al ejecutar llamadas_dia.py"
  exit 1
fi

echo "Pipeline completado exitosamente."
