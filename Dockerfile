# Usa Python 3.10 (compatible con Rasa 3.x)
FROM python:3.10-slim

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

# Crea y activa entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instala dependencias
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Expone el puerto que Render usará (Render requiere que sea 10000 por defecto, o usar $PORT)
EXPOSE 10000

# Comando de arranque (Render usa $PORT automáticamente)
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "10000"]