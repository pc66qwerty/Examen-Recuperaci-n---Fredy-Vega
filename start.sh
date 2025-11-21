#!/bin/bash

# Crear directorio de archivos estáticos
mkdir -p staticfiles
mkdir -p static

# Ejecutar migraciones
python manage.py migrate --noinput

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Iniciar Gunicorn
gunicorn config.wsgi --log-file - --bind 0.0.0.0:$PORT