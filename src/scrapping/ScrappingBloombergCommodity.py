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
# Deixe o navegador visível (não use --headless)
driver = webdriver.Chrome(service=service, options=options)

url = "https://br.investing.com/indices/bloomberg-commodity"

try:
    driver.get(url)
    
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/nav/div[2]/ul/li[2]/a"))
    )

    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/nav/div[2]/ul/li[2]/a").click()

    
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]"))
    )

    # abre periodo
    periodo = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]")
    periodo.click()

    # seleciona mensal
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[3]"))  
    )

    data = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[3]")
    data.click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]"))  
    )

    # clica em selecionar data

    data = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]")
    data.click()
    

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/input"))  
    )

    # seleciona data
    date_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/input")
    date_input.click()
    date_input.clear()
    # date_input.send_keys("01011991")

    # date_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/input")))
    # date_input.clear()
    # date_input.send_keys("1991-01-01")


    time.sleep(10)

    table = driver.find_element(By.ID, "curr_table")                                    
    
    headers = [th.text for th in table.find_elements(By.TAG_NAME, "th")]
    
    rows = []
    for tr in table.find_elements(By.TAG_NAME, "tr"):
        row = [td.text for td in tr.find_elements(By.TAG_NAME, "td")]
        if row:
            rows.append(row)
    
    df = pd.DataFrame(rows, columns=headers)
    
    print(df)
    df.to_csv('C:\\Users\\MOTTA\\Downloads\\data-engineer-test-main\\src\\data\\BloombergCommodity.csv', index=False)
    
finally:
    driver.quit()
