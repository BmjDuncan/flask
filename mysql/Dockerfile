FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD=goose

COPY ./database.sql /docker-entrypoint-initdb.d/
EXPOSE 3306
