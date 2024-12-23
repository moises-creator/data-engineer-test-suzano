from airflow.decorators import dag, task
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.utils.dates import days_ago

@dag(start_date=days_ago(1), schedule=None, catchup=False, tags=["scraping", "bigquery"])
def scraping_to_bigquery():

    @task
    def create_table():
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `SEU_PROJECT_ID.suzanoinvesting.bloomberg` (
            field1 STRING,
            field2 INT64,
            field3 FLOAT64
        )
        """
        hook = BigQueryHook()
        hook.run_query(create_table_query, use_legacy_sql=False)

    @task
    def scrape_bloomberg():
        return [{"field1": "value1", "field2": 123, "field3": 45.6}]

    @task
    def load_to_bigquery(data):
        hook = BigQueryHook()
        hook.insert_all(
            project_id="gentle-platform-443802-k8", 
            dataset_id="suzanoinvesting",
            table_id="bloomberg",
            rows=data
        )

    create_table() >> scrape_bloomberg() >> load_to_bigquery()

scraping_to_bigquery()
