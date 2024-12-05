import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

def create_driver():
    """
    Cria uma instância do Selenium WebDriver para uso remoto.
    """
    options = Options()
    driver = webdriver.Remote(
        command_executor="http://selenium:4444",  # URL do serviço Selenium
        options=options
    )
    return driver

def scrape_bloomberg() -> dict:
    """
    Scrape Bloomberg Commodity Index data and return as JSON.
    """
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
        "sec-ch-ua": "'Microsoft Edge';v='131', 'Chromium';v='131', 'Not_A Brand';v='24'",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "'Windows'",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }}
    }})
    .then(response => response.json())
    .then(data => JSON.stringify(data)) // Transformar os dados em string JSON para retornar ao Python
    .catch((error) => JSON.stringify({{"error": error.message}})); // Corrigir erro
    """

    driver = create_driver()
    try:
        data = json.loads(driver.execute_script(script))
    finally:
        driver.quit()

    return data

def scrape_usd_cny() -> dict:
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
        "sec-ch-ua": "'Microsoft Edge';v='131', 'Chromium';v='131', 'Not_A Brand';v='24'",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "'Windows'",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }}
    }})
    .then(response => response.json())
    .then(data => JSON.stringify(data))
    .catch((error) => JSON.stringify({{"error": error.message}}));
    """

    driver = create_driver()
    try:
        data = json.loads(driver.execute_script(script))
    finally:
        driver.quit()

    return data

def scrape_china_index() -> dict:
    """
    Scrape Chinese Caixin Services Index data and return as JSON.
    """
    url = "https://sbcharts.investing.com/events_charts/eu/596.json"
    # Fazer a requisição GET
    response = requests.get(url)
    # Verificar o status e processar os dados
    if response.status_code == 200:
        data = response.json()  # Converte a resposta JSON em um dicionário Python
        return data