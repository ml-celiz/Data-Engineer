# App de Estación de Servicio Cercana

Aplicación desarrollada en **Python + Streamlit** que permite identificar las estaciones de servicio más económicas y más costosas dentro de un radio de **1 km por ciudad**, filtrando además por tipo de combustible.  

Los resultados se muestran en un **mapa interactivo con Folium**, destacando con colores las estaciones según el precio del combustible seleccionado.

---

## Tecnologías utilizadas

- **Python 3.13**
- **Streamlit** (interfaz de la app)
- **Folium** (mapas interactivos)
- **GeoPandas / Shapely / GeoJSON** (procesamiento geoespacial)
- **Haversine** (cálculo de distancias)
- **Here Platform API** (geolocalización con `YOUR_API_KEY`)
- **Docker** (contenedorización de la aplicación)

---

## Estructura del proyecto

```
proyecto_4/
│── app/
│   ├── 1_Fuel-prices.jpg          # Imagen de portada (sidebar de la app)
│   ├── app.py                     # Código principal de la aplicación en Streamlit
│   ├── credencial_template.py     # Plantilla de credencial con tu API Key
│   ├── DF_STATIONS.csv            # Dataset procesado de estaciones
│   ├── Dockerfile                 # Archivo de dockerización
│   ├── profile.jpg                # Imagen de perfil para la sección "Sobre mí"
│   ├── requirements.txt           # Dependencias necesarias
│   └── utils.py                   # Funciones auxiliares para mapas y cálculos
│
│── obtencion_df/
│   └── script_obtencion_df.py     # Script para obtención y limpieza del dataset
│
└── docs/
    └── Explicacion.md             # Explicación completa del sistema
```

---

## Cómo correr la aplicación

### Opción 1: Local
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/usuario/proyecto_4.git
   cd proyecto_4/app
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar tu **API Key de Here Platform** en `credencial_template.py`:
   ```python
   YOUR_API_KEY = "TU_API_KEY_AQUI"
   ```
4. Ejecutar la app:
   ```bash
   streamlit run app.py
   ```

### Opción 2: Docker
1. Construir la imagen:
   ```bash
   docker build -t nearby-oil-app .
   ```
2. Correr el contenedor:
   ```bash
   docker run -p 8501:8501 nearby-oil-app
   ```
3. Abrir en el navegador 👉 `http://localhost:8501`

