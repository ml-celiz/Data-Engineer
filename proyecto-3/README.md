# Sistema para extraer estadísticas diarias de YouTube

Este proyecto implementa un flujo automatizado en AWS para recolectar estadísticas de canales de YouTube y analizarlas con Amazon Athena.

---

## Tecnologías utilizadas

- **AWS Lambda** → automatización del script de extracción.
- **Amazon S3** → almacenamiento de los datos (input y output).
- **Amazon Athena** → consultas e insights sobre las estadísticas recolectadas.
- **Google YouTube Data API v3** → fuente de los datos.
- **Amazon EventBridge (cron)** → disparador para ejecución diaria.

---

## Estructura del proyecto
```
proyecto-3
│── data/
│   ├── channels_to_analize.csv                # Lista de canales a analizar
│   ├── YOUTUBE_FILES_CHANNEL_15_DIAS.rar      # Muestra de 15 dias de estadisticas
│
│── lambda/
│   ├── lambda_demo.py                         # Script principal para AWS Lambda
│   ├── credencial_template.py                       # Plantilla con la API_KEY (no subir credenciales reales)
│
│── athena/
│   ├── queries_athena.txt                     # Consultas SQL para obtener insights
│
│── README.md                                  # Documentacion
│── requirements.txt                           
│── .gitignore                                 
```
---

## 🔑 Variables de entorno (AWS Lambda)

Configurar en la función Lambda:

- `BUCKET` → nombre del bucket de entrada (ejemplo: `demo_input_youtube`)
- `BUCKET_DESTINY` → nombre del bucket de salida (ejemplo: `demo_output_youtube`)
- `APIKEY` → API Key de Google Console
- `FILE_CHANNELS` → archivo CSV con los canales (`channels_to_analize.csv`)

---

## Flujo del sistema

1. **Google Console** → Obtener la `API_KEY` de YouTube Data API v3.  
2. **Carga inicial en S3** → Subir `channels_to_analize.csv` al bucket de entrada (`demo_input_youtube`).  
3. **AWS Lambda** → Ejecuta `lambda_demo.py`, extrae estadísticas y guarda resultados diarios en `demo_output_youtube`.  
4. **AWS EventBridge** → Configurar un evento CRON diario para automatizar la ejecución.  
5. **Amazon Athena** →  
   - Crear catálogo.  
   - Crear crawler `youtube_demo` apuntando al bucket `demo_output_youtube`.  
   - Guardar en base de datos `channel_stats`.  
   - Ejecutar queries de `athena/queries_athena.txt` para obtener insights.

---

## Consultas SQL en Athena

📄 Archivo: `athena/queries_athena.txt`

- **Query 1**: estadísticas completas por canal.  
- **Query 2**: crecimiento de un canal/categoría.  
- **Query Final**: optimización de crecimiento (suscriptores, videos, views).  

---

## Cómo ejecutar localmente

```bash
# Clonar repositorio
git clone https://github.com/usuario/youtube-stats-project.git
cd youtube-stats-project

# Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---
