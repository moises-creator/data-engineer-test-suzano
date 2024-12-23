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

    # @task_group(group_id='clean_group')
    # def cleanupGroup():
    #     cleanup_bloomberg_task = PostgresOperator(
    #         task_id="cleanup_bloomberg",
    #         postgres_conn_id=DB_CONNECTION_ID,
    #         sql="DROP TABLE IF EXISTS Bloomberg_Commodity_Index;"
    #     )

    #     cleanup_usd_cny_task = PostgresOperator(
    #         task_id="cleanup_usd_cny",
    #         postgres_conn_id=DB_CONNECTION_ID,
    #         sql="DROP TABLE IF EXISTS usd_cny;"
    #     )

    #     cleanup_china_index_task = PostgresOperator(
    #         task_id="cleanup_china_index",
    #         postgres_conn_id=DB_CONNECTION_ID,
    #         sql="DROP TABLE IF EXISTS chinese_caixin_services_index;"
    #     )

    #     cleanup_bloomberg_task >> cleanup_usd_cny_task >> cleanup_china_index_task

    # create_tables_task = PostgresOperator(
    #     task_id="create_tables",
    #     postgres_conn_id=DB_CONNECTION_ID,
    #     sql=read_sql_file("include/sql/create_tables.sql"),
    # )

    # @task_group(group_id='load_group')
    # def loadGroup():
    #     @task
    #     def load_bloomberg(**kwargs):
    #         loader = DataLoader(DB_CONNECTION_ID)
    #         loader.load_bloomberg(**kwargs)

    #     @task
    #     def load_usd_cny(**kwargs):
    #         loader = DataLoader(DB_CONNECTION_ID)
    #         loader.load_usd_cny(**kwargs)

    #     @task
    #     def load_china_index(**kwargs):
    #         loader = DataLoader(DB_CONNECTION_ID)
    #         loader.load_china_index(**kwargs)
            

    #     load_bloomberg() >> load_usd_cny() >> load_china_index()


    scrapeGroup() #>> cleanupGroup() >> create_tables_task >> loadGroup()

scraping_to_postgres()
