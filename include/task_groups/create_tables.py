from include.scraping_operations import DataScraper
from airflow.utils.task_group import TaskGroup
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator



class CreateTablesTG(TaskGroup):
        def __init__(self, group_id, projet_id="gentle-platform-443802-k8", dataset_id="suzanoinvesting", tooltip="Cria tabelas no BigQuery", **kwargs):
            super().__init__(group_id=group_id, tooltip=tooltip, **kwargs)

            create_bloomberg_table = BigQueryInsertJobOperator(
                task_id="create_bloomberg_table",
                configuration={
                    "query": {
                        "query": f"""
                        CREATE TABLE IF NOT EXISTS `{projet_id}.{dataset_id}.bloomberg` (
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
                task_group=self
            )

            create_usd_cny_table = BigQueryInsertJobOperator(
                task_id="create_usd_cny_table",
                configuration={
                    "query": {
                        "query": f"""
                        CREATE TABLE IF NOT EXISTS `{projet_id}.{dataset_id}.usd_cny` (
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
                task_group=self
            )

            create_china_index_table = BigQueryInsertJobOperator(
                task_id="create_china_index_table",
                configuration={
                    "query": {
                        "query": f"""
                        CREATE TABLE IF NOT EXISTS `{projet_id}.{dataset_id}.chinese_caixin_services_index` (
                            date DATE,
                            actual_state STRING,
                            close FLOAT64,
                            forecast FLOAT64
                        )
                        """,
                        "useLegacySql": False,
                    }
                },
                task_group=self
            )

            create_bloomberg_table >> create_usd_cny_table >> create_china_index_table
