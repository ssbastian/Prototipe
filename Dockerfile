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

# Asegúrate de tener la última versión de pip, setuptools y wheel
RUN python -m pip install --upgrade pip setuptools wheel

# Instala dependencias desde requirements.txt
RUN pip install -r requirements.txt

# Expone el puerto que Render usará (por defecto 10000, o la variable $PORT)
EXPOSE 10000

# Comando de arranque (Render inyecta $PORT automáticamente)
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "10000"]