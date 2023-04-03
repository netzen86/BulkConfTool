# BulkConfTool
Script for bulk configuration network devices.

Using netmiko.

In directory where place Dockerfile run this command for build docker image.  
```
docker build -t netmgmt .
docker buildx build --platform=linux/amd64 -t netmgmt .
```
Save docker image in file
```
docker save netmgmt:latest | gzip > netmgmt.tar.gz
```
Load docker image from file
```
docker load < netmgmt.tar.gz
```
Start the docker container using bash and after exiting the container remove it.
```
docker run -it --rm netmgmt bash
docker compose up -d
docker-compose -f docker-compose-local.yml exec netmgmt bash
```
```
export en_pass="p@S\$w0rd777"
export password="p@S\$w0rd890"
```