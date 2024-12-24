from include.scraping_operations import DataScraper
from airflow.utils.task_group import TaskGroup
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator


class UploadToGcsTG(TaskGroup):
    def __init__(self, group_id, tooltip="Criacao da tabela arquivos na camada bronze do BigQuery e Cloud Storage", **kwargs):
        super().__init__(group_id=group_id, tooltip=tooltip, **kwargs)


        upload_bloomberg = LocalFilesystemToGCSOperator(
            task_id="upload_bloomberg",
            src="include/csv/bloomberg.csv",
            dst="bloomberg.csv",
            bucket="{{ params.bucket_name }}",
            task_group=self
        )

        upload_usd_cny = LocalFilesystemToGCSOperator(
            task_id="upload_usd_cny",
            src="include/csv/usd_cny.csv",
            dst="usd_cny.csv",
            bucket="{{ params.bucket_name }}",
            task_group=self
        )

        upload_china_index = LocalFilesystemToGCSOperator(
            task_id="upload_china_index",
            src="include/csv/china_index.csv",
            dst="china_index.csv",
            bucket="{{ params.bucket_name }}",
            task_group=self
        )
        upload_bloomberg >> upload_usd_cny >> upload_china_index