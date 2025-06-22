import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import subprocess

# Leer el archivo consolidado con las métricas
metricas_path = "transcripciones/evaluacion_metricas.csv"
metricas_df = pd.read_csv(metricas_path)

# Renombramos columna 'tiempo' si existe
if "tiempo" in metricas_df.columns:
    metricas_df = metricas_df.rename(columns={"tiempo": "tiempo_procesamiento_seg"})

# Calculo relacion entre tiempo de grabación y procesamiento

def duracion_audio_ffprobe(ruta):
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            ruta
        ]
        duracion = subprocess.check_output(cmd).decode().strip()
        return float(duracion)
    except:
        return None

# Agregamos tiempo de grabación y cociente procesamiento/grabación
tiempos_grabacion = []
for i, row in metricas_df.iterrows():
    ruta_wav = os.path.join("audios_etiquetados", f"{row['grabacion']}.wav")
    duracion_grab = duracion_audio_ffprobe(ruta_wav)
    tiempos_grabacion.append(duracion_grab)

metricas_df["tiempo_grabacion_seg"] = tiempos_grabacion
metricas_df["relacion_proc_vs_grab"] = metricas_df["tiempo_procesamiento_seg"] / metricas_df["tiempo_grabacion_seg"]

# Guardamos el archivo extendido con duración de grabación y relación
metricas_df.to_csv("transcripciones/evaluacion_metricas.csv", index=False)

# Agrupamos por modelo y calculamos el promedio de cada métrica
resumen = metricas_df.groupby("modelo").agg({
    "levenshtein": "mean",
    "wer": "mean",
    "cer": "mean",
    "tiempo_procesamiento_seg": "mean",
    "tiempo_grabacion_seg": "mean",
    "relacion_proc_vs_grab": "mean"
}).reset_index()

# Normalizamos Levenshtein
resumen["levenshtein_norm"] = resumen["levenshtein"] / resumen["levenshtein"].max()

# Reordenar modelos si es necesario
resumen = resumen.iloc[[0, 3, 2, 1]]

resumen = resumen[["modelo","levenshtein","wer","cer","levenshtein_norm","tiempo_procesamiento_seg","tiempo_grabacion_seg","relacion_proc_vs_grab"]]

# Exportamos el resumen normalizado a CSV
resumen.to_csv("transcripciones/resumen_normalizado.csv", index=False)

# Mostramos la tabla resumen
print("\nResumen de resultados (normalizado):")
print(resumen)

# Graficamos las distancias normalizadas
fig, ax1 = plt.subplots(figsize=(10, 6))

bar_width = 0.2
x = np.arange(len(resumen["modelo"]))

ax1.bar(x - bar_width, resumen["levenshtein_norm"], width=bar_width, label="Levenshtein (normalizado)")
ax1.bar(x, resumen["wer"], width=bar_width, label="WER")
ax1.bar(x + bar_width, resumen["cer"], width=bar_width, label="CER")

ax1.set_xlabel("Modelo")
ax1.set_ylabel("Distancia normalizado")
ax1.set_title("Comparación de distancias por modelo (normalizado)")
ax1.set_xticks(x)
ax1.set_xticklabels(resumen["modelo"])
ax1.legend()
plt.tight_layout()
plt.savefig("transcripciones/distancia_por_modelo.png")
plt.close()

# Graficamos los tiempos de procesamiento promedio
plt.figure(figsize=(8, 5))
plt.bar(resumen["modelo"], resumen["tiempo_procesamiento_seg"], color="skyblue")
plt.xlabel("Modelo")
plt.ylabel("Tiempo de procesamiento promedio (s)")
plt.title("Tiempo promedio de transcripción por modelo")
plt.tight_layout()
plt.savefig("transcripciones/tiempo_procesamiento_por_modelo.png")
plt.close()

# Graficamos los tiempos de grabación promedio
plt.figure(figsize=(8, 5))
plt.bar(resumen["modelo"], resumen["tiempo_grabacion_seg"], color="orange")
plt.xlabel("Modelo")
plt.ylabel("Tiempo de grabación promedio (s)")
plt.title("Tiempo promedio de grabación por modelo")
plt.tight_layout()
plt.savefig("transcripciones/tiempo_grabacion_por_modelo.png")
plt.close()

# Graficamos la relación procesamiento/grabación promedio
plt.figure(figsize=(8, 5))
plt.bar(resumen["modelo"], resumen["relacion_proc_vs_grab"], color="green")
plt.xlabel("Modelo")
plt.ylabel("Relación proc/grabación")
plt.title("Relación entre tiempo de procesamiento y duración de la grabación")
plt.tight_layout()
plt.savefig("transcripciones/relacion_proc_vs_grab.png")
plt.close()

print("Gráficos generados y resultados exportados correctamente.")
