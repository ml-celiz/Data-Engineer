import json
from datetime import datetime, timedelta
import os
import logging
import airflow
from airflow.models import Variable
from airflow import models
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
import snowflake.connector as sf
import pandas as pd
import time
import random
import os
from utils import get_data,data_processing
from datetime import datetime

# Argumentos por default
default_arguments = {   'owner': 'nombre_usuario_dag',
                        'email': 'email_dag',
                        'retries': 1, # Si falla, cuantas veces quiero que haga los intentos
                        'retry_delay': timedelta(minutes=5)}

# Declaracion del dag object
with DAG('FOOTBAL_LEAGUES', # Nombre
         default_args = default_arguments,
         description = 'Extrayendo datos de la liga de futbol' ,
         start_date = datetime(2025, 9, 3),
         schedule_interval = None,
         tags = ['tabla_espn'],
         catchup = False
         ) as dag :

        # Informacion sensible
         params_info = Variable.get("feature_info", deserialize_json=True) # Obtencion de la variable de entorno creada en Airflow
         df = pd.read_csv('/usr/local/airflow/df_ligas.csv')
         df_team = pd.read_csv('/usr/local/airflow/team_table.csv') # Para obtener el id del equipo

        # Recibe: ligas y url (df) + equipos con id unico (df_team)
         def extract_info(df ,df_team ,**kwargs):

            df_data = data_processing(df) # utils.py

            df_final = pd.merge(df_data,df_team, how='inner', on='EQUIPO')

            df_final = df_final[['ID_TEAM','EQUIPO', 'J', 'G', 'E', 'P', 'GF', 'GC', 'DIF', 'PTS', 'LIGA',
                'CREATED_AT']] # Data frame final

            df_final.to_csv('./premier_positions.csv',index=False) # Conversion a csv

        # Dependencia de tareas
         extract_data = PythonOperator(
             task_id = 'EXTRACT_FOTBALL_DATA',
             provide_context = True,
             python_callable = extract_info,
             op_kwargs = {"df":df,"df_team":df_team}
         )

         upload_stage = SnowflakeOperator(
             task_id = 'upload_data_stage',
             sql = './queries/upload_stage.sql',
             snowflake_conn_id='demo_conn',
             warehouse = params_info["DWH"],
             database = params_info["DB"],
             role = params_info["ROLE"],
             params = params_info
         )

         ingest_table = SnowflakeOperator(
             task_id = 'ingest_table',
             sql = './queries/upload_table.sql',
             snowflake_conn_id = 'demo_conn',
             warehouse = params_info["DWH"],
             database = params_info["DB"],
             role = params_info["ROLE"],
             params = params_info
         )

        # Dag: Ejecuta stract_data, luego upload_stage y por ultimo ingesta el csv a la tabla
         extract_data >>  upload_stage >> ingest_table