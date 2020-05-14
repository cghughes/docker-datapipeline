#!/bin/bash
export AIRFLOW_HOME=/opt/airflow
sleep 10
airflow initdb
airflow webserver -p 8080 &

# Flower server for monitoring celery workers (optional)
# sleep 10
# flower -p 5555 --broker=pyamqp://airflow:3point142@rabbit01:5672/airflow --broker_api=http://airflow:3point142@rabbit01:15672/api/ &

airflow scheduler
