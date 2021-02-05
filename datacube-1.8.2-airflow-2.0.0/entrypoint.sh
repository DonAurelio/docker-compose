#!/bin/bash

#Reference: https://stackoverflow.com/questions/41451159/how-to-execute-a-script-when-i-terminate-a-docker-container

#Define cleanup procedure
cleanup() {
    echo "Container stopped, performing cleanup..."
    rm -rf /home/datacube/airflow/{*.out,*.pid,*.py,*.err,*.log}
    rm -rf /home/datacube/airflow/{unittests.cfg,logs}
}

#Cleanup at the begining
cleanup

#Trap SIGTERM
trap 'cleanup' SIGTERM

#Execute a command

airflow db init

airflow users create \
      --username admin \
      --firstname Peter \
      --lastname Parker \
      --role Admin \
      --email spiderman@superhero.org \
      --password admin

airflow webserver -D &

airflow celery flower -D &

airflow scheduler -D &

cd  /home/datacube

jupyter-lab --no-browser --LabApp.token='' --port=8081 --ip=0.0.0.0 --allow-root
