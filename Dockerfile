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

# Configurações do Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependências do sistema necessárias para as bibliotecas Python
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

# Criar diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o projeto
COPY . .

# Coletar arquivos estáticos
# RUN python manage.py collectstatic --noinput

# Porta que o Render vai usar (importante!)
EXPOSE 8000

# Comando para iniciar - usando a variável PORT do Render
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT