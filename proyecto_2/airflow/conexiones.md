# Conexión de Airflow con Snowflake

Para la interaccion entre Airflow con Snowflake.

## 1. Acceder a la interfaz de Airflow
Abrir en el navegador:
```
http://localhost:8080
```

## 2. Crear una nueva conexión
1. Ir a **Admin > Connections**.
2. Hacer clic en **+** para agregar una nueva conexión.
3. Completar los datos:

- **Conn Id**: `snowflake_conn`  
- **Conn Type**: `Snowflake`  
- **Host**: `xyz12345.snowflakecomputing.com` *(reemplazar por tu cuenta)*  
- **Login**: `USUARIO_SNOWFLAKE`  
- **Password**: `CONTRASEÑA_SNOWFLAKE`  
- **Schema**: `PUBLIC`  
- **Database**: `LEAGUES`  
- **Warehouse**: `NORMAL_WH`  
- **Role**: `ACCOUNTADMIN`  

## 3. Guardar y probar conexión
Hacer clic en **Save** y luego en **Test** para verificar que Airflow pueda conectarse correctamente.