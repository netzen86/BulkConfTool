FROM python:3.10

WORKDIR /
 
# Копируем файлы проекта в контейнер.
COPY . .
# Выполняем установку зависимостей внутри контейнера.
# раскоментировать что бы собрать на маке
RUN apt update \
    && apt -y install vim libsasl2-dev python-dev libldap2-dev libssl-dev
RUN python3 -m pip install --upgrade pip setuptools
RUN pip3 install -r requirements.txt --no-cache-dir

# Выполнить запуск сервера при старте контейнера. 
# Для отображения отладочной информации добавить ключ "--log-syslog"
