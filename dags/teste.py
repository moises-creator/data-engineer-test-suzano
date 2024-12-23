from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

# Operadores do Google Cloud
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

import pandas as pd
import os

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

def create_csv_from_dataframe(**context):
    """
    Gera (ou obtém) um DataFrame em memória e salva como CSV em /tmp/.
    """
    # Exemplo de DataFrame estático
    data = {
        "id": [1, 2, 3],
        "nome": ["Alice", "Bob", "Charlie"]
    }
    df = pd.DataFrame(data)

    # Caminho temporário onde vamos salvar o CSV
    local_path = "/tmp/meu_df.csv"

    # Salva o CSV sem o índice
    df.to_csv(local_path, index=False)

    # Retorna o caminho do arquivo para o próximo operador usar via XCom
    return local_path

with DAG(
    dag_id="df_para_csv_gcs_bq",
    default_args=default_args,
    schedule_interval=None,  # ou "0 7 * * *" etc., se quiser agendar
) as dag:

    # Task 1: criar o CSV a partir de um DataFrame
    task_df_to_csv = PythonOperator(
        task_id="df_to_csv",
        python_callable=create_csv_from_dataframe,
    )

    # Variáveis para o restante do pipeline
    BUCKET_NAME = "meu-bucket"
    DEST_GCS_PATH = "pasta/no/bucket/meu_df.csv"
    BQ_TABLE = "seu_projeto.seu_dataset.sua_tabela"

    # Task 2: subir o CSV local para o GCS
    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id="upload_csv_to_gcs",
        src="{{ ti.xcom_pull(task_ids='df_to_csv') }}",  # Pega o path do CSV retornado pela task anterior
        dst=DEST_GCS_PATH,
        bucket=BUCKET_NAME,
        gcp_conn_id="google_cloud_default",
    )

    # Task 3: carregar do GCS para BigQuery
    gcs_to_bq = GCSToBigQueryOperator(
        task_id="gcs_para_bigquery",
        bucket=BUCKET_NAME,
        source_objects=[DEST_GCS_PATH],
        destination_project_dataset_table=BQ_TABLE,
        source_format="CSV",
        write_disposition="WRITE_TRUNCATE",  # sobrescreve a tabela toda vez
        skip_leading_rows=1,                # se o CSV tem header
        field_delimiter=",",
        gcp_conn_id="google_cloud_default",
    )

    # Definição da ordem das tasks no DAG
    task_df_to_csv >> upload_csv_to_gcs >> gcs_to_bq