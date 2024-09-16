# Используем базовый образ Python
FROM python:3.9-slim

   # Устанавливаем рабочую директорию
WORKDIR /app

   # Копируем файлы приложения в рабочую директорию
COPY . .

   # Устанавливаем зависимости
RUN pip install --no-cache-dir streamlit pandas jupyter

   # Указываем команду для запуска приложения
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
