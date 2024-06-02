FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD mchaysafer
ENV MYSQL_DATABASE offers_db

COPY init.sql /docker-entrypoint-initdb.d/
