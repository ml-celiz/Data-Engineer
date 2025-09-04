# Instalación

1. Actualizar paquetes del sistema:
   ```bash
   sudo apt update && sudo apt upgrade

2. Instalar Python y pip:
    ```bash
    sudo apt install -y python3-pip

3. Clonar el repositorio en la instancia:
    ```bash
    git clone https://github.com/ml-celiz/Data-Engineer.git
    cd Data-Engineer

4. Instalar dependencias desde requerimientos.txt:
    ```bash
    pip3 install -r requirimientos.txt

5. Configurar las variables de entorno en el servidor:
    ```bash
   1. Crear cuenta en Twilio para obtener:

    TWILIO_SID  
    TWILIO_TOKEN  

   2. Crear cuenta en Weather API para obtener:

    WEATHER_API_KEY  

   3. Definir variables de entorno:

    export TWILIO_SID="tu_sid"  
    export TWILIO_TOKEN="tu_token"  
    export WEATHER_API_KEY="tu_api_key"  
    export PHONE_NUMBER="+549XXXXXXXXX" 

6. Automatización con cron   
   Configurar un cron job para ejecutar el script en un horario determinado, por ejemplo todos los días a las 9:00 AM:
    ```bash
    crontab -e
    0 9 * * * /usr/bin/python3 /home/ubuntu/Data-Engineer/proyecto-1/src/programa_principal.py
