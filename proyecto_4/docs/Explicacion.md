# Explicación del Sistema

La aplicación permite localizar las estaciones de servicio más económicas o más costosas en un radio configurable por el usuario, según la ciudad y el tipo de combustible.

---

## Obtención y procesamiento del dataset

1. **Fuente de datos**:  
   Se descarga desde [datos.gob.ar](https://datos.gob.ar/) el dataset `precios_combustibles_arg`.

2. **Script `script_obtencion_df.py`:**
   - Limpieza y filtrado por **período y mes más reciente**.
   - Filtrado adicional por **departamento** y **ciudades específicas** (ejemplo: Rosario en Santa Fe, o Bogotá / Medellín en Colombia según dataset).
   - Se crea la columna `Full_Address` (dirección + ciudad + país).
   - Con la **Here Platform API** se obtiene latitud y longitud para cada dirección (`Coords`).
   - Se reemplazan valores N/A por `EMPTY`.
   - Se exporta el dataset final (`DF_STATIONS.csv` o `DATASET_FINAL.csv`).

---

## Funciones principales (`utils.py`)

1. **GetLatLon2**: Obtiene coordenadas (lat, long) desde una dirección usando la API Key de Here.
2. **cal_dist**: Calcula la distancia entre dos puntos geográficos.
3. **distance_estac**: Calcula la distancia desde un punto central a todas las estaciones en un radio dado.
4. **transform_df_map**: Convierte coordenadas en tuplas `(lat, long)` para graficar.
5. **marker_rest**: Agrega marcadores en el mapa:
   - Verde → precio más bajo.
   - Rojo → precio más alto.
   - Naranja → resto de estaciones.

---

## Visualización con Folium y Streamlit

- El usuario selecciona:
  1. Ciudad.
  2. Dirección central.
  3. Radio de búsqueda (km).
  4. Tipo de combustible.

- El sistema:
  - Calcula distancias con `haversine`.
  - Filtra estaciones dentro del radio.
  - Dibuja un **mapa con Folium**:
    - Círculo de cobertura.
    - Marcador del centroide.
    - Estaciones coloreadas según precio.

- La app cuenta con una **sidebar** con dos opciones:
  - **Correr App**: ejecuta el flujo principal.
  - **Sobre mí**: muestra datos de contacto y redes sociales.

---

## Dockerización

Archivo `Dockerfile`:
- Basado en `python:3.13`.
- Configura Streamlit en modo headless.
- Expone el puerto **8501**.
- Instala dependencias desde `requirements.txt`.
- Ejecuta la app con:
  ```bash
  streamlit run app/app.py --server.port=8501
  ```

---

## Resumen

- **Entrada**: Dataset oficial de precios de combustibles.  
- **Proceso**: Limpieza → Geocodificación con Here API → Cálculo de distancias → Visualización en mapa.  
- **Salida**: Mapa interactivo con estaciones más baratas, más caras y rango intermedio.  
