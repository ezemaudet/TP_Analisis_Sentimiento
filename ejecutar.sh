#!/bin/bash

# Activar el entorno virtual si es necesario
# source /ruta/a/tu/entorno/bin/activate

# Ejecutar el primer script
echo "Ejecutando transcripcion.py..."
python transcripcion.py

# Verificar si el primer script se ejecutó correctamente
if [ $? -ne 0 ]; then
  echo "Error al ejecutar transcripcion.py"
  exit 1
fi

# Ejecutar el segundo script
echo "Ejecutando sentimiento.py..."
python sentimiento.py

# Verificar si el segundo script se ejecutó correctamente
if [ $? -ne 0 ]; then
  echo "Error al ejecutar sentimiento.py"
  exit 1
fi

echo "Ejecución completada exitosamente."
