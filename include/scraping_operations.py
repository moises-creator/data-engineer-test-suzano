import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from airflow.hooks.postgres_hook import PostgresHook
import requests
import pandas as pd

def read_sql_file(filepath):
    """Lê um arquivo SQL e retorna o conteúdo como uma string."""
    with open(filepath, 'r') as file:
        return file.read()

class DataScraper:
    def create_driver(self):
        """Cria uma instância do Selenium WebDriver para uso remoto."""
        options = Options()
        driver = webdriver.Remote(
            command_executor="http://selenium:4444",
            options=options
        )
        driver.get("https://www.investing.com")
        WebDriverWait(driver, 20).until(EC.url_contains("investing.com"))
        return driver

    def scrape_bloomberg(self, **kwargs):
        """Scrape Bloomberg Commodity Index data and return as JSON."""
        data_hoje = datetime.now().strftime('%Y-%m-%d')
        script = f"""
        return fetch("https://api.investing.com/api/financialdata/historical/948434?start-date=1991-01-01&end-date={data_hoje}&time-frame=Monthly&add-missing-rows=false", {{
            method: "GET",
            headers: {{
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "content-type": "application/json",
                "domain-id": "www",
                "origin": "https://www.investing.com",
                "referer": "https://www.investing.com/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0"
            }}
        }})
        .then(response => response.json())
        .then(data => JSON.stringify(data))
        .catch((error) => JSON.stringify({{"error": error.message}}));
        """
        driver = self.create_driver()
        try:
            data = json.loads(driver.execute_script(script))
        finally:
            driver.quit()

        pd.DataFrame(data['data']).to_csv('include/csv/bloomberg.csv', index=False)

    def scrape_usd_cny(self, **kwargs):
        """Scrape USD/CNY data."""
        data_hoje = datetime.now().strftime('%Y-%m-%d')
        script = f"""
        return fetch("https://api.investing.com/api/financialdata/historical/2111?start-date=1991-01-01&end-date={data_hoje}&time-frame=Monthly&add-missing-rows=false", {{
            method: "GET",
            headers: {{
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "content-type": "application/json",
                "domain-id": "www",
                "origin": "https://www.investing.com",
                "referer": "https://www.investing.com/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0"
            }}
        }})
        .then(response => response.json())
        .then(data => JSON.stringify(data))
        .catch((error) => JSON.stringify({{"error": error.message}}));
        """
        driver = self.create_driver()
        try:
            data = json.loads(driver.execute_script(script))
        finally:
            driver.quit()
        
        pd.DataFrame(data['data']).to_csv('include/csv/usd_cny.csv', index=False)

    def scrape_china_index(self, **kwargs):
        """Scrape Chinese Caixin Services Index data and return as JSON."""
        url = "https://sbcharts.investing.com/events_charts/eu/596.json"
        response = requests.get(url)
        if response.status_code == 200:
            pd.DataFrame(response.json()['attr']).to_csv('include/csv/china_index.csv', index=False)

class DataLoader:
    def __init__(self, db_connection_id):
        self.pg_hook = PostgresHook(postgres_conn_id=db_connection_id)

    def load_bloomberg(self, **kwargs):
        """Processa e carrega os dados do Bloomberg no banco de dados."""
        data = kwargs['ti'].xcom_pull(task_ids="scrape_group.scrape_bloomberg", key='bloomberg_data')

        rows = [
            (
                row['rowDateTimestamp'][:10],   
                row['last_closeRaw'],          
                row['last_openRaw'],           
                row['last_maxRaw'],            
                row['last_minRaw'],            
                row.get('volumeRaw', 0)        
            )
            for row in data['data']
        ]
        self.pg_hook.insert_rows(
            table="Bloomberg_Commodity_Index",
            rows=rows,
            target_fields=["date", "close", "open", "high", "low", "volume"],
            commit_every=1000
        )

    def load_usd_cny(self, **kwargs):
        """Processa e carrega os dados de USD/CNY no banco de dados."""
        data = kwargs['ti'].xcom_pull(task_ids="scrape_group.scrape_usd_cny", key='usd_cny_data')

        rows = [
            (
                row['rowDateTimestamp'][:10],   
                row['last_closeRaw'],          
                row['last_openRaw'],           
                row['last_maxRaw'],            
                row['last_minRaw'],            
                row.get('volumeRaw', 0)        
            )
            for row in data['data']
        ]
        self.pg_hook.insert_rows(
            table="usd_cny",
            rows=rows,
            target_fields=["date", "close", "open", "high", "low", "volume"],
            commit_every=1000
        )

    def load_china_index(self, **kwargs):
        """Processa e carrega os dados do índice da China no banco de dados."""
        data = kwargs['ti'].xcom_pull(task_ids="scrape_group.scrape_china_index", key='china_index_data')

        rows = [
            (
                datetime.utcfromtimestamp(row['timestamp'] // 1000).strftime('%Y-%m-%d'),   
                row['actual_state'],       
                row['actual'],             
                row.get('forecast')        
            )
            for row in data['attr']
        ]
        self.pg_hook.insert_rows(
            table="chinese_caixin_services_index",
            rows=rows,
            target_fields=["date", "actual_state", "close", "forecast"],
            commit_every=1000
        )
