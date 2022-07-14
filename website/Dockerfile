FROM php:7.0-apache
LABEL maintainer="Rui Quintino,https://github.com/rquintino"

# Set argument to make source directory variable
ARG sourceDirectory=OpenML

# Install PHP extensions and PECL modules.
RUN buildDeps=" \
    libbz2-dev \
    default-libmysqlclient-dev \
    " \
    runtimeDeps=" \
    curl \
    git \
    libfreetype6-dev \
    libicu-dev \
    libjpeg-dev \
    libmcrypt-dev \
    libpng-dev \
    libpq-dev \
    " \
    && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y $buildDeps $runtimeDeps \
    && docker-php-ext-install bz2 calendar iconv intl mbstring mcrypt mysqli pdo_mysql pdo_pgsql pgsql zip \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install gd \
    && pecl install redis \
    && docker-php-ext-enable redis.so \
    && apt-get purge -y --auto-remove $buildDeps \
    && rm -r /var/lib/apt/lists/*

# Install Composer.
ENV COMPOSER_HOME /root/composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
ENV PATH $COMPOSER_HOME/vendor/bin:$PATH


RUN a2enmod rewrite
RUN service apache2 restart

RUN ln -sf /dev/stdout /var/log/apache2/access.log

RUN ln -sf /dev/stderr /var/log/apache2/error.log

RUN mkdir -p /var/www/html
COPY ./${sourceDirectory} /var/www/html

## Disable coping config folder as this will be used by AWS EFS
# RUN mkdir -p /openmlconfig
# COPY ./api_key.txt /openmlconfig/api_key.txt

# COPY ./entrypoint.sh /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]