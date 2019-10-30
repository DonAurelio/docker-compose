# Open Datacube as a Multi-Container Application

On this section, we will prepare the OpenDatacube environment to perform image processing and analysis. This multi-container applications comprise two containers:

* cube_db: The database used for the OpenDatacube API to index satellite imaginery.
* cube: The container with a ready to use OpenDatacube 1.6.1 and Python 3.6.

## Set Up

Clone this repository and get into the **open-datacube** foder using the following command

```sh 
git clone https://github.com/DonAurelio/docker-compose.git && cd docker-compose/open-datacube
```

Start containers

```sh
docker-compose up -d 
```

Inspect runnig containes

```sh
docker-compose ps
```

Get into the **cube** container

```sh
docker-compose exec cube bash
```

Exit within the container

```sh
exit
```

Stop containers

```sh
docker-compose stop
```

Start containers

```sh
docker-compose start
```

Destroy containers 

```sh
docker-compose down -v --remove-orphans
```
