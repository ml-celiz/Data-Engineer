import random
import pandas as pd
from tqdm import tqdm
from cred_here import *
import json
import requests
import ast

# Herramientas
import folium
from shapely.geometry import Polygon
import numpy as np
import geojson
import folium
import geopandas as gpd
from shapely.geometry import Polygon
import shapely.wkt
from haversine import haversine, Unit
import random
import time
from pyproj import Geod
#from polygon_geohasher.polygon_geohasher import geohash_to_polygon
from shapely import wkt
from geopandas import datasets, GeoDataFrame, read_file, points_from_xy
from geopandas.tools import overlay
from geopandas.tools import sjoin
from folium.plugins import MeasureControl
from folium.plugins import MarkerCluster
import time

# Funciones
# 1. Funcion que a partir de una direccion y la api obtengo las coordenadas de latitud y longitud
def GetLatLon2(Address, YOUR_API_KEY):
    url2_geocode  = f'https://geocode.search.hereapi.com/v1/geocode?q={Address}&apiKey='+YOUR_API_KEY
    try:
        response = requests.get(url2_geocode).json()
        CleanAddress = response['items'][0]['title'].upper()
        LAT = response['items'][0]['position']['lat']
        LON = response['items'][0]['position']['lng']
        results = [CleanAddress,round(LAT,7),round(LON,7)]
    except:
        results = ['NotFound','NA','NA']
    return results

# 2. Funcion para calcular la distancia
# punto inicial (geo_source), punto 2 (ubicaciones de c/u de las estaciones), unidad = km
def cal_dist(geo_source,point2,unit):
    if unit == 'Km':
        distance = haversine(geo_source, point2,Unit.KILOMETERS)
    elif unit == 'm':
        distance = haversine(geo_source, point2,Unit.METERS)
    elif unit == 'miles':
        distance = haversine(geo_source, point2,Unit.MILES)
    return distance # retorna la distancia en km

# 3. Funcion para calcular la distancia a las estaciones
# punto inicial (geo_source), dataframe (ciudad que nosotros especifiquemos), radio (filtro de estaciones que esten dentro de ese radio), unidad = km
def distance_estac(geo_source, df, radio, unit):
    distancia = [] # arreglo de distancia
    source = [] # arreglo del punto 2
    for i in tqdm(range(len(df)),colour = 'green'): # recorremos el df de la ciudad
        distancia.append(cal_dist(geo_source,df['POINT'][i],unit)) # calculamos la distancia
        source.append(geo_source) # capturar la locacion central para c/ registro
    # dataset
    new_df = df.copy()
    new_df['SOURCE'] = source # columna 1 le asigno la fuente
    new_df['DISTANCE'] = distancia # columna 2 le asigno la distancia
    new_df = new_df[new_df['DISTANCE']<=radio] # filtro solo por las que sean menores del radio
    new_df = new_df.reset_index()
    new_df = new_df.drop(columns ='index')
    return new_df.sort_values(by='DISTANCE',ascending=True)

# 4. Funcion que toma la latitud y longitud y crea una tupla
def transform_df_map(df_temp):
    coordenadas = []
    for i in range(len(df_temp)):
        try :
            coord = float(df_temp['LAT'][i]),float(df_temp['LNG'][i]) # captura la long y la lat y forma una tupla
            coordenadas.append(coord)
        except :
            coordenadas.append('EMPTY')
    df_temp['POINT'] = coordenadas # creo una columna y le asigno la tupla
    df_temp = df_temp[df_temp['POINT']!='EMPTY']
    df_temp = df_temp.reset_index()
    df_temp = df_temp.drop(columns = 'index')
    new_df = df_temp.copy()
    return new_df

# 5. Funcion que con el precio del combustible me va a pintar de verde el icono, y si es el precio maximo lo pinta de rojo, y si no es ninguno de los dos lo pinta de naranja
# dataframe filtrado por el tipo de combustible (gdf_results_2), el mapa (m), la unidad (Km), el producto (oil) y el icono
def marker_rest(df,mapa,unit,oil,icono):
    # dataframe
    df = df[df['Producto']==oil]
    df = df.reset_index()
    df = df.drop(columns = 'index')
    for i in range(len(df)): # registro x registro
        if df['Precio'][i]==df['Precio'].min(): # si el preciop es minimo ...
            html =  f"""<b>MARCA:</b> {df.Bandera[i]} <br>
                    <b>NAME:</b> {df.Nombre_comercial[i]} <br>
                    <b>PRODUCTO:</b> {df.Producto[i]} <br>
                    <b>PRECIO:</b> {df.Precio[i]} <br>
                    <b>DISTANCE:</b> {round(df.DISTANCE[i],2)}<br>
                    <b>DIRECCION:</b> {df.Direccion[i]}<br> 
                    <b>UNIT:</b> {unit}<br>""" # etiqueta
            iframe = folium.IFrame(html,figsize=(6, 3)) # frame
            popup = folium.Popup(iframe)
            folium.Marker(location=[float(df['LAT'][i]),float(df['LNG'][i])],
                               icon=folium.Icon(color='darkgreen', icon_color='white', # color verde
                               icon=icono, prefix='glyphicon'),
                               popup = popup).add_to(mapa)

        elif df['Precio'][i]==df['Precio'].max(): # si el precio es maximo...
            html =  f"""<b>MARCA:</b> {df.Bandera[i]} <br>
                    <b>NAME:</b> {df.Nombre_comercial[i]} <br>
                    <b>PRODUCTO:</b> {df.Producto[i]} <br>
                    <b>PRECIO:</b> {df.Precio[i]} <br>
                    <b>DISTANCE:</b> {round(df.DISTANCE[i],2)}<br>
                    <b>DIRECCION:</b> {df.Direccion[i]}<br>
                    <b>UNIT:</b> {unit}<br>"""  # etiqueta
            iframe = folium.IFrame(html,figsize=(6, 3)) # frame
            popup = folium.Popup(iframe)
            folium.Marker(location=[float(df['LAT'][i]),float(df['LNG'][i])],
                               icon=folium.Icon(color='darkred', icon_color='white', # color rojo
                               icon=icono, prefix='glyphicon'),
                               popup =popup).add_to(mapa)

        else: # si el precio no es ni el minimo ni el maximo...
            html =  f"""<b>MARCA:</b> {df.Bandera[i]} <br>
                    <b>NAME:</b> {df.Nombre_comercial[i]} <br>
                    <b>PRODUCTO:</b> {df.Producto[i]} <br>
                    <b>PRECIO:</b> {df.Precio[i]} <br>
                    <b>DISTANCE:</b> {round(df.DISTANCE[i],2)}<br>
                    <b>DIRECCION:</b> {df.Direccion[i]}<br> 
                    <b>UNIT:</b> {unit}<br>""" # etiqueta
            iframe = folium.IFrame(html,figsize=(6, 3)) # frame
            popup = folium.Popup(iframe)
            folium.Marker(location=[float(df['LAT'][i]),float(df['LNG'][i])],
                               icon=folium.Icon(color='orange', icon_color='white', # color naranja
                               icon=icono, prefix='glyphicon'),
                               popup =popup).add_to(mapa) # <font-awesome-icon icon="fa-regular fa-gas-pump"/>

    return