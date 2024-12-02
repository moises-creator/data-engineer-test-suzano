from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


service = Service(ChromeDriverManager().install())  
options = webdriver.ChromeOptions()
options.add_argument("--headless")  

driver = webdriver.Chrome(service=service, options=options)

url = "https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596"

try:
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "eventHistoryTable596"))
    )
    
    while True:
        try:
            load_more_button = driver.find_element(By.ID, "showMoreHistory596")
            load_more_button.click()
        except Exception as e:
            print("Não há mais botões para clicar ou erro ao clicar:", e)
            break
    
    table = driver.find_element(By.ID, "eventHistoryTable596")
    
    headers = [th.text for th in table.find_elements(By.TAG_NAME, "th")]

    rows = []
    for tr in table.find_elements(By.TAG_NAME, "tr"):
        row = [td.text for td in tr.find_elements(By.TAG_NAME, "td")]
        if row:
            rows.append(row)
    
    df = pd.DataFrame(rows, columns=headers)
    
    print(df)
    df.to_csv('C:\\Users\\MOTTA\\Downloads\\data-engineer-test-main\\src\\data\\ChineseCaixinServicesIndex.csv', index=False)


finally:
    driver.quit()
