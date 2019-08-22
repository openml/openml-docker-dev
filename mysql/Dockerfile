FROM mysql
LABEL maintainer="Rui Quintino,https://github.com/rquintino"

# *.sql files in /docker-entrypoint-initdb.d are executed at mysql instance start, by alphabetical order
ADD ./openml_expdb.sql /docker-entrypoint-initdb.d
ADD ./openml.sql /docker-entrypoint-initdb.d