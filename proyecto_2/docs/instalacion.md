# Instalación

## 1. Requisitos previos
- Docker instalado y corriendo.
- [Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli) instalada.
- Cuenta en Snowflake con un **Database** y un **Warehouse** creados.

## 2. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/football-leagues-etl.git
cd football-leagues-etl
```

## 3. Crear un proyecto Astro
Si aún no tenés un proyecto inicializado:
```bash
astro dev init
```
Esto creará la estructura de carpetas básica de Airflow para Astro CLI.

## 4. Copiar los DAGs y archivos al proyecto
- Mover el DAG (`demo_leagues.py`, `utils.py`) a la carpeta `dags/demo_leagues`.
- Mover los SQL a `dags/demo_leagues/queries` (o donde quieras).
- Dejar los datos (`df_ligas.csv`, etc.) en `include/data/`.

## 5. Levantar Airflow con Astro CLI
```bash
astro dev start
```
Esto levantará los servicios de Airflow (webserver, scheduler, etc.) en contenedores.

## 6. Acceder a la UI
Abrir en el navegador:
```
http://localhost:8080
```
Usuario: `admin`  
Contraseña: `admin`

## 7. Configurar conexión a Snowflake
En la UI de Airflow:
- **Conn Id**: `snowflake_conn`