import requests
import random
import pandas as pd
from tqdm import tqdm
from bs4  import BeautifulSoup
from credencial_template import YOUR_API_KEY
import json
import time
import ast

# Credencial
YOUR_API_KEY = YOUR_API_KEY

# 1. LIMPIEZA Y TRANSFORMACION
df = pd.read_csv('precios_de_combustibles.csv')
#print(df.head())

# Obtener periodo mas reciente
#print(df.Periodo.unique()) # 2022
#print(df[df['Periodo']==2022])

# Obtener mes mas reciente
#print(df[df['Periodo']==2022]['Mes'].max()) # mes 6 = junio
df2 = df[(df['Periodo']==2022) & (df['Mes']==6)] # periodo 2022 y mes 6
#print(df2)

# Delimitar a determinados departamentos y determinadas ciudades
df3 = df2[(df2['Departamento']=='BOGOTA D.C.') | ((df2['Departamento']=='ANTIOQUIA') & ((df2['Municipio']=='MEDELLIN') | (df2['Municipio']=='ITAGUI') | (df2['Municipio']=='BELLO') | (df2['Municipio']=='SABANETA') | (df2['Municipio']=='RIONEGRO') | (df2['Municipio']=='ENVIGADO')))] # departamento bogota y antioquia, primeras 7 ciudades
df3.reset_index(inplace = True)
df3.drop(columns = 'index', inplace = True)
#print(df3)

# Transformamos la columna direccion
df3['Dir2'] = df3['Direccion'].apply(lambda x : x.replace('#', 'No'))
df3['Full_Address'] = df3.apply(lambda x : x['Direccion'] + ', ' + x['Municipio'].capitalize() + ', Colombia', axis = 1)
#print(df3)

# Cuantas direcciones deseados geocodificar
#print(df3['Full_Address'].nunique())

# Dataframe con las estaciones seleccionadas
# filtramos por nombre_comercial, direccion y full_address
# borramos duplicados
estaciones = df3[['Nombre_comercial', 'Direccion', 'Full_Address']].drop_duplicates(subset = 'Nombre_comercial')
estaciones.reset_index(inplace = True)
estaciones.drop(columns = 'index', inplace = True)
#print(estaciones)

# 2. GEOCODING
# Primer registro
#print(estaciones['Full_Address'][0])

address = estaciones['Full_Address'][0] # direccion del primer registro para probar

# Funcion que devuelve las coordenadas segun tu direccion y tu api
def get_coords(address, YOUR_API_KEY):
    url = f'https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={YOUR_API_KEY}' # url
    # excepcion: nuestra direccion puede traer caracteres especiales que den error
    try:
        response = requests.get(url).json() # peticion
        # informacion de interes del json
        CleanAddress = response['items'][0]['title'].upper()
        LAT = response['items'][0]['position']['lat']
        LNG = response['items'][0]['position']['lng']
        results = [CleanAddress, LAT, LNG] # arreglo con toda la inf
    except:
        results = ['Not Found', 'NA', 'NA']
    return results

#print(get_coords(adress, YOUR_API_KEY)

# Extraccion de coordenadas para todo el dataset
coordenadas = []
tiempo = [1, 2, 2.5] # scrapping para no sobrecargar los servidores

for i in tqdm(range(len(estaciones['Full_Address'])), colour='green'):
    try:
        R = get_coords(estaciones['Full_Address'][i], YOUR_API_KEY) # direccion del registro i
        geo_source = R[1], R[2]
        coordenadas.append(geo_source)
    except:
        coordenadas.append('Error')
    time.sleep(random.choices(tiempo)[0])

#print(coordenadas)

# Dataframe final
# merge entre el dataframe original (df3) y el de estaciones
df_final = pd.merge(df3,estaciones[['Full_Address','Coords']],how = 'inner' , on = 'Full_Address')
#print(df_final)

df_final.to_csv('DATASET_FINAL.csv', index = False)