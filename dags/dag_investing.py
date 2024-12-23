from airflow.decorators import dag, task, task_group
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.utils.dates import days_ago
from include.scraping_operations import DataScraper

GCP_BUCKET_NAME = "suzano-scraping-data"
PROJECT_ID = "gentle-platform-443802-k8"

@dag(start_date=days_ago(1), schedule=None, catchup=False, tags=["scraping", "gcp", "bigquery"])
def scraping_to_gcp_bigquery():

    create_bucket = GCSCreateBucketOperator(
        task_id="create_bucket",
        bucket_name=GCP_BUCKET_NAME,
        storage_class="STANDARD",
        location="US",
    )

    @task_group(group_id='scrape_group')
    def scrape_group():
        @task
        def scrape_bloomberg():
            """Scrape Bloomberg data."""
            scraper = DataScraper()
            scraper.scrape_bloomberg()
        
        @task
        def scrape_usd_cny():
            """Scrape USD/CNY data."""
            scraper = DataScraper()
            scraper.scrape_usd_cny()
        
        @task
        def scrape_china_index():
            """Scrape China Index data."""
            scraper = DataScraper()
            scraper.scrape_china_index()

        scrape_bloomberg() >> scrape_usd_cny() >> scrape_china_index()

    @task_group(group_id="upload_to_gcs")
    def upload_to_gcs():
        upload_bloomberg = LocalFilesystemToGCSOperator(
            task_id="upload_bloomberg",
            src="include/csv/bloomberg.csv",
            dst="bloomberg.csv",
            bucket=GCP_BUCKET_NAME,
        )

        upload_usd_cny = LocalFilesystemToGCSOperator(
            task_id="upload_usd_cny",
            src="include/csv/usd_cny.csv",
            dst="usd_cny.csv",
            bucket=GCP_BUCKET_NAME,
        )

        upload_china_index = LocalFilesystemToGCSOperator(
            task_id="upload_china_index",
            src="include/csv/china_index.csv",
            dst="china_index.csv",
            bucket=GCP_BUCKET_NAME,
        )

        upload_bloomberg >> upload_usd_cny >> upload_china_index

    @task_group(group_id="create_tables")
    def create_tables():
        create_bloomberg_table = BigQueryInsertJobOperator(
            task_id="create_bloomberg_table",
            configuration={
                "query": {
                    "query": """
                    CREATE TABLE IF NOT EXISTS `gentle-platform-443802-k8.suzanoinvesting.bloomberg` (
                        date DATE,
                        close FLOAT64,
                        open FLOAT64,
                        high FLOAT64,
                        low FLOAT64,
                        volume INT64
                    )
                    """,
                    "useLegacySql": False,
                }
            },
        )

        create_usd_cny_table = BigQueryInsertJobOperator(
            task_id="create_usd_cny_table",
            configuration={
                "query": {
                    "query": """
                    CREATE TABLE IF NOT EXISTS `gentle-platform-443802-k8.suzanoinvesting.usd_cny` (
                        date DATE,
                        close FLOAT64,
                        open FLOAT64,
                        high FLOAT64,
                        low FLOAT64,
                        volume INT64
                    )
                    """,
                    "useLegacySql": False,
                }
            },
        )

        create_china_index_table = BigQueryInsertJobOperator(
            task_id="create_china_index_table",
            configuration={
                "query": {
                    "query": """
                    CREATE TABLE IF NOT EXISTS `gentle-platform-443802-k8.suzanoinvesting.chinese_caixin_services_index` (
                        date DATE,
                        actual_state STRING,
                        close FLOAT64,
                        forecast FLOAT64
                    )
                    """,
                    "useLegacySql": False,
                }
            },
        )

        create_bloomberg_table >> create_usd_cny_table >> create_china_index_table


    @task_group(group_id="load_to_bigquery")
    def load_to_bigquery():
        load_bloomberg = GCSToBigQueryOperator(
            task_id="load_bloomberg",
            bucket=GCP_BUCKET_NAME,
            source_objects=["bloomberg.csv"],
            destination_project_dataset_table=f"{PROJECT_ID}.suzanoinvesting.bloomberg",
            source_format="CSV",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
        )

        load_usd_cny = GCSToBigQueryOperator(
            task_id="load_usd_cny",
            bucket=GCP_BUCKET_NAME,
            source_objects=["usd_cny.csv"],
            destination_project_dataset_table=f"{PROJECT_ID}.suzanoinvesting.usd_cny",
            source_format="CSV",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
        )

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

    create_bucket >> scrape_group() >> upload_to_gcs() >> create_tables() >> load_to_bigquery()

scraping_to_gcp_bigquery()
