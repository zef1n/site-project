# Используем официальный образ Python в качестве базового
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей в контейнер
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код в контейнер
COPY .. .

# Указываем переменную окружения для API_TOKEN (можно переопределить при запуске контейнера)
ENV API_TOKEN=your_default_token_here

# Указываем команду для запуска бота
CMD ["python", "bot.py"]