
FROM mysql:5.7.25
LABEL maintainer="Rui Quintino,https://github.com/rquintino"

# *.sql files in /docker-entrypoint-initdb.d are executed at mysql instance start, by alphabetical order
ADD ./openml_expdb.sql /docker-entrypoint-initdb.d
ADD ./openml.sql /docker-entrypoint-initdb.d
COPY ./custom-mysql.cnf /etc/mysql/conf.d/
COPY ./portml-mysql.cnf /etc/mysql/my.cnf

# RUN mkdir -p /storage
# RUN chmod -R 777 /storage
# RUN groupadd -r -g 6000 mysqlgroup
# RUN useradd -r -u 6000 -g 6000 mysqluser
# USER mysqluser
# VOLUME ["/storage"]