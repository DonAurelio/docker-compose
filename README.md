# A bunch of docker-compose.yml files

Docker compose enables the **orchestration** of multiple containers using a single command line tool, unlike Docker that allows you to manage a single container at a time. Docker componse is designed to deploy applications that relly on multiple services (containers), such us database, web server, nfs an so on. 

This repository contains a set of ready to use docker-compose files to deploy multi-container applications for scientific purposes.

## Content

To deploy a multi-container application using the one of the following files, you need to install Docker and Docker Componse.

1. [Apache Airflow](https://github.com/DonAurelio/docker-compose/tree/master/airflow): A Python API to programmatically author, schedule and monitor workflows in Python.
2. [Open Datacube](https://github.com/DonAurelio/docker-compose/tree/master/open-datacube): A Python API and a set of GIS libraries to enable the storage and query of satellity imaginery data.

## Install Docker and Docker Compose


Update the source list

```sh 
sudo apt-get update
```

Install the ubuntu distribution of docker

```sh 
sudo apt-get install docker.io
```

Create the **docker** group

```sh 
sudo groupadd docker
```

Add the current user to the docker group

```sh 
sudo usermod -aG docker $USER
```

Reboot your system 

```sh 
sudo reboot now
```

Install **pip** and use it to instal **docker-compose**

```sh 
sudo apt-get install python-pip
pip install docker-compose
```
