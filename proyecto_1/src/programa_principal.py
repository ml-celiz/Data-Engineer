# Librerias
import os
from twilio.rest import Client
from twilio_config import *
import time

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from datetime import datetime

from deep_translator import GoogleTranslator

# Creacion de la url
query = 'Argentina'
api_key = API_KEY_WAPI
url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

# Peticion a la url
# Conversion a un archivo json
response = requests.get(url_clima).json()

# Creacion del Dataframe
# Funcion para extraer cada uno de los campos de interes de los registros de cada hora
def obtener_pronostico(response, i):
    # Datos de interes
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0] # Fecha
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0]) # Hora
    condicion_climatica = GoogleTranslator(source='en', target='es').translate(response['forecast']['forecastday'][0]['hour'][i]['condition']['text']) # Condicion climatica traducida
    temperatura = response['forecast']['forecastday'][0]['hour'][i]['temp_c'] # Temperatura en °C
    lluvia = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain'] # ¿Lloverá o no llovera? 1 - SI, 0 - NO
    probabilidad_lluvia = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain'] # Probabilidad de lluvia

    return fecha, hora, condicion_climatica, temperatura, lluvia, probabilidad_lluvia

# Array para alojar todos los datos necesarios
datos = []
# Itera 24 veces porque hay 24 registros en 24 horas (calculados con len)
for i in tqdm(range(len(response['forecast']['forecastday'][0]['hour'])), colour='green'):
    datos.append(obtener_pronostico(response, i))

# Columnas
col = ['Fecha', 'Hora', 'Condicion climática', 'Temperatura', 'Lluvia', 'Probabilidad lluvia']

# Dataframe
df = pd.DataFrame(datos, columns=col)
#print(df)

# Reduccion del Dataframe
# ¿En que horario me interesa saber si va a llover o no? (6 am a 22 pm)
df_reducido = df[(df['Lluvia']==1) & (df['Hora']>6) & (df['Hora']<22)]
df_reducido = df_reducido[['Hora', 'Condicion climática']]
df_reducido.set_index('Hora', inplace=True)
#print(df_reducido)

# Mensaje SMS desde Twilio
time.sleep(2)
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)
message = client.messages.create(
    body = '\nHola! \n\n\n El pronostico de lluvia hoy '+ df['Fecha'][0] +' en ' + query +' es : \n\n\n ' + str(df_reducido),
    from_ = PHONE_NUMBER,
    to = '+549XXXXXXXXX'
    )

print('Mensaje enviado ' + message.sid) # Hash de que mi mensaje fue enviado
