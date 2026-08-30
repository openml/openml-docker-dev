FROM python:3.7-slim

# Install python dependecies
RUN apt-get -y update && apt-get install
RUN apt-get install -y python3-pip python3-dev

# Copy requirements file to Docker
COPY ./requirements.txt /requirements.txt

# Install Python libraries from requirements file
RUN pip3 install -r requirements.txt

# Copy entrypoint file
COPY ./entrypoint.sh /entrypoint.sh

#Copt files
COPY ./upload-to-minio.py /upload-to-minio.py