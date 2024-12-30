from airflow.decorators import dag, task, task_group
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator, BigQueryCreateEmptyDatasetOperator
from airflow.utils.dates import days_ago
from include.task_groups.scraper import DataScraperTG
from include.task_groups.upload_gcs import UploadToGcsTG
from include.task_groups.create_tables import CreateTablesTG
from include.task_groups.load_bg import LoadToBigQueryTG


params = {"bucket_name":"suzano-scraping-data","project_id":"gentle-platform-443802-k8", "dataset_id":"suzanoinvesting"}

@dag(start_date=days_ago(1), 
     schedule=None, 
     params=params,
     catchup=False, 
     tags=["scraping", "gcp", "bigquery"]
)


def scraping_to_gcp_bigquery():

    create_bucket = GCSCreateBucketOperator(
        task_id="create_bucket",
        bucket_name="{{ params.bucket_name }}",
        storage_class="STANDARD",
        location="US",
    )

    # create_dataset = BigQueryCreateEmptyDatasetOperator(
    #     task_id="create_dataset",
    #     dataset_id="{{ params.dataset_id }}",
    #     project_id="{{ params.project_id }}",
    #     location="US",
    # )

    scraper_group = DataScraperTG(group_id="scraper_group")

    upload_to_gcs = UploadToGcsTG(group_id="upload_to_gcs")

    create_tables = CreateTablesTG(group_id="create_tables")

    load_to_bigquery = LoadToBigQueryTG(group_id="load_to_bigquery")


    scraper_group >> upload_to_gcs >> create_tables >> load_to_bigquery

scraping_to_gcp_bigquery()
