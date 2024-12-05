from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.cloud_sql import CloudSQLExecuteQueryOperator
from airflow.models.baseoperator import chain
from airflow.utils.dates import days_ago
from include.scraping_utils import scrape_bloomberg, scrape_usd_cny, scrape_china_index
import os

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
GCP_CONNECTION_ID = "gcp_cloud_sql"
INSTANCE_CONNECTION_NAME = "your-project-id:region:instance-name"  

@dag(start_date=days_ago(1), schedule=None, catchup=False, tags=["scraping", "cloud_sql"])
def scraping_to_cloud_sql():

    scrape_bloomberg_task = PythonOperator(
        task_id='scrape_bloomberg',
        python_callable=scrape_bloomberg,
        op_kwargs={
            'output_path': '/tmp/bloomberg.json',
            'chromedriver_path': CHROMEDRIVER_PATH,
        }
    )

    scrape_usd_cny_task = PythonOperator(
        task_id='scrape_usd_cny',
        python_callable=scrape_usd_cny,
        op_kwargs={
            'output_path': '/tmp/usd_cny.json',
            'chromedriver_path': CHROMEDRIVER_PATH,
        }
    )

    scrape_china_index_task = PythonOperator(
        task_id='scrape_china_index',
        python_callable=scrape_china_index,
        op_kwargs={
            'output_path': '/tmp/china_index.json',
        }
    )

    create_tables_task = CloudSQLExecuteQueryOperator(
        task_id="create_tables",
        gcp_conn_id=GCP_CONNECTION_ID,
        instance=INSTANCE_CONNECTION_NAME,
        database="investing_extract",
        sql="""
        CREATE TABLE IF NOT EXISTS Bloomberg_Commodity_Index (
            date DATE NOT NULL,
            close DECIMAL(10, 2),
            open DECIMAL(10, 2),
            high DECIMAL(10, 2),
            low DECIMAL(10, 2),
            volume BIGINT,
            PRIMARY KEY (date)
        );
        CREATE TABLE IF NOT EXISTS usd_cny (
            date DATE NOT NULL,
            close DECIMAL(10, 2),
            open DECIMAL(10, 2),
            high DECIMAL(10, 2),
            low DECIMAL(10, 2),
            volume BIGINT,
            PRIMARY KEY (date)
        );
        CREATE TABLE IF NOT EXISTS chinese_caixin_services_index (
            date DATE NOT NULL,
            actual_state VARCHAR(255),
            close DECIMAL(10, 2),
            forecast DECIMAL(10, 2),
            PRIMARY KEY (date)
        );
        """,
    )

    load_bloomberg_task = CloudSQLExecuteQueryOperator(
        task_id="load_bloomberg",
        gcp_conn_id=GCP_CONNECTION_ID,
        instance=INSTANCE_CONNECTION_NAME,
        database="investing_extract",
        sql=""" 
        INSERT INTO Bloomberg_Commodity_Index (date, close, open, high, low, volume)
        VALUES (%(date)s, %(close)s, %(open)s, %(high)s, %(low)s, %(volume)s)
        ON CONFLICT (date) DO NOTHING;
        """,
        parameters=[
            {
                "date": row['rowDateTimestamp'][:10],
                "close": row['last_closeRaw'],
                "open": row['last_openRaw'],
                "high": row['last_maxRaw'],
                "low": row['last_minRaw'],
                "volume": row.get('volumeRaw', 0),
            }
            for row in json.load(open('/tmp/bloomberg.json', 'r'))['data']
        ],
    )

    load_usd_cny_task = CloudSQLExecuteQueryOperator(
        task_id="load_usd_cny",
        gcp_conn_id=GCP_CONNECTION_ID,
        instance=INSTANCE_CONNECTION_NAME,
        database="investing_extract",
        sql=""" 
        INSERT INTO usd_cny (date, close, open, high, low, volume)
        VALUES (%(date)s, %(close)s, %(open)s, %(high)s, %(low)s, %(volume)s)
        ON CONFLICT (date) DO NOTHING;
        """,
        parameters=[
            {
                "date": row['rowDateTimestamp'][:10],
                "close": row['last_closeRaw'],
                "open": row['last_openRaw'],
                "high": row['last_maxRaw'],
                "low": row['last_minRaw'],
                "volume": row.get('volumeRaw', 0),
            }
            for row in json.load(open('/tmp/usd_cny.json', 'r'))['data']
        ],
    )

    load_china_index_task = CloudSQLExecuteQueryOperator(
        task_id="load_china_index",
        gcp_conn_id=GCP_CONNECTION_ID,
        instance=INSTANCE_CONNECTION_NAME,
        database="investing_extract",
        sql=""" 
        INSERT INTO chinese_caixin_services_index (date, actual_state, close, forecast)
        VALUES (%(date)s, %(actual_state)s, %(close)s, %(forecast)s)
        ON CONFLICT (date) DO NOTHING;
        """,
        parameters=[
            {
                "date": datetime.utcfromtimestamp(row['timestamp'] // 1000).strftime('%Y-%m-%d'),
                "actual_state": row['actual_state'],
                "close": row['actual'],
                "forecast": row.get('forecast'),
            }
            for row in json.load(open('/tmp/china_index.json', 'r'))['attr']
        ],
    )

    chain(
        [scrape_bloomberg_task, scrape_usd_cny_task, scrape_china_index_task],
        create_tables_task,
        [load_bloomberg_task, load_usd_cny_task, load_china_index_task],
    )


scraping_to_cloud_sql()
