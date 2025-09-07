import streamlit as st
import pandas as pd
from PIL import Image
import time
import json
import random
from datetime import datetime
import datetime
import os
import numpy as np
import requests
from tqdm import tqdm
from cred_here import *
import ast

# Herramientas
import folium
from shapely.geometry import Polygon
import numpy as np
import geojson
import geopandas as gpd
from tqdm import tqdm
from shapely.geometry import Polygon
import shapely.wkt
from haversine import haversine, Unit
import random
import time
from pyproj import Geod
from shapely import wkt
from geopandas import datasets, GeoDataFrame, read_file, points_from_xy
from folium.plugins import MeasureControl
from folium.plugins import MarkerCluster

from credencial_template import YOUR_API_KEY
from utils import GetLatLon2,cal_dist,distance_estac,transform_df_map,marker_rest
from streamlit_folium import folium_static

image = Image.open('1_Fuel-prices.jpg') # abrimos imagen

# barra lateral
st.sidebar.image(image , caption="Nearby Oil App",width = 256) # agregamos imagen a la barra lateral
app_mode = st.sidebar.selectbox("Elegir App Modo", ["Correr App","Sobre mi"]) # agregamos un select box a la barra lateral

# menu
if app_mode == 'Correr App': # si selecciona run app

    st.title('App de Estación de Servicio Cercana') # titulo
    st.markdown('App Descripción') # descripcion

    df_map = pd.read_csv('DF_STATIONS.csv') # leemos dataframe

    cities =  list(df_map['Municipio'].unique()) # lista de ciudades

    # filtro ciudad
    c1, c2, c3, c4, c5 = st.columns((1, 6, 6, 6, 1)) # columnas

    choose_city =  c2.selectbox("Elegir ciudad", cities) # select box de ciudades # columna 2

    # central location
    central_location = c2.text_input('Central Location', 'CC Multiplaza , Bogotá')

    DEVELOPER_KEY = YOUR_API_KEY # api para geocodificacion

    if len(central_location) != 0 : # si central location no es =/ N/A

        R = GetLatLon2(central_location,YOUR_API_KEY) # a partir de una localizacion central obtenemos la latitud y longitud
        geo_source = R[1], R[2]

        unit = 'Km' # unidad
        rad = c4.slider('Radius', 1, 3, 1) # slider del radio

        df_city = df_map[df_map['Municipio'] == choose_city] # df con seleccion de ciudad
        df_city.reset_index(inplace = True)
        df_city.drop(columns = 'index',inplace = True)

        df_city =  transform_df_map(df_city) # añadimos columna point = tupla(latitud, longitud)

        results = distance_estac(geo_source, df_city, rad, unit) # calculo de distancia de mi central location a cada point
        results = results.reset_index()
        results = results.drop(columns = 'index')

        # filtro de productos
        products =  list(results['Producto'].unique()) # lista de productos

        gdf_stores_results = GeoDataFrame(results, geometry = points_from_xy(results.LNG, results.LAT)) # convertimos el df a un geodataframe

        choose_products =  c3.selectbox("Elegir combustible", products) # select box de producto # columna 3

        # mapa
        if c3.button('MOSTRAR MAPA'): # boton para ejecutar el mapa # columna 3

            gdf_stores_results2 = gdf_stores_results[gdf_stores_results['Producto'] == choose_products] # filtro del df de resultados por el producto que yo elegi
            gdf_stores_results2 = gdf_stores_results2.reset_index()
            gdf_stores_results2 = gdf_stores_results2.drop(columns = 'index')

            icono = "usd" # icono (no aparece otro icono c/ folium)

            m = folium.Map([geo_source[0],geo_source[1]], zoom_start=15) # mapa

            # graficar circulo
            folium.Circle(
                radius = int(rad)*1000,
                location = [geo_source[0], geo_source[1]],
                color = 'green',
                fill = 'red'
            ).add_to(m)

            # graficar centroide
            folium.Marker(
                location = [geo_source[0],geo_source[1]],
                icon = folium.Icon(color='black', icon_color='white',
                icon = "home", prefix='glyphicon'),
                popup = "<b>CENTROID</b>"
            ).add_to(m)

            marker_rest (gdf_stores_results2, m, unit, choose_products, icono) # graficamos todas las ubicaciones de las estaciones en el mapa

            # llamada para renderizar el mapa de Folium en Streamlit
            folium_static(m)

elif app_mode == "Sobre mi": # si selecciona about me

    st.title('App de Estación de Servicio Cercana')
    st.success("No dudes en contactarme acá 👇 ")

    col1, col2, col3, col4 = st.columns((2,1,2,1))

    col1.markdown('* [**LinkedIn**](https://www.linkedin.com/in/ml-celiz/)')
    col1.markdown('* [**GitHub**](https://github.com/ml-celiz)')
    image2 = Image.open('profile.jpg')
    col3.image(image2, width=230)