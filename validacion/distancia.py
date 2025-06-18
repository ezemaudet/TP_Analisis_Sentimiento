import os
import pandas as pd
import numpy as np
import Levenshtein
import jiwer

# Leer las transcripciones reales (true) y las generadas por los modelos
true_path = "true_transcripciones.csv"
resultados_path = "transcripciones/transcripciones_tiempos.csv"

# Cargamos las transcripciones verdaderas
true_df = pd.read_csv(true_path)
resultados_df = pd.read_csv(resultados_path)

# Renombramos la columna transcripcion del true para diferenciarla
true_df = true_df.rename(columns={"transcripcion": "transcripcion_true"})

# Hacemos el merge sobre grabacion (única clave común)
merged_df = pd.merge(resultados_df, true_df[["grabacion", "transcripcion_true"]], on="grabacion")

# Inicializamos columnas de métricas
merged_df["levenshtein"] = np.nan
merged_df["wer"] = np.nan
merged_df["cer"] = np.nan

# Funciones auxiliares

def calcular_levenshtein(true_text, pred_text):
    try:
        return Levenshtein.distance(str(true_text), str(pred_text))
    except:
        return np.nan

def calcular_wer(true_text, pred_text):
    try:
        return jiwer.wer(str(true_text), str(pred_text))
    except:
        return np.nan

def calcular_cer(true_text, pred_text):
    try:
        return jiwer.cer(str(true_text), str(pred_text))
    except:
        return np.nan

# Aplicamos las métricas
merged_df["levenshtein"] = merged_df.apply(lambda row: calcular_levenshtein(row["transcripcion_true"], row["transcripcion"]), axis=1)
merged_df["wer"] = merged_df.apply(lambda row: calcular_wer(row["transcripcion_true"], row["transcripcion"]), axis=1)
merged_df["cer"] = merged_df.apply(lambda row: calcular_cer(row["transcripcion_true"], row["transcripcion"]), axis=1)

# Guardamos el resultado final
merged_df.to_csv("transcripciones/evaluacion_metricas.csv", index=False)
print("Evaluación de métricas completada y guardada.")
