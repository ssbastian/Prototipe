# Usa Python 3.8 (compatible con Rasa 3.5)
FROM python:3.8-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala librerías del sistema necesarias
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        gfortran \
        libatlas-base-dev \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos del proyecto
COPY . /app

# Asegura versiones actualizadas de herramientas de instalación
RUN python -m pip install --upgrade pip setuptools wheel

# Instala dependencias desde requirements.txt
RUN pip install -r requirements.txt

# Render inyecta el puerto como variable de entorno $PORT
# No fijamos un puerto, sino que usamos el que Render proporcione
# Esto es lo que permite que Render lo detecte correctamente
CMD ["sh", "-c", "rasa run --enable-api --cors '*' --port ${PORT}"]
