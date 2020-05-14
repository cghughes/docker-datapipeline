# CGH DEV docker-datapipeline
CGH DEV Docker Data Pipeline Template
1. Cassandra DB (with 3 nodes) - pipeline data store
2. Maria DB (single node) - airflow metadata instance
3. Rabbit MQ - broker to handle Airflow worker requests
4. Airflow - Web and Scheduler (with celery and flower) + example based on Papermill
5. Airflow Worker (with 2 nodes)
6. Jupyter Notebook
