import os
import whisper
import pandas as pd
import subprocess
import time

# Creamos carpetas si no existen
os.makedirs("transcripciones", exist_ok=True)
os.makedirs("audios_etiquetados", exist_ok=True)

# Leemos los audios descargados
archivos_audio = [f for f in os.listdir("audios_etiquetados") if f.endswith(".wav")]

# Cargamos el CSV de formatos detectados
formatos_df = pd.read_csv("audios_etiquetados/formato_audios.csv")

# Solo procesamos aquellos audios que son WAV PCM (formato compatible)
audios_validos = formatos_df[formatos_df["formato_detectado"].str.contains("wav|pcm|s16le", case=False, na=False)]

# Modelos de Whisper
modelos = ["base", "small", "medium" , "large"]
resultados = []

for modelo_usado in modelos:
    print(f"Cargando modelo {modelo_usado}...")
    model = whisper.load_model(modelo_usado)

    for _, row in audios_validos.iterrows():
        archivo_audio = row['archivo']
        ruta_audio = os.path.join("audios_etiquetados", archivo_audio)
        print (archivo_audio)

        try:
            inicio = time.time()
            result = model.transcribe(ruta_audio, language="es")
            fin = time.time()

            transcripcion = result["text"]
            duracion = fin - inicio

            nombre_base = archivo_audio.replace(".wav", "")
            nombre_txt = f"{nombre_base}_{modelo_usado}.txt"
            ruta_txt = os.path.join("audios_etiquetados", nombre_txt)
            print (nombre_txt)

            with open(ruta_txt, "w", encoding="utf-8") as f:
                f.write(transcripcion)

            resultados.append({
                "grabacion": nombre_base,
                "modelo": modelo_usado,
                "transcripcion": transcripcion,
                "tiempo": duracion
            })

        except Exception as e:
            print(f"Error al transcribir {archivo_audio} con {modelo_usado}: {e}")

# Guardamos resultados en CSV
df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv("transcripciones/transcripciones_tiempos.csv", index=False)
print("Proceso de transcripción completado.")
