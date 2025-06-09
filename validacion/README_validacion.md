# Proyecto de Validación de Modelos de Transcripción

Este proyecto implementa un pipeline completo para validar modelos de transcripción de audio utilizando Whisper y analizar el rendimiento de distintas versiones (`base`, `small`, `medium`, `large`) comparado contra transcripciones reales.

---

## 🔧 Descripción general del pipeline

El flujo completo consta de 4 etapas principales:

1️⃣ **Descarga de audios**
- Archivo: `descargar.py`
- Descarga grabaciones desde la API de Vozelia.
- Verifica el formato de cada archivo usando `ffprobe` y guarda los audios en `audios_etiquetados/`.
- Registra los formatos detectados en `formato_audios.csv`.

2️⃣ **Transcripción de audios**
- Archivo: `transcribir.py`
- Lee los audios descargados.
- Transcribe cada archivo utilizando los modelos de Whisper: `base`, `small`, `medium`, `large`.
- Guarda las transcripciones individuales y registra el tiempo de procesamiento.
- Exporta `transcripciones_tiempos.csv`.

3️⃣ **Cálculo de métricas de distancia**
- Archivo: `distancia.py`
- Compara las transcripciones de los modelos contra las transcripciones reales (`true_transcripciones.csv`).
- Calcula:
  - Distancia Levenshtein
  - Word Error Rate (WER)
  - Character Error Rate (CER)
- Exporta el archivo `evaluacion_metricas.csv` con los resultados completos.

4️⃣ **Generación de gráficos**
- Archivo: `graficos.py`
- Calcula promedios por modelo.
- Genera los gráficos:
  - `distancia_por_modelo.png` (errores)
  - `tiempo_por_modelo.png` (tiempo de ejecución)
- Los gráficos se guardan automáticamente en `transcripciones/graficos/`.

---

## 🖥 Requisitos de instalación

```bash
python>=3.10
pandas
numpy
matplotlib
python-Levenshtein
jiwer
whisper
ffmpeg (instalado en el sistema)
