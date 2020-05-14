FROM jupyter/scipy-notebook

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

RUN rm -f requirements*