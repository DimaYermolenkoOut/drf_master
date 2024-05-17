FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy requeriments.txt to the working directory
COPY requirements.txt .

# Install the requeriments
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
#FROM python:3.12
#
## Установка зависимостей системы
#RUN apt-get update && apt-get install -y \
#    libmariadb-dev-compat \
#    libmariadb-dev
#
## Установка рабочей директории
#WORKDIR /app
#
## Копирование requirements.txt и установка зависимостей
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#
## Копирование всего кода в рабочую директорию
#COPY . .
#
## Открытие порта 8000 для доступа извне
#EXPOSE 8000
#
## Выполнение миграций и запуск сервера при запуске контейнера
#CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
