Proyecto de Validación de Modelos de Transcripción
Este proyecto implementa un pipeline completo para validar modelos de transcripción de audio utilizando Whisper y analizar el rendimiento de distintas versiones (base, small, medium, large) comparado contra transcripciones reales.

🔧 Descripción general del pipeline
El flujo completo consta de 5 etapas principales:

1️⃣ Descarga de audios

Archivo: descargar.py

Descarga grabaciones desde la API de Vozelia.

Verifica el formato de cada archivo usando ffprobe y guarda los audios en audios_etiquetados/.

Registra los formatos detectados en formato_audios.csv.

2️⃣ Transcripción de audios

Archivo: transcribir.py

Lee los audios descargados.

Transcribe cada archivo utilizando los modelos de Whisper: base, small, medium, large.

Guarda las transcripciones individuales y registra el tiempo de procesamiento.

Exporta transcripciones_tiempos.csv.

3️⃣ Cálculo de métricas de distancia

Archivo: distancia.py

Compara las transcripciones de los modelos contra las transcripciones reales (true_transcripciones.csv).

Calcula:

Distancia Levenshtein

Word Error Rate (WER)

Character Error Rate (CER)

Exporta el archivo evaluacion_metricas.csv con los resultados completos.

4️⃣ Generación de gráficos

Archivo: graficos.py

Calcula promedios de las distancias NORMALIZADAS por modelo y de los tiempos de ejecución.

Genera los gráficos:

distancia_por_modelo.png (errores)

tiempo_por_modelo.png (tiempo de ejecución)

Los gráficos se guardan automáticamente en transcripciones/.

Se guarda una tabla resumen de los resultados.

5️⃣ Análisis de duración promedio y frecuencia diaria de llamadas

Archivo: llamadas_dia.py o ejecutar_validacion.sh

Descarga automáticamente los registros CDR desde la API de Vozelia usando credenciales definidas en variables de entorno (.env).

Procesa el CSV de llamadas con pandas.

Calcula:

Duración total de llamadas por día (en minutos).

Cantidad total de llamadas por día.

Duración promedio por llamada diaria.

Genera y guarda en la carpeta resultados_llamadas/:

duracion_diaria.csv (duración total por día)

cantidad_llamadas_diaria.csv (cantidad de llamadas por día)

duracion_diaria_llamadas.png (gráfico de duración diaria)

cantidad_llamadas_diaria.png (gráfico de frecuencia diaria)

🖥 Requisitos de instalación
bash
Copiar
Editar
python>=3.10
pandas
numpy
matplotlib
python-Levenshtein
jiwer
whisper
ffmpeg (instalado en el sistema)
python-dotenv
requests
