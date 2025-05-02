# Usa Python 3.8 (slim-buster para compatibilidad con librerías)
FROM python:3.8-slim-buster

# Establece el directorio de trabajo
WORKDIR /app

# Instala solo las librerías esenciales del sistema (evita redundancias)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia solo los archivos necesarios (mejora caché de Docker)
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto (después de instalar dependencias para caché)
COPY . .

# Puerto dinámico (Railway inyecta $PORT igual que Render)
CMD sh -c "rasa run --enable-api --cors '*' --port \$PORT"
