# Notificador SMS del tiempo

Automatización de alertas meteorológicas vía SMS utilizando **Twilio**, **Weather API**, **AWS EC2** y **Python**.  
El sistema obtiene el pronóstico del clima de una ciudad determinada y lo envía automáticamente (Con una instancia de AWS EC2) a un número de celular en un horario programado.  

---

## Tecnologías utilizadas
- **Python** → automatización y lógica del sistema.  
- **Weather API** → obtención de datos meteorológicos en formato JSON.  
- **Twilio** → compra de número y envío de SMS.  
- **AWS EC2** → ejecución del script en la nube con tareas programadas (cron).  

---

## Estructura del proyecto
```
├── docs/                       # Documentación, diagramas, imágenes 
│ └── ejemplo_mensaje.jpg       # Imagen de ejemplo con el mensaje que deberia llegar al celular    
│ └── instalacion.py            # Instalación paso a paso
├── src/                        # Código fuente  
│ └── programa_principal.py  
│ └── twilio_config.py  
├── .gitignore  
├── requerimientos.txt          # Dependencias de Python  
├── README.md
```
---