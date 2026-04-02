# FROM python:3.11-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# Instalar dependências de sistema necessárias
# RUN apt-get update && apt-get install -y \
  #  gcc \
  #  g++ \
  #  python3-dev \
  #  libcairo2-dev \
  #  libpango1.0-dev \
  #  libffi-dev \
  #  libssl-dev \
  #  build-essential \
  #  && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libffi-dev \
    libssl-dev \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o projeto
COPY . .

EXPOSE 8000

# Roda migrations antes de iniciar o Gunicorn
CMD python manage.py migrate --noinput && \
    gunicorn core.wsgi:application --bind 0.0.0.0:$PORT