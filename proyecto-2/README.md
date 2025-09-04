# ETL de Ligas de Fútbol con Airflow y Snowflake

Este proyecto implementa un pipeline de ingesta de datos de ligas de fútbol utilizando Apache Airflow para la orquestación y Snowflake como Data Warehouse.

---

## Tecnologias utilizadas
- **Python** (pandas, requests, lxml) → extracción y transformación de datos.

- **Apache Airflow** → orquestación y programación de tareas ETL.

- **Snowflake** → almacenamiento en Data Warehouse (Stage + Table).

- **Docker** → ejecución de Airflow en contenedores.

- **Astro CLI** → despliegue y gestión local de Airflow.

- **OpenPyXL** → manejo de archivos Excel (team_table).

---

## Estructura del proyecto
```
│── README.md                 # Descripción del proyecto 
│── .gitignore
│── requerimientos.txt        # Dependencias de Python     
│  
├── dags/                     # DAGs de Airflow  
│   ├── demo_leagues.py  
│   └── utils.py              # Funciones auxiliares para scraping y limpieza  
│  
├── data/                     # Archivos de datos de entrada  
│   ├── df_ligas.csv          # Ligas y URLs  
│   ├── team_table.xlsx       # Equipos e IDs únicos (si se requiere)  
│  
├── sql/                      # Queries SQL para Snowflake  
│   ├── upload_stage.sql  
│   ├── upload_table.sql  
│   └── snowflake_queries.sql  
│  
├── airflow/                  # Configuración específica de Airflow  
│   ├── setup_variables.json  # Variables de entorno de Airflow  
│   └── connections.md        # Guía para crear conexión con Snowflake  
│  
└── docs/                     # Documentación  
    ├── instalacion.md        # Instalación paso a paso  
    └── uso.md                # Cómo ejecutar el pipeline  
```
---
