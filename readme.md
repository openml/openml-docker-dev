# OpenML Docker compose images/scripts for local development setup (Linux/Windows)

## **For local dev environment setup only, Insecure & Not for Production Setup**


# Issues/limitations
- current only works on port 80
- wiki powered by gollum is not working (in the new OpenML frontend this will no longer be used).


# Requirements

- Git (https://git-scm.com/)
- Docker (https://www.docker.com/get-docker)

For Linux: docker commands assume you can use docker without sudo (your user is in docker group, ex: sudo usermod -aG docker $USER). Otherwise prefix docker commands with sudo. 


# Instructions


### Step 1: Clone the repos
First the Docker repo with the general structure and database files is cloned. Once this repo is cloned the content repos for the PHP website and Flask website are cloned in subfolders of this Docker repo. Multiple source folders for different versions of the websites are supported. This allows you to quickly change between two versions of the same website.


####  1. Docker repo
Clone and change into the Docker directory with the following commands

```
git clone https://github.com/openml/openml-docker-dev.git [Optional the name of the new directory (openml-docker-dev)]

cd [name of directory]
```

#### 2. PHP website repo
Clone the OpenML repo into the Docker directory. Select the "docker_changes" branch or any other branch that supports Docker integration

```
git clone -b docker_changes https://github.com/openml/OpenML.git [PHP directory name (OpenML)]
```
![](images/2018-04-07-00-57-29.png)

####  3. Flask website 

Clone the new website from here (also inside Docker directory), keep track of the folder name
- Branch name TBD

```
git clone -b docker https://github.com/OpenML/openml.org.git [Flask directory name (openml.org)]
```

* for PortML clone with
```
git clone -b docker https://github.com/PortML/openml.org.git [Flask directory name (openml.org)]
```

### Step 2: Set structure for storage folder
The Docker configuration uses host volumes to store data. This allows persistent data over restarts of the docker instances. In order to set this up the following folder structure must be present in the ``storage`` folder in the main Docker directory.

![](images/storage-directory.PNG)

Also copy the content of ``[PHP website directory]/data`` into ``storage/datastore`` this is used to initiate demo data

Note that deleting content in the ``es`` or ``mysql`` folder will delete the ElasticSearch and MySQL database respectively. The initialization scrips need to be run afterwards to init the demo data. Deleting one and not the other will likely result in data not correctly be referenced in the website.

### Step 3: Configure Docker and the websites
Most backend configurations can be set in the ``docker-compose.yml`` file. Front-end configurations for the React app needs to be defined in a separate environment file as these are compiled without the use of docker environment variables.

1. Copy ``docker-compose-template.yml`` and rename it to ``docker-compose.yml``

2. Edit MySQL configuration in ``docker-compose.yml`` mainly define a secure **mysql password**, optional change the database name:

    **(leaving the default will make docker-compose fail)**

    ![](images/compose-mysql-config.PNG)


3. Copy ``[PHP directory]\openml_OS\config\BASE_CONFIG-BLANK-ENV.php`` to ``[PHP directory]\openml_OS\config\BASE_CONFIG.php``

4. Edit the ``website`` environment variables in ``docker-compose.yml``:

    ![](images/compose-php-config.PNG)

    Change the usernames and passwords fields, (bby default you can use ``root`` as username and the password set in step 2)
    
    Other variables can be changed as well:
    - The ``HOST`` variables reference to the location of the MySQL database, for docker this is the container name of the MySQL image (mysql_test)
    - The ``ES_URL``s reference to the location of the ElasticSearch instance
    - Note that changing the ``DATA_PATH`` variable also requires you to change the volume definition for the datastore in the same compose file
    - It is not advised to change the ``DIRECTORY_PATH`` vairable as this also requires you to edit the ``Dockerfile`` in the ``website`` directory to reflect these changes so the source files are copied to the correct location inside the Docker image

5.  Optional non environmental changes in the ``[PHP directory]\openml_OS\config\BASE_CONFIG.php`` file

    ![](images/2018-04-07-01-04-02.png)

6.  Disable email activation in ``[PHP directory]OpenML/openml_OS/config/ion_auth.php``

    ![](images/2018-04-07-01-07-21.png)

7. Flask configurations
    1. Copy and rename ``.flaskenv_TEMPLATE`` to ``.flaskenv`` in the ``[Flask website directory]``
    2. Copy and rename ``TEMPLATE.reactenv`` to ``.reactenv`` in the ``[Flask website directory]``  or rename to ``.reactenv_aws`` for AWS deployment.
    3. Edit DATABASE_URI field in ``.flaskenv`` to add in the mysql password in place of PASSWORD-
  (use the same password as the mysql password in docker-compose.yml)
    4. Fill in the following environmental variables in the ``docker compose.yml`` file under the ``website_new`` service. These variables will overwrite the variables in ``.flaskenv`` but this is kept in place for backwards compatibility:
        1. DATABASE_URI=mysql+pymysql://root:[fil-in PASSWORD]@[fill-in MYSQL_CONTAINER_NAME]:3306/[fill-in DATABASE_NAME]
            - Fill in the PASSWORD, MYSQL_CONTAINER_NAME (``mysql_test``), and DATABASE_NAME (``openml``)
        2. ELASTICSEARCH_SERVER=[ES_URL] , default is ``http://elasticsearch:9200/``
        3. APP_SECRET_KEY and JWT_SECRET_KEY
        4. SERVER_URL, fill in container name of new website and the port (``http://website_new:5000/``)
        5. REDIRECT_URL, to new website (``http://website_new:5000``)
        6. BACKEND_SERVER, link to PHP backend server to set Python API server (``http://website/api/v1/xml/``)
        7. SEND_EMAIL, used for disabling sending emails in development (currently set to ``False`` as configuration is not yet tested with sending emails using the Docker setup)
        8. DASHBOARD_USE_DOCKER_CONTAINER_NAME, when using Docker downloading datasets from the dashboard code is not working as the container name should be used. Set this to true to use the DASHBOARD_PHP_CONTAINER_NAME
        9. DASHBOARD_PHP_CONTINER_NAME, name of the older backend container used for dashboard code when running Docker
    4. Note on DATABASE_URI: hostname should be 'mysql_test' (by default), the container name of database:
  ``DATABASE_URI=mysql+pymysql://[username]:[password]@mysql_test:3306/openml``
    5. Update the variables in the ``.reactenv`` file according to the deployment. The template file already is configured to work with localhost and the ports the containers are accessible to (80: PHP; 5000; Flask; 9200: ES)
    6. In order to enable the python debug prints in docker add the following lines of code to the ``docker-compose.yml`` file inside the ``website_new`` service
      ````
      environment:
            - PYTHONUNBUFFERED=1
      ````
    - Please make sure you rebuild the ``[Flask website directory]`` docker image if you make any changes to these configuration files using: 
      This will  make sure the react image is re-built (Don't do this before the first docker-compose up): 
    ```
    cd [Flask website directory]
    docker build -t openml-docker -f Dockerfile .
    ```
    - [Optionally] you can use a hot-reload configuration for the new website with some constrains, see the section below how to set this up

8. Copy evaluation engine
    - Copy the ``Java`` folder in ``[PHP website directory]/openml_OS/third_party/OpenML`` and copy it to ``openmlsource`` inside the Docker root folder. The Java background worker is configured to get the evaluation engine from this location. [Optional] a compiled JAR file from a newer version of the EvaluationEngine can be placed here inside a ``Java`` folder

<!-- - Continue with remaining steps and view Step 7 for testing new website changes
- Switch back to root folder


```
cd ..

``` -->

### Step 4: Starting docker-compose

Make sure docker is running.

On the Docker folder, where ``docker-compose.yml`` is located run:

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.8.2

docker-compose up
```
The elasticsearch pull is needed only for the very first time. Images can take few minutes to build for the first time, 
after start wait a few seconds for services to be ready, ex: MySQL ready for connections)

![](images/2018-04-07-01-11-21.png)

![](images/2018-04-07-01-12-43.png)

#### Development restarts
During development the Docker image needs to be recreated multiple times. The following commands ensure that old images are removed and a new image is recreated:
```
docker-compose rm -f
docker-compose pull
docker-compose up --build
```

Or chain it:
```
docker-compose rm -f ; docker-compose pull ; docker-compose up --build
```

### Step 5: Check phpmyadmin at http://localhost:8080/

![](images/2018-04-07-01-13-38.png)

![](images/2018-04-07-01-13-50.png)

![](images/2018-04-07-01-14-02.png)


### Step 6: Init dbs, admin user & elastic search indexes
The first command only needs to be run the first time, or every time when the persistent storage is disabled (not advised as configuration changes are required for this)

Execute in a new window/shell: 

```
docker exec -it openml-docker-dev_website_1 php index.php cron init_local_env
```

(take note the printed admin username and password, and wait to finish, can take 1-2mins)

![](images/localdb.PNG)



Change data folder owner to www-data apache user in container, allow for logs/uploads in data folder, resets log file permissions created in previous init step

Execute in a new window/shell:
```
docker exec -it openml-docker-dev_website_1 chown -R www-data:www-data /var/www/html/data
```


###  Step 6: Final tests (Old website)

Login on http://localhost with admin and saved password

![](images/admin.PNG)

![](images/2018-04-07-01-18-32.png)

![](images/2018-04-07-01-18-37.png)

### Check dataset 
We have 1 sample dataset
![](images/ds1.PNG)

### Test upload dataset & wait for feature calculation. The status will change to active in a few minutes.
![](images/2018-04-07-01-18-59.png)

![](images/2018-04-07-01-19-05.png)

![](images/upload2.PNG)

### Note: Files in OpenML cloned repo are mounted inside the website container, any change will reflect immediately on the site

### Step 7 New website checks 
- Check the new website running at localhost:5000. It should look similar to new.openml.org
- Sign up as a new user in the new website. (Note that you cannot use the admin account from the old website to login here)
- Sign in with your email and password
- You should be able to see your profile
- [Optional] By default the user created above is not an admin. This is required if you want to use the dataset upload. This can be done by loggin into MyPHPAdmin and changing the 'users_groups' row of this user. Set the 'group_id' to 1 (admin group) and save. This is not always needed, only when a user is created before the init commands are ran
- Check Dataset upload (required to fill in all fields)

### Step 8 Building images for remote deployment
The PortML version of the docker image also includes configurations for remote deployment (AWS) backend images (Flask and PHP) can use environment variables which can be set in the ``docker-compose.yml`` file and in the remote hosting environment. However, frontend (React) and database (MySQL) configurations need pre-build images specifically for the deployment. For this case a second compose file is created that targets these changes. In order to create image for AWS run the following command:
```
docker-compose -f docker-compose.yml -f docker-compose-aws.yml up -d --build
```

If small changes do not trigger an update when pushing to AWS use the following command(s) to build from scratch:

```
docker-compose rm -f ; docker-compose pull ; docker-compose -f docker-compose.yml -f docker-compose-aws.yml up -d --build
```

All environment settings in the docker files are not used when running the images on AWS, all environment variables therefore need to be set in the AWS task definition per container configuration

### [Optional hot-reload new website]
Using a hot-reload in docker requires you to set the volume of the source code to your local folder of the new website. Flask runs in development mode and will see changes you make without requireing you to rebuild the image. The only downside is that you are unable to reach the new front-end (React code) via the docker URL. You can seperatly run a node development server for the front-end to also enable hot-reload for the React front-end.

Add the following lines of code to the main 'docker-compose.yml' file inside the 'website_new' service to enable this hot-reload function:
````
volumes:
      - ./openml.org:/app
````

## Troubleshoot
If the new website rebuild doesn't work, try clearing all caches with:
```
docker system prune -a
```
and then, pull elastic search before doing docker-compose up.


### Java error
On windows by default the entry scripts use the Windows line ending (CRLF) this cannot be committed using git, but needs to be changed to ``LF``. 

### Cannot login with PhpMyadmin
Stop all containers. Try to delete the content of the ``mysql`` and ``es`` folder in the ``storage`` directory. And restart everything cleanly (with removing the previous images)

## ToDos
- Include Flask environmental variables in the docker-compose file
