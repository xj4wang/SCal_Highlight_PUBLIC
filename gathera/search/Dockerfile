FROM tiangolo/uvicorn-gunicorn:python3.6

RUN pip install --no-cache-dir fastapi

# Install Pyserini
RUN pip install pyserini==0.9.4.0

# Install Java for Anserini
RUN echo $JAVA_HOME
RUN apt update -y
#RUN apt install -y software-properties-common python-software-properties
RUN apt install -y default-jdk
RUN JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64/bin/java"
RUN export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64/bin/java"


COPY ./app /app