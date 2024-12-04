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
# options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--disable-Advertisement")
options.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome(service=service, options=options)

url = "https://br.investing.com/indices/bloomberg-commodity"

try:
    driver.get(url)

    # Aguarde até que o botão de "Histórico" seja clicável
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/nav/div[2]/ul/li[2]/a"))
    ).click()

    # Aguarde até que o campo de seleção de período seja clicável
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]"))
    ).click()

    # Seleciona "Mensal"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[3]"))
    ).click()

    # Seleciona o campo de data inicial
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]/div[3]/div[1]/div[1]/input"))
    )

    # Foca no campo e insere a data
    data_inicial = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]/div[3]/div[1]/div[1]/input")
    driver.execute_script("arguments[0].scrollIntoView(true);", data_inicial)
    driver.execute_script("arguments[0].value = '1991-01-01';", data_inicial)

    # Aplica as alterações
    aplicar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]/div[3]/div[2]"))
    )
    driver.execute_script("arguments[0].click();", aplicar)

    # Aguarda a tabela carregar
    table = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div[3]/table"))
    )

    # Extraindo os dados da tabela
    headers = [th.text for th in table.find_elements(By.TAG_NAME, "th")]
    rows = []
    for tr in table.find_elements(By.TAG_NAME, "tr"):
        row = [td.text for td in tr.find_elements(By.TAG_NAME, "td")]
        if row:
            rows.append(row)

    df = pd.DataFrame(rows, columns=headers)
    print(df)

    # Salvar os dados em CSV
    df.to_csv('data\\BloombergCommodity.csv', index=False)

finally:
    driver.quit()
