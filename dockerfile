# Используем официальный образ Python 3.13 (когда он выйдет)
# Пока лучше использовать 3.11 или 3.12 (как стабильные версии)
FROM python:3.12-slim-bookworm

WORKDIR /app

# Устанавливаем зависимости системы для PostgreSQL и других пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Сначала копируем только requirements.txt для кэширования слоя
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY backend/ .

# Команда запуска (лучше использовать gunicorn для продакшена)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]