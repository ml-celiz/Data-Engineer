# Uso del Pipeline

## 1. Ejecutar Airflow
Levantar los servicios:
```bash
docker-compose up
```

## 2. Activar el DAG
1. Ingresar a la UI de Airflow en [http://localhost:8080](http://localhost:8080).
2. Habilitar el DAG `demo_leagues`.
3. Ejecutar el DAG manualmente o esperar a la programación automática.

## 3. Revisar los datos en Snowflake
Ejecutar en Snowflake:
```sql
SELECT *
FROM "LEAGUES"."PUBLIC"."FOOTBALL_LEAGUES";
```