import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
import requests

# Cargamos variables de entorno
load_dotenv()
API_KEY = os.getenv("API_KEY_vozelia")
TENANT = os.getenv("TENANT_vozelia")
START_DATE = "2025-1-01"
END_DATE = "2025-01-31"


# URL para obtener los registros de llamadas en CSV
url = f"https://pbxone.vozelia.com.pa/pbx/proxyapi.php?key={API_KEY}&reqtype=INFO&info=CDRS&format=csv&tenant={TENANT}&start={START_DATE}&end={END_DATE}"

response = requests.get(url)

if response.status_code == 200:
    with open("llamadas.csv", "wb") as f:
        f.write(response.content)

    print("CDR descargado exitosamente.")

    # Cargar CSV en pandas para visualizar datos
    df = pd.read_csv("llamadas.csv")
    print(df.head())  # Mostrar las primeras filas

else:
    print("Error al obtener las llamadas:", response.text)

# Crear carpeta de salida si no existe
os.makedirs("resultados_llamadas", exist_ok=True)

# Cargar el archivo si aún no está en df
# df = pd.read_csv("llamadas.csv")

# Convertir la columna 'start' a datetime
df["start"] = pd.to_datetime(df["start"], errors='coerce')

# Filtrar filas válidas (con duración y fecha no nula)
df_validas = df[(df["duration"].notna()) & (df["start"].notna())]

# Crear columna de fecha
df_validas["fecha"] = df_validas["start"].dt.date

# --- Tabla 1: Duración total de llamadas por día (en minutos) ---
resumen_duracion = df_validas.groupby("fecha")["duration"].sum().reset_index()
resumen_duracion["total_duracion_min"] = resumen_duracion["duration"] / 60
resumen_duracion = resumen_duracion[["fecha", "total_duracion_min"]]
resumen_duracion.columns = ["fecha", "total_duracion_min"]
resumen_duracion.to_csv("resultados_llamadas/duracion_diaria.csv", index=False)

# --- Tabla 2: Cantidad de llamadas por día ---
resumen_cantidad = df_validas.groupby("fecha")["ID"].count().reset_index()
resumen_cantidad.columns = ["fecha", "cantidad_llamadas"]
resumen_cantidad.to_csv("resultados_llamadas/cantidad_llamadas_diaria.csv", index=False)

# --- Gráfico 1: Duración total diaria (en minutos) ---
plt.figure(figsize=(12, 6))
#plt.plot(resumen_duracion["fecha"], resumen_duracion["total_duracion_min"], marker="o")
plt.bar(resumen_duracion["fecha"], resumen_duracion["total_duracion_min"], color="skyblue", edgecolor="black")
plt.xticks(rotation=45)
plt.xlabel("Fecha")
plt.ylabel("Duración total (minutos)")
plt.title("Duración total diaria de llamadas (en minutos)")
plt.grid(True)
plt.tight_layout()
plt.savefig("resultados_llamadas/duracion_diaria_llamadas.png")
plt.close()

# --- Gráfico 2: Cantidad de llamadas diaria ---
plt.figure(figsize=(12, 6))
plt.bar(resumen_cantidad["fecha"], resumen_cantidad["cantidad_llamadas"], color="skyblue")
plt.xticks(rotation=45)
plt.xlabel("Fecha")
plt.ylabel("Cantidad de llamadas")
plt.title("Cantidad de llamadas por día")
plt.tight_layout()
plt.savefig("resultados_llamadas/cantidad_llamadas_diaria.png")
plt.close()

# Filtrar llamadas válidas (duración no nula y mayor que 10 seg y menor que 500 seg )
df_validas = df[df["duration"].notna() & (df["duration"] > 10) & (df["duration"] < 500)]

# Histograma de duración de llamadas
plt.figure(figsize=(10, 6))
plt.hist(df_validas["duration"], bins=30, color="steelblue", edgecolor="black")
plt.xlabel("Duración de llamada (segundos)")
plt.ylabel("Cantidad de llamadas")
plt.title("Distribución de duración de llamadas mayores a 10 Seg. y menores a 500 Seg.")
plt.tight_layout()
plt.savefig("resultados_llamadas/histograma_duracion_llamadas.png")
plt.show()

print("Tablas y gráficos guardados en carpeta 'resultados_llamadas'")
