import os
import csv
from typing import Any, Dict, List
import pymysql
import pandas as pd
from newsapi import NewsApiClient


from db import WarehouseConnection, get_warehouse_credentials


def fetch_page(api_key, start_date, end_date, page):
    """
    Queries the News API and returns breaking news.

            Parameters:
                    api_key (str): NewsAPI key (Register on the API website(https://newsapi.org/) to get a key.
                    start_date (str):
                    end_date (str):
                    page: Number of pages. Used to page through the results if the total results found is greater than the page size.
            Returns:
                    all_articles (dict): All the breaking news articles
    """
    newsapi = NewsApiClient(api_key=api_key)
    all_articles = newsapi.get_everything(
        q="*", from_param=start_date, to=end_date, language="en", page=page
    )
    return all_articles


def get_sources(article):
    """
    Extracts the source information from the results queried from the API and saves
    them to temp storage
    
        Parameters:
            article(dict)
        Returns:
            source_id (str):
    """

    source = article.get("source")
    source_name = source.get("name")
    save_to_csv([source_name.lower(), source_name], "/home/airflow/data/sources.csv")
    return source_name.lower()


def get_authors(article):
    """
    Extracts the authors information from the results queried from the API and saves
    them to temp storage
    
        Parameters:
            article(dict)
        Returns:
            author_id (str):
    """
    author_name = article.get("author")
    if isinstance(author_name, type(None)):
        author_name = "Anonymous"
    save_to_csv([author_name.lower(), author_name], "/home/airflow/data/authors.csv")
    return author_name.lower()


def get_content(article, author_id, source_id):
    """
    Get the main content of the news for the fact table and saves it to temporary locations
    and returns data to be saved to the blob storage
    """
    blob_id = article.get("publishedAt") + "_" + author_id + "_" + source_id
    title = article.get("title")
    description = article.get("description")
    url = article.get("url")
    published_date = article.get("publishedAt")
    content = article.get("content")
    save_to_csv(
        [author_id, source_id, title, url, published_date],
        "/home/airflow/data/articles.csv",
    )
    return {
        # "table": [author_id, source_id, title, url, published_date],
        "blob": {
            "date": published_date[:-10],
            "content": {
                "id": blob_id,
                "datetime": published_date,
                "description": description,
                "content": content,
            },
        },
    }


def fetch_all_pages(api_key, start_date, end_date, pages):
    for page in range(1, pages + 1):
        all_article = fetch_page(api_key, start_date, end_date, page)
        for article in all_article["articles"]:
            source_name = get_sources(article)
            author_name = get_authors(article)
            all_articles = get_content(article, author_name, source_name)


def load_dimension_data(filename, insert_query):
    """
    Read dimension table data (authors and sources) from
    temporary location and load to the data lake tables
    """
    df = pd.read_csv(filename).drop_duplicates(keep="last")
    for _, row in df.iterrows():
        send_data_to_destination([(row[0], row[1])], insert_query)


#[author_id, source_id, title, url, published_date]

def load_fact_table_data(filename, insert_query):
    """
    Read fact table data (articles) from
    temporary location and load to the data lake tables
    """
    df = pd.read_csv(filename).drop_duplicates(keep="last")
    for _, row in df.iterrows():
        send_data_to_destination([(row[0], row[1], row[2], row[3], row[4])], insert_query)


######### Helper functions ######################


def send_data_to_destination(data, query):
    with WarehouseConnection(get_warehouse_credentials()).managed_cursor() as curr:
        curr.executemany(query, data)


def save_to_csv(data, filename):
    with open(filename, "a", newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(data)


def delete_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)
