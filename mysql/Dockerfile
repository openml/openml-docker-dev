FROM mysql
LABEL maintainer="Rui Quintino,https://github.com/rquintino"

# *.sql files in /docker-entrypoint-initdb.d are executed at mysql instance start, by alphabetical order

COPY ./openml_expdb.sql /docker-entrypoint-initdb.d
COPY ./openml.sql /docker-entrypoint-initdb.d