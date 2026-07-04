FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /{{ cookiecutter.project_name }}

RUN apt-get update && apt-get install -y \
    wget \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /{{ cookiecutter.project_name }}/docker/entrypoint.sh

EXPOSE 8000