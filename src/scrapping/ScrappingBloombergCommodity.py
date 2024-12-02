from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# Deixe o navegador visível (não use --headless)
driver = webdriver.Chrome(service=service, options=options)

url = "https://br.investing.com/indices/bloomberg-commodity-historical-data"

try:
    driver.get(url)
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/table"))
    )
    
    table = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/table")
    
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
