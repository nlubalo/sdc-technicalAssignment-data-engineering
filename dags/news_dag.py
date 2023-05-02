from datetime import datetime
import os

from airflow import DAG
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.python_operator import PythonOperator

from extract_api import fetch_all_pages, load_dimension_data, delete_if_exists