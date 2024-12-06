import json
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models.baseoperator import chain
from airflow.utils.dates import days_ago
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime
from include.scraping_utils import scrape_bloomberg, scrape_usd_cny, scrape_china_index
import os

DB_CONNECTION_ID = os.getenv("DB_CONNECTION_ID")

def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def load_bloomberg_task(**kwargs):
    """Processa e carrega os dados do Bloomberg no banco de dados."""
    
    data = kwargs['ti'].xcom_pull(task_ids='scrape_bloomberg')

    
    if isinstance(data, str):
        data = json.loads(data)

    
    rows = [
        (
            row['rowDateTimestamp'][:10],  # Date
            row['last_closeRaw'],         # Close
            row['last_openRaw'],          # Open
            row['last_maxRaw'],           # High
            row['last_minRaw'],           # Low
            row.get('volumeRaw', 0)       # Volume
        )
        for row in data['data']
    ]

    
    pg_hook = PostgresHook(postgres_conn_id=DB_CONNECTION_ID)
    pg_hook.insert_rows(
        table="Bloomberg_Commodity_Index",  
        rows=rows,                         
        target_fields=["date", "close", "open", "high", "low", "volume"],  
        commit_every=1000                  
    )



def load_usd_cny_task(**kwargs):
    """Processa e carrega os dados de USD/CNY no banco de dados."""
    
    data = kwargs['ti'].xcom_pull(task_ids='scrape_usd_cny')

    
    if isinstance(data, str):
        data = json.loads(data)

    
    rows = [
        (
            row['rowDateTimestamp'][:10],  # Date
            row['last_closeRaw'],         # Close
            row['last_openRaw'],          # Open
            row['last_maxRaw'],           # High
            row['last_minRaw'],           # Low
            row.get('volumeRaw', 0)       # Volume
        )
        for row in data['data']
    ]

    
    pg_hook = PostgresHook(postgres_conn_id=DB_CONNECTION_ID)
    pg_hook.insert_rows(
        table="usd_cny",  
        rows=rows,        
        target_fields=["date", "close", "open", "high", "low", "volume"],  
        commit_every=1000  
    )


def load_china_index_task(**kwargs):
    """Processa e carrega os dados do índice da China no banco de dados."""
    
    data = kwargs['ti'].xcom_pull(task_ids='scrape_china_index')

    
    if isinstance(data, str):
        data = json.loads(data)

    
    rows = [
        (
            datetime.utcfromtimestamp(row['timestamp'] // 1000).strftime('%Y-%m-%d'),  # Date
            row['actual_state'],  # Actual State
            row['actual'],        # Close
            row.get('forecast')   # Forecast
        )
        for row in data['attr']
    ]

    
    pg_hook = PostgresHook(postgres_conn_id=DB_CONNECTION_ID)
    pg_hook.insert_rows(
        table="chinese_caixin_services_index",  
        rows=rows,                             
        target_fields=["date", "actual_state", "close", "forecast"],  
        commit_every=1000                      
    )


@dag(start_date=days_ago(1), schedule=None, catchup=False, tags=["scraping", "postgres"])
def scraping_to_postgres():
    
    scrape_bloomberg_task = PythonOperator(
        task_id='scrape_bloomberg',
        python_callable=scrape_bloomberg,  
    )

    scrape_usd_cny_task = PythonOperator(
        task_id='scrape_usd_cny',
        python_callable=scrape_usd_cny,  
    )

    scrape_china_index_task = PythonOperator(
        task_id='scrape_china_index',
        python_callable=scrape_china_index,  
    )

    cleanup_bloomberg_task = PostgresOperator(
        task_id="cleanup_bloomberg",
        postgres_conn_id=DB_CONNECTION_ID,
        sql="DROP TABLE IF EXISTS Bloomberg_Commodity_Index;"
    )

    cleanup_usd_cny_task = PostgresOperator(
        task_id="cleanup_usd_cny",
        postgres_conn_id=DB_CONNECTION_ID,
        sql="DROP TABLE IF EXISTS usd_cny;"
    )

    cleanup_china_index_task = PostgresOperator(
        task_id="cleanup_china_index",
        postgres_conn_id=DB_CONNECTION_ID,
        sql="DROP TABLE IF EXISTS chinese_caixin_services_index;"
    )

    
    create_tables_task = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id=DB_CONNECTION_ID,
        sql=read_sql_file("include/sql/create_tables.sql"),
    )

    
    load_bloomberg = PythonOperator(
        task_id="load_bloomberg",
        python_callable=load_bloomberg_task,
        provide_context=True,  
    )

    load_usd_cny = PythonOperator(
        task_id="load_usd_cny",
        python_callable=load_usd_cny_task,
        provide_context=True,
    )

    load_china_index = PythonOperator(
        task_id="load_china_index",
        python_callable=load_china_index_task,
        provide_context=True,
    )

    
    chain(
        scrape_bloomberg_task,
        scrape_usd_cny_task,
        scrape_china_index_task,
        cleanup_bloomberg_task,
        cleanup_usd_cny_task,
        cleanup_china_index_task,
        create_tables_task,
        load_bloomberg,
        load_usd_cny,
        load_china_index,
    )


scraping_to_postgres()
