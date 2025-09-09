import json
import pandas as pd
import time
import requests
import random
import time
import boto3
from datetime import datetime
import datetime
import os

s3_client = boto3.client('s3')

# Funcion para obtener estadisticas de un canal
def get_stats(api_key, channel_id):

    # Url de la API
    url_channel_stats = 'https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id=' + channel_id + '&key=' + api_key

    # Obtenemos informacion
    channel_stats = requests.get(url_channel_stats).json()

    # Limpieza y transformacion de los datos
    # Obtenemos seccion de estadisticas
    channel_stats = channel_stats['items'][0]['statistics']

    # Obtener fecha
    date = pd.to_datetime('today').strftime('%Y-%m-%d')

    # Diccionario
    data_channel = {
        'Created_at': date,
        'Total_views': int(float(channel_stats['viewCount'])),
        'Suscribers': int(float(channel_stats['subscriberCount'])),
        'Video_count': int(float(channel_stats['videoCount'])),
    }

    return data_channel

# Funcion para aplicar la funcion get_stats a cada uno de los canales del df_channels
def channel_stats(df, api_key):
    # arreglos
    date = []
    views = []
    suscriber = []
    video_count = []
    channel_name = []

    tiempo = [1, 2.5, 3, 2] # scraping con un factor de tiempo

    # iteramos el df
    for i in tqdm(range(len(df)), colour='green'):
        # var temporal
        stats_temp = get_stats(DEVELOPER_KEY, df_channels['Channel_id'][i])

        # agregamos inf a arreglos
        date.append(stats_temp['Created_at'])
        views.append(stats_temp['Total_views'])
        suscriber.append(stats_temp['Suscribers'])
        video_count.append(stats_temp['Video_count'])
        channel_name.append(df['Channel_name'][i])

        time.sleep(random.choice(tiempo)) # cada vez que entra al loop espera x segundos definidos en la var "tiempo" para no colapsar el servidor

    # Dataframe final
    data = {
        'Channel_name': channel_name,
        'Suscribers': suscriber,
        'Video_Count': video_count,
        'Total_Views': views,
        'created_at': date,
    }

    df_channels_final = pd.DataFrame(data)

    return df_channels_final

# Funcion lambda que vamos a usar
def lambda_handler(event, context):

    # leemos variables de entorno de entrada
    bucket_name = os.environ['BUCKET']
    filename =  os.environ['FILE_CHANNELS']
    DEVELOPER_KEY = os.environ['APIKEY']
    
    # obtener el archivo de el bucket de input s3
    obj = s3_client.get_object(Bucket=bucket_name, Key= filename)
    df_channels = pd.read_csv(obj['Body']) # 'Body' es una palabra clave

    # obtenemos resultados
    results = channels_stats(df_channels, DEVELOPER_KEY) # llamamos funcion
    date = pd.to_datetime('today').strftime("%Y%m%d") # obtenemos fecha de hoy

    # guardamos el archivo
    results.to_csv(f'/tmp/youtube_stats_{date}.csv',index = False)
 
    # enviamos el archivo al bucket de output s3
    s3 = boto3.resource("s3")
    
    s3.Bucket(os.environ['BUCKET_DESTINY']).upload_file(f'/tmp/youtube_stats_{date}.csv', Key=f'youtube_stats_{date}.csv')
    os.remove(f'/tmp/youtube_stats_{date}.csv')

    return f'file youtube_stats_{date}.csv send succeded' # se retorno correctamente
