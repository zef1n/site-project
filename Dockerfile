# 1. Используем базовый образ Python
FROM python:3.10-slim

# 2. Устанавливаем обновления системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
ENV API_TOKEN='7442945233:AAFcqTkImSRADz5IoZdK9zurLbyATDGopP0'
# 3. Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем файлы бота в контейнер
COPY . /app
WORKDIR /app

# 5. Указываем команду для запуска бота
CMD ["python", "bot.py"]

# 6. Опционально указываем порт (не обязательно для Telegram-бота)
EXPOSE 80
