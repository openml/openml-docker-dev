# OpenML Docker compose for local development setup

# Issues/limitations
- current only works on port 80
- wiki powered by gollum is not working yet

# Instructions

## Clone this repository & clone OpenML branch inside

git clone https://github.com/openml/openml-docker-dev.git

cd openml-docker-dev

git clone https://github.com/openml/OpenML.git

![](images/2018-04-07-00-57-29.png)

## Fill in Docker-compose Configuration

mainly define a secure mysql password:
![](images/2018-04-07-01-00-13.png)

## Fill in OpenML Configuration file

copy OpenML\openml_OS\config\BASE_CONFIG-BLANK.php to OpenML\openml_OS\config\BASE_CONFIG.php

Check & change BASE_CONFIG as appropriate, ex: (mysql password)

![](images/2018-04-07-01-01-52.png)

![](images/2018-04-07-01-02-07.png)

![](images/2018-04-07-01-02-46.png)

![](images/2018-04-07-01-03-14.png)

![](images/2018-04-07-01-03-52.png)

![](images/2018-04-07-01-04-02.png)

Disable email activation in OpenML\openml_OS\ion_auth.php

![](images/2018-04-07-01-07-21.png)

## Build images & start service containers

docker-compose up

(images can take few minutes to build for the first time, after start wait a few seconds for services to be ready)

![](images/2018-04-07-01-11-21.png)

![](images/2018-04-07-01-12-43.png)

## Check phpmyadmin at http://localhost:8080/

![](images/2018-04-07-01-13-38.png)

![](images/2018-04-07-01-13-50.png)

![](images/2018-04-07-01-14-02.png)

## Init dbs, admin user & elastic search indexes

Execute in a new window/shell:

docker exec -it openmldockerdev_website_1 php index.php cron init_local_env

(note the generated admin password, and wait to finish, can take 1-2mins)

![](images/2018-04-07-01-15-54.png)

![](images/2018-04-07-01-21-47.png) 

## Final tests

### Login on http://localhost with admin and saved password

![](images/2018-04-07-01-18-26.png)

![](images/2018-04-07-01-18-32.png)

![](images/2018-04-07-01-18-37.png)

### Check elastic search
![](images/2018-04-07-01-18-46.png)

### Test upload dataset & wait for feature calculation
![](images/2018-04-07-01-18-59.png)

![](images/2018-04-07-01-19-05.png)

## Files in OpenML cloned repo are mounted inside the website container, any change will reflect immediately on the site





