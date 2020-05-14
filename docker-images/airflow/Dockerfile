#FROM apache/airflow:1.10.10
FROM python:3.7

#ENV ACCEPT_EULA 'Y'
#ENV SA_PASSWORD 'yourStrong(!)Password'
USER root
RUN apt-get update 
RUN apt-get install -y vim binutils gcc build-essential netcat
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements2.txt ./
RUN pip install --no-cache-dir -r requirements2.txt

COPY requirements3.txt ./
RUN pip install --no-cache-dir -r requirements3.txt 

COPY requirements_airflow.txt ./
RUN pip install --no-cache-dir -r requirements_airflow.txt 

RUN rm -f requirements*

RUN useradd -ms /bin/bash airflow
RUN install -d -m 0755 -o airflow /opt/airflow 
WORKDIR /opt/airflow

COPY --chown=airflow initAirFlow-server.sh ./
RUN chmod +x ./initAirFlow-server.sh

COPY --chown=airflow initAirFlow-worker.sh ./
RUN chmod +x ./initAirFlow-worker.sh

COPY --chown=airflow airflow.cfg ./
COPY --chown=airflow flowerconfig.py ./

USER airflow

#ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["./initAirFlow-server.sh"]