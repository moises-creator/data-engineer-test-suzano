import json
from datetime import datetime
from selenium import webdriver
import requests

def scrape_bloomberg(output_path: str, chromedriver_path: str) -> str:
    """
    Scrape Bloomberg Commodity Index data and save to a JSON file.
    """
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

    data_hoje = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.investing.com/api/financialdata/historical/948434?start-date=1991-01-01&end-date={data_hoje}&time-frame=Monthly"

    script = f"""
    return fetch("{url}", {{
        method: "GET",
        headers: {{
            "accept": "*/*",
            "content-type": "application/json"
        }}
    }}).then(response => response.json());
    """
    data = driver.execute_script(script)
    driver.quit()

    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

    return output_path


def scrape_usd_cny(output_path: str, chromedriver_path: str) -> str:
    """
    Scrape USD/CNY data and save to a JSON file.
    """
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

    data_hoje = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.investing.com/api/financialdata/historical/2111?start-date=1991-01-01&end-date={data_hoje}&time-frame=Monthly"

    script = f"""
    return fetch("{url}", {{
        method: "GET",
        headers: {{
            "accept": "*/*",
            "content-type": "application/json"
        }}
    }}).then(response => response.json());
    """
    data = driver.execute_script(script)
    driver.quit()

    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

    return output_path


def scrape_china_index(output_path: str) -> str:
    """
    Scrape Chinese Caixin Services Index data and save to a JSON file.
    """
    url = "https://sbcharts.investing.com/events_charts/eu/596.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)
        return output_path
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
