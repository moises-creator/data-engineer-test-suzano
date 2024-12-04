from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import time


service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
#navegador visível (não use --headless)
options.add_argument('log-level=INT')
driver = webdriver.Chrome(service=service, options=options)

url = "https://br.investing.com/indices/bloomberg-commodity"

try:
    print("START!!!!!!!")
    driver.get(url)
    print("Estou aqui")

    print("Vou clicar no anuncio")
    time.sleep(100)
    driver.find_element(By.XPATH, "/html/body/iframe[1]").click()

    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/nav/div[2]/ul/li[2]/a").click()
    print("Dados históricos")

    periodo = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]")
    periodo.click()
    print("Período clicado")

    data = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[3]")
    data.click()


    # seleciona data
    # clica em selecionar data
    data = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]")
    data.click()


    # clica em data inicial
    data_inicial = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/input")
    data_inicial.click()
    
    print("CLIQUEI EM DATA INICIAL")

    time.sleep(10)

    table = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div[3]/table")                                    
    
    headers = [th.text for th in table.find_elements(By.TAG_NAME, "th")]
    
    rows = []
    for tr in table.find_elements(By.TAG_NAME, "tr"):
        row = [td.text for td in tr.find_elements(By.TAG_NAME, "td")]
        if row:
            rows.append(row)
    
    df = pd.DataFrame(rows, columns=headers)
    
    print(df)
    df.to_csv('data\\BloombergCommodity.csv', index=False)
    
finally:
    driver.quit()