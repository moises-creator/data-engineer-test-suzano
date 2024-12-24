from asyncio import TaskGroup
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

class LoadToBigQueryTG(TaskGroup):
    def __init__(self, group_id, tooltip="Carregamento dos dados no BigQuery", **kwargs):
        super().__init__(group_id=group_id, tooltip=tooltip, **kwargs)

        
        load_bloomberg = GCSToBigQueryOperator(
            task_id="load_bloomberg",
            bucket="{{ params.bucket_name }}",
            source_objects=["bloomberg.csv"],
            destination_project_dataset_table="{{params.project_id}}.{{params.dataset_id}}.bloomberg",
            source_format="CSV",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
            task_group=self
        )

        load_usd_cny = GCSToBigQueryOperator(
            task_id="load_usd_cny",
            bucket="{{ params.bucket_name }}",
            source_objects=["usd_cny.csv"],
            destination_project_dataset_table="{{params.project_id}}.{{params.dataset_id}}.usd_cny",
            source_format="CSV",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
            task_group=self
        )

        load_china_index = GCSToBigQueryOperator(
            task_id="load_china_index",
            bucket="{{ params.bucket_name }}",
            source_objects=["china_index.csv"],
            destination_project_dataset_table="{{params.project_id}}.{{params.dataset_id}}.chinese_caixin_services_index",
            source_format="CSV",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
            task_group=self
        )

        load_bloomberg >> load_usd_cny >> load_china_index