FROM python:3.7

WORKDIR /
 
# Копируем файлы проекта в контейнер.
COPY . .
# Выполняем установку зависимостей внутри контейнера.
# раскоментировать что бы собрать на маке
RUN apt-get update \
    && apt-get -y install vim
RUN python3 -m pip install --upgrade pip setuptools
RUN pip3 install -r requirements.txt --no-cache-dir

# Выполнить запуск сервера при старте контейнера. 
# Для отображения отладочной информации добавить ключ "--log-syslog"
