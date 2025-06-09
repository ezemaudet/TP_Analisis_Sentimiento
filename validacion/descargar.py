import os
import requests
from dotenv import load_dotenv
import pandas as pd
import subprocess

# Cargamos variables de entorno
load_dotenv()
API_KEY = os.getenv("API_KEY_vozelia")
TENANT = os.getenv("TENANT_vozelia")

# Creamos carpeta de audios etiquetados si no existe
os.makedirs("audios_etiquetados", exist_ok=True)

# Lista de grabaciones a descargar
grabaciones = [
    "audio_cpbx06.vozelia.com.pa-1748869173.19935707.wav",
    "audio_cpbx06.vozelia.com.pa-1748869815.19945115.wav",
    "audio_cpbx06.vozelia.com.pa-1748869967.19947341.wav"
]

# Inicializamos lista para registrar formatos
detalle_formatos = []

# Función para detectar formato con ffprobe
def detectar_formato(archivo):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=format_name",
        "-of", "default=noprint_wrappers=1:nokey=1",
        archivo
    ]
    try:
        formato = subprocess.check_output(cmd).decode().strip()
        return formato
    except subprocess.CalledProcessError:
        return "Formato desconocido"

# Descargamos las grabaciones
for nombre_archivo in grabaciones:
    recording_id = nombre_archivo.replace("audio_", "").replace(".wav", "")
    url = f"https://pbxone.vozelia.com.pa/pbx/proxyapi.php?key={API_KEY}&reqtype=INFO&info=recording&id={recording_id}&tenant={TENANT}"

    destino = os.path.join("audios_etiquetados", nombre_archivo)

    if os.path.exists(destino):
        print(f"El archivo {nombre_archivo} ya existe. Saltando descarga.")
    else:
        response = requests.get(url)
        if response.status_code == 200:
            with open(destino, "wb") as f:
                f.write(response.content)
            print(f"Descargado correctamente: {nombre_archivo}")
        else:
            print(f"Error al descargar {nombre_archivo}: {response.text}")
            continue

    # Detectar formato
    formato_detectado = detectar_formato(destino)
    print(f"Formato de {nombre_archivo}: {formato_detectado}")

    detalle_formatos.append({
        "archivo": nombre_archivo,
        "formato_detectado": formato_detectado
    })

# Guardamos el detalle de formatos en CSV
pd.DataFrame(detalle_formatos).to_csv("audios_etiquetados/formato_audios.csv", index=False)
print("Descarga y detección de formatos finalizada.")
