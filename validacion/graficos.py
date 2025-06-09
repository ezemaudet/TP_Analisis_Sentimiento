import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Leer el archivo consolidado con las métricas
metricas_path = "transcripciones/evaluacion_metricas.csv"
metricas_df = pd.read_csv(metricas_path)

# Agrupamos por modelo y calculamos el promedio de cada métrica
resumen = metricas_df.groupby("modelo").agg({
    "levenshtein": "mean",
    "wer": "mean",
    "cer": "mean",
    "tiempo": "mean"
}).reset_index()

# Mostramos la tabla resumen
print("\nResumen de resultados:")
print(resumen)


# Creamos el gráfico de barras para las distancias
fig, ax1 = plt.subplots(figsize=(10,6))

bar_width = 0.2
x = np.arange(len(resumen["modelo"]))

ax1.bar(x - bar_width, resumen["levenshtein"], width=bar_width, label="Levenshtein")
ax1.bar(x, resumen["wer"], width=bar_width, label="WER")
ax1.bar(x + bar_width, resumen["cer"], width=bar_width, label="CER")

ax1.set_xlabel("Modelo")
ax1.set_ylabel("Distancia promedio")
ax1.set_title("Comparación de distancia por modelo")
ax1.set_xticks(x)
ax1.set_xticklabels(resumen["modelo"])
ax1.legend()
plt.tight_layout()
plt.savefig("transcripciones/distancia_por_modelo.png")
plt.close()

# Creamos el gráfico de barras para los tiempos
plt.figure(figsize=(8,5))
plt.bar(resumen["modelo"], resumen["tiempo"], color="skyblue")
plt.xlabel("Modelo")
plt.ylabel("Tiempo promedio (s)")
plt.title("Tiempo promedio de transcripción por modelo")
plt.tight_layout()
plt.savefig("transcripciones/tiempo_por_modelo.png")
plt.close()

print("Gráficos generados y guardados correctamente.")
