# Базовый образ с Python 3.11
FROM python:3.11-slim

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копирование файлов в контейнер
COPY task2.py requirements.txt ./

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Команда по умолчанию для запуска скрипта
ENTRYPOINT ["python", "/app/task2.py"]

