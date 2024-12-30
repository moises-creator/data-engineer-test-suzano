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

        if "data" in data:
            df = pd.DataFrame(data['data'])
            
            colunas_relevantes = {
                'rowDate': 'date',
                'last_close': 'close',
                'last_open': 'open',
                'last_max': 'high',
                'last_min': 'low',
                'volume': 'volume'
            }

            df_filtrado = df[list(colunas_relevantes.keys())].rename(columns=colunas_relevantes)

            df_filtrado.to_csv('include/csv/bloomberg.csv', index=False)
            print("Dados filtrados e salvos com sucesso.")
        else:
            print("Erro: Dados não encontrados.")


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
        
        if "data" in data:
            df = pd.DataFrame(data['data'])

            colunas_relevantes = {
                'rowDate': 'date',
                'last_close': 'close',
                'last_open': 'open',
                'last_max': 'high',
                'last_min': 'low',
                'volume': 'volume'
            }

            df_filtrado = df[list(colunas_relevantes.keys())].rename(columns=colunas_relevantes)

            df_filtrado.to_csv('include/csv/usd_cny.csv', index=False)
            print("Dados filtrados e salvos com sucesso.")
        else:
            print("Erro: Dados não encontrados.")


    def scrape_china_index(self, **kwargs):
        """Scrape Chinese Caixin Services Index data and return as JSON."""
        url = "https://sbcharts.investing.com/events_charts/eu/596.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            if "attr" in data:
                df = pd.DataFrame(data['attr'])

                colunas_relevantes = {
                    'timestamp': 'date',
                    'actual': 'actual_state',
                    'actual_formatted': 'close',
                    'forecast_formatted': 'forecast'
                }

                df_filtrado = df[list(colunas_relevantes.keys())].rename(columns=colunas_relevantes)

                df_filtrado['date'] = pd.to_datetime(df_filtrado['date'], unit='ms')

                df_filtrado.to_csv('include/csv/china_index.csv', index=False)
                print("Dados filtrados e salvos com sucesso.")
            else:
                print("Erro: Dados não encontrados no JSON.")
        else:
            print(f"Erro ao acessar a URL. Código de status: {response.status_code}")
