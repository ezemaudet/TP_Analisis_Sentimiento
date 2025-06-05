# TP_Analisis_Sentimiento


### Requisitos especiales del modelo Wisper del sistema
Este proyecto requiere `ffmpeg` instalado en el sistema para que Whisper pueda procesar los archivos de audio.

#### En Ubuntu / Debian:
```bash
sudo apt update
sudo apt install ffmpeg -y

# Instrucciones

Entrar al directorio TP_Analisis_Sentimiento:
cd proyecto_callcenter/TP_Analisis_Sentimiento

Activar el environment:
source env/bin/activate

Variables de entorno en archivo .env
El archivo .env guarda las variables de entorno.
Aqui se configuran las fechas de inicio y fin de las grabaciones, el filtro de la duracion en segundos de la llamada y la cant de grabaciones que queremos analizar. 

API_KEY = os.getenv("API_KEY_vozelia")
TENANT = os.getenv("TENANT_vozelia")
START_DATE = "2025-05-16"
END_DATE = "2025-05-17"
TIME=60 (Filtrado de grabaciones mayores a x segundos)
cant_grab= 10 (Cantidad de grabaciones para testear)
 
Ejectutar archive bash llamado ejecutar.sh
./ejecutar.sh

El archive ejecutar.sh ejecuta lo siguiente:
transcripcion.py
ejecuta un programa que busca las grabaciones mediante una api y las transcribe utilizando el modelo Wisper. Se genera un archivo llamadas.csv que es una data frame de los datos de las grabaciones en caso que se quisiera analizar otro tipo de datos de la llamada como fecha, duracion, numero de extencion, si la llamada fue saliente o entrante etc. Las transcripciones son guardadas en el archivo transcripciones.csv
sentimiento.py
ejecuta un analisis de sentimiento de la transcripcion y lo guarda en el archivo transcripciones.csv el sntimiento de la lamada en una Nueva columna.

