FROM mysql
LABEL maintainer="Rui Quintino,https://github.com/rquintino"

# *.sql files in /docker-entrypoint-initdb.d are executed at mysql instance start, by alphabetical order

COPY ./OpenML/downloads/openml_expdb.sql /docker-entrypoint-initdb.d
COPY ./OpenML/downloads/openml.sql /docker-entrypoint-initdb.d