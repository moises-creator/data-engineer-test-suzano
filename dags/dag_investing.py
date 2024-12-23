from airflow.decorators import dag, task, task_group
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from include.scraping_operations import DataScraper, DataLoader, read_sql_file
import os

DB_CONNECTION_ID = os.getenv("DB_CONNECTION_ID")


@dag(start_date=days_ago(1), schedule=None, catchup=False, tags=["scraping", "postgres"])
def scraping_to_postgres():

    @task_group(group_id='scrape_group')
    def scrapeGroup():
        @task
        def scrape_bloomberg(**kwargs):
            scraper = DataScraper()
            return scraper.scrape_bloomberg(**kwargs)


        @task
        def scrape_usd_cny(**kwargs):
            scraper = DataScraper()
            return scraper.scrape_usd_cny(**kwargs)

        @task
        def scrape_china_index(**kwargs):
            scraper = DataScraper()
            return scraper.scrape_china_index(**kwargs)
        
        scrape_bloomberg() >> scrape_usd_cny() >> scrape_china_index()
    scrapeGroup() 

scraping_to_postgres()
