from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain
from airflow.utils.dates import days_ago
from include.scraping_utils import scrape_bloomberg, scrape_usd_cny, scrape_china_index
import os

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

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

    chain(
        [scrape_bloomberg_task, scrape_usd_cny_task, scrape_china_index_task]

    )

scraping_to_cloud_sql()
