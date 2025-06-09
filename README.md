# Sistema de Transcripción y Análisis de Sentimiento
Este sistema permite:
- Descargar grabaciones desde la central de Vozelia vía API.
- Transcribir automáticamente las llamadas utilizando Whisper.
- Analizar el sentimiento de cada llamada transcrita.
- Generar reportes en archivos estructurados.

Activar el environment:
source env/bin/activate

## Instalación automática

Clonar el repositorio y ejecutar el script de instalación:
git clone <tu_repo>
cd TP_Analisis_Sentimiento

# Ejecutar el setup para preparar todo el entorno
./setup.sh

Este script realiza:
Actualización del sistema.
Instalación de ffmpeg (requerido por Whisper).
Creación y activación de un entorno virtual env/.
Instalación automática de las dependencias de Python desde requirements.txt.


Configuración del sistema
Configurar las variables de entorno en el archivo .env (se debe crear manualmente):
Variables de entorno en archivo .env
El archivo .env guarda las variables de entorno.
Aqui se configuran las fechas de inicio y fin de las grabaciones, el filtro de la duracion en segundos de la llamada y la cant de grabaciones que queremos analizar. 

API_KEY_vozelia=xxxxxxxxxxxx
TENANT_vozelia=xxxxxxxx
START_DATE=2025-05-16 Fechas de las grabaciones a descargar.
END_DATE=2025-05-17 Fechas de las grabaciones a descargar.
TIME=60 Filtro de duración mínima de las llamadas (en segundos).
cant_grab=10 Cantidad de grabaciones a procesar.

Ejecución automática
Con el entorno preparado y el .env configurado, ejecutar el pipeline completo:
./ejecutar.sh

El script ejecuta los siguientes módulos:

transcripcion.py
Descarga grabaciones desde Vozelia mediante API.
Realiza la transcripción de las llamadas.
Genera un archivos con el log de llamadas.csv y las transcripciones.csv

sentimiento.py
Analiza el sentimiento de cada transcripción.
Agrega la columna sentimiento al archivo transcripciones.csv.

Archivos generados
llamadas.csv → Detalle completo de las llamadas descargadas.

transcripciones.csv → Transcripciones completas con el análisis de sentimiento incluido.

Estructura del Proyecto:

Entrar al directorio TP_Analisis_Sentimiento:
cd proyecto_callcenter/TP_Analisis_Sentimiento
README.md
.env
requirements.txt
setup.sh
transcripciones.csv
ejecutar.sh
llamadas.csv
transcripcion.py
sentimiento.py

validacion/README_validacion.md
ejecutar_validacion-sh
validacion/descargar.py
validacion/transcribir.py
validacion/distancia.py
validacion/graficos.py

validacion/transcripciones/transcripciones_tiempos.csv
validacion/transcripciones/evaluacion_metricas.csv
validacion/transcripciones/true_transcripciones.csv
validacion/transcripciones/distancia_por_modelo.png
validacion/transcripciones/tiempo_por_modelo.png



Notas adicionales
Totalmente compatible con entornos headless (servidores remotos, VMs sin GUI).
Los gráficos se generan como archivos .png listos para visualización posterior.
Control de dependencias centralizado en requirements.txt.
Se require un minimo de 16Gigas de memoria RAM para corer el modelo medium.
