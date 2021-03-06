#!/bin/bash 

echo "Running entrypoint"

rm -rf /home/airflow/logs/*.err /home/airflow/logs/*.log /home/airflow/logs/*.pid

# initialize the database
echo "initdb ........."
airflow initdb

# start the scheduler
echo "scheduler ........."
airflow scheduler -D &

# start the scheduler
echo "worker ........."
airflow worker -D &

# start the web server, default port is 8080
echo "webserver ........."
airflow webserver -p 8080



# flower service
echo "flower ........."
# airflow flower
