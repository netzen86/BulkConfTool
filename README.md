# BulkConfTool
Script for bulk configuration network devices.

Using netmiko.

In directory where place Dockerfile run this command for build docker image.  
```
docker build -t runscript .
```
Save docker image in file
```
docker save myimage:latest | gzip > myimage_latest.tar.gz
```
Load docker image from file
```
docker load < busybox.tar.gz
```
Start the docker container using bash and after exiting the container remove it.
```
docker run -it --rm runscript bash
```