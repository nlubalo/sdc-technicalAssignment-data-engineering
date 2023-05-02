from datetime import datetime
import os

from airflow import DAG
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.python_operator import PythonOperator

from news_etl import fetch_all_pages, load_dimension_data, delete_if_exists


default_args = {"owner": "airflow", "start_date": datetime(2023, 4, 27)}
newsapi_dag = DAG(
    dag_id="news_api_dag", default_args=default_args, schedule_interval="@weekly"
)

create_tables = MySqlOperator(
    task_id="create_tables",
    mysql_conn_id="mysql_newsDB",
    sql="create_tables.sql",
    dag=newsapi_dag,
)
delete_source_file_task = PythonOperator(
    task_id="delete_source_file",
    python_callable=delete_if_exists,
    op_kwargs={"filename": "/home/airflow/data/sources.csv"},
    dag=newsapi_dag,
)

delete_authors_file_task = PythonOperator(
    task_id="delete_authors_file",
    python_callable=delete_if_exists,
    op_kwargs={"filename": "/home/airflow/data/authors.csv"},
    dag=newsapi_dag,
)

delete_articles_file_task = PythonOperator(
    task_id="delete_articles_file",
    python_callable=delete_if_exists,
    op_kwargs={"filename": "/home/airflow/data/articles.csv"},
    dag=newsapi_dag,
)


"""
TODO:
    change start date and end dates to a dynamic values
"""
extract_and_transform_task = PythonOperator(
    task_id="extract_data",
    python_callable=fetch_all_pages,
    op_kwargs={
        "api_key": os.getenv("KEY", ""),
        "start_date": "2023-04-23",
        "end_date": "2023-04-30",
        "pages": 5,
    },
    dag=newsapi_dag,
)
# Add dag to delete temp files  load_dimension_data("authors.csv", insert_query)


load_source_data_task = PythonOperator(
    task_id="load_source_data",
    python_callable=load_dimension_data,
    op_kwargs={
        "filename": "/home/airflow/data/sources.csv",
        "insert_query": """INSERT IGNORE INTO newsDb.sources (sourceID, sourceName) VALUES (%s, %s)""",
    },
    dag=newsapi_dag,
)


load_authors_data_task = PythonOperator(
    task_id="load_authors_data",
    python_callable=load_dimension_data,
    op_kwargs={
        "filename": "/home/airflow/data/authors.csv",
        "insert_query": """INSERT IGNORE INTO newsDb.authors (authorID, authorName) VALUES (%s, %s)""",
    },
    dag=newsapi_dag,
)


create_tables >> delete_source_file_task >> delete_authors_file_task >> delete_articles_file_task >> extract_and_transform_task >> load_source_data_task >> load_authors_data_task
