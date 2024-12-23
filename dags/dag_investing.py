from airflow.decorators import dag, task, task_group
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator, GCSFileTransformOperator, GCSToBigQueryOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.utils.dates import days_ago
from include.scraping_operations import DataScraper
import os

GCP_BUCKET_NAME = "suzano-scraping-data"
PROJECT_ID = "gentle-platform-443802-k8"

@dag(start_date=days_ago(1), schedule=None, catchup=False, tags=["scraping", "gcp", "bigquery"])
def scraping_to_gcp_bigquery():

    # Criar o bucket no GCP (se não existir)
    create_bucket = GCSCreateBucketOperator(
        task_id="create_bucket",
        bucket_name=GCP_BUCKET_NAME,
        storage_class="STANDARD",
        location="US",
    )

    @task_group(group_id='scrape_group')
    def scrape_group():
        @task
        def scrape_bloomberg(**kwargs):
            """Scrape Bloomberg data and upload to GCP bucket."""
            scraper = DataScraper()
            scraper.scrape_bloomberg(**kwargs)
            os.system(f"gsutil cp include/csv/bloomberg.csv gs://{GCP_BUCKET_NAME}/bloomberg.csv")

        @task
        def scrape_usd_cny(**kwargs):
            """Scrape USD/CNY data and upload to GCP bucket."""
            scraper = DataScraper()
            scraper.scrape_usd_cny(**kwargs)
            os.system(f"gsutil cp include/csv/usd_cny.csv gs://{GCP_BUCKET_NAME}/usd_cny.csv")

        @task
        def scrape_china_index(**kwargs):
            """Scrape China Index data and upload to GCP bucket."""
            scraper = DataScraper()
            scraper.scrape_china_index(**kwargs)
            os.system(f"gsutil cp include/csv/china_index.csv gs://{GCP_BUCKET_NAME}/china_index.csv")

        scrape_bloomberg() >> scrape_usd_cny() >> scrape_china_index()

    @task
    def create_bigquery_tables():
        """Create BigQuery tables if they don't exist."""
        hook = BigQueryHook()
        queries = [
            """
            CREATE TABLE IF NOT EXISTS `gentle-platform-443802-k8.suzanoinvesting.bloomberg` (
                date DATE,
                close FLOAT64,
                open FLOAT64,
                high FLOAT64,
                low FLOAT64,
                volume INT64
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS `gentle-platform-443802-k8.suzanoinvesting.usd_cny` (
                date DATE,
                close FLOAT64,
                open FLOAT64,
                high FLOAT64,
                low FLOAT64,
                volume INT64
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS `gentle-platform-443802-k8.suzanoinvesting.chinese_caixin_services_index` (
                date DATE,
                actual_state STRING,
                close FLOAT64,
                forecast FLOAT64
            )
            """
        ]
        for query in queries:
            hook.run_query(query, use_legacy_sql=False)

    @task_group(group_id="load_to_bigquery")
    def load_to_bigquery():
        # Load Bloomberg data
        load_bloomberg = GCSToBigQueryOperator(
            task_id="load_bloomberg",
            bucket=GCP_BUCKET_NAME,
            source_objects=["bloomberg.csv"],
            destination_project_dataset_table=f"{PROJECT_ID}.suzanoinvesting.bloomberg",
            source_format="CSV",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
        )

        # Load USD/CNY data
        load_usd_cny = GCSToBigQueryOperator(
            task_id="load_usd_cny",
            bucket=GCP_BUCKET_NAME,
            source_objects=["usd_cny.csv"],
            destination_project_dataset_table=f"{PROJECT_ID}.suzanoinvesting.usd_cny",
            source_format="CSV",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
        )

        # Load China Index data
        load_china_index = GCSToBigQueryOperator(
            task_id="load_china_index",
            bucket=GCP_BUCKET_NAME,
            source_objects=["china_index.csv"],
            destination_project_dataset_table=f"{PROJECT_ID}.suzanoinvesting.chinese_caixin_services_index",
            source_format="CSV",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
        )

        load_bloomberg >> load_usd_cny >> load_china_index

    create_bucket >> scrape_group() >> create_bigquery_tables() >> load_to_bigquery()

scraping_to_gcp_bigquery()
