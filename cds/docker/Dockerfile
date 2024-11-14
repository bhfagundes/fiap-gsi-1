FROM postgres:13

ENV POSTGRES_DB=energy_consumption
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin123

COPY ../sql/schema.sql /docker-entrypoint-initdb.d/