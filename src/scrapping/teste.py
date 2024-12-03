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
    ).click()

    # Clique para abrir o calendário
    calendar_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]/div[3]/div[1]/div[1]/input")
    driver.execute_script("arguments[0].click();", calendar_input)

    # Selecione o ano (1991) - Clique no seletor de ano
    year_selector = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='ui-datepicker-year']"))
    )
    year_selector.click()

    # Escolha 1991 na lista de anos
    year_1991 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='1991']"))
    )
    year_1991.click()

    # Selecione o mês (Janeiro) - Clique no seletor de mês
    month_selector = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='ui-datepicker-month']"))
    )
    month_selector.click()

    # Escolha Janeiro (mês 0 no calendário, já que o índice começa em 0)
    january = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='0']"))
    )
    january.click()

    # Selecione o dia 1
    day_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='1']"))
    )
    day_1.click()

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
    df.to_csv('C:\\Users\\MOTTA\\Downloads\\data-engineer-test-main\\src\\data\\BloombergCommodity.csv', index=False)

finally:
    driver.quit()
