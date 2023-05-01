# First-time build can take upto 10 mins.

FROM apache/airflow:2.5.3-python3.9

ENV AIRFLOW_HOME=/opt/airflow

USER $AIRFLOW_UID
#RUN apt-get update -qq && apt-get install vim -qqq

#RUN apt-get install -y python3
# git gcc g++ -qqq

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install newsapi-python

# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]



WORKDIR $AIRFLOW_HOME

#COPY scripts scripts
#RUN chmod +x scripts

USER $AIRFLOW_UID