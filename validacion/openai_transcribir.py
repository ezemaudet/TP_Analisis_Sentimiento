# 🔧 Instalar si estás en Colab (si no lo tenés)
# !pip install openai pandas python-dotenv

import os
import openai
import pandas as pd
import time
from dotenv import load_dotenv

# --- CARGAR VARIABLE DE ENTORNO ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key or not openai.api_key.startswith("sk-"):
    raise ValueError("❌ Clave API de OpenAI no válida. Asegurate de definir OPENAI_API_KEY en tu entorno.")

# --- CONFIGURACIÓN DE DIRECTORIOS ---
os.makedirs("transcripciones", exist_ok=True)
os.makedirs("audios_etiquetados", exist_ok=True)

# --- DETECTAR TODOS LOS .wav ---
archivos_audio = [f for f in os.listdir("audios_etiquetados") if f.endswith(".wav")]

# --- CARGAR RESULTADOS ANTERIORES (si existen) ---
ruta_resultados = "transcripciones/transcripciones_tiempos.csv"
if os.path.exists(ruta_resultados):
    df_previos = pd.read_csv(ruta_resultados)
else:
    df_previos = pd.DataFrame(columns=["grabacion", "modelo", "transcripcion", "tiempo_procesamiento_seg"])

# --- NUEVOS RESULTADOS CON OPENAI API ---
nuevos_resultados = []

for archivo_audio in archivos_audio:
    ruta_audio = os.path.join("audios_etiquetados", archivo_audio)
    nombre_base = archivo_audio.replace(".wav", "")

    # Saltar si ya existe resultado para este modelo
    if ((df_previos["grabacion"] == nombre_base) & (df_previos["modelo"] == "openai_whisper_api")).any():
        print(f"⏩ Ya existe transcripción para {nombre_base} con OpenAI API. Se omite.")
        continue

    print(f"☁️ Procesando {archivo_audio} con OpenAI Whisper API...")

    try:
        inicio = time.time()

        with open(ruta_audio, "rb") as audio_file:
            response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="es"
            )

        fin = time.time()
        duracion = fin - inicio
        texto = response.text

        nuevos_resultados.append({
            "grabacion": nombre_base,
            "modelo": "openai_whisper_api",
            "transcripcion": texto,
            "tiempo_procesamiento_seg": duracion
        })

    except Exception as e:
        print(f"⚠️ Error al procesar {archivo_audio}: {e}")

# --- GUARDAR COMBINADO ---
df_nuevos = pd.DataFrame(nuevos_resultados)
df_final = pd.concat([df_previos, df_nuevos], ignore_index=True)
df_final.to_csv(ruta_resultados, index=False)
print("✅ Transcripción con OpenAI completada y agregada al archivo existente.")
