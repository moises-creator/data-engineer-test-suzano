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

    # Aguarde até que o botão seja clicável
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/nav/div[2]/ul/li[2]/a"))
    ).click()

    # Abre período
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]"))
    ).click()

    # Seleciona mensal
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[3]"))
    ).click()

    # Seleciona data
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]"))
    ).click()

    # Localiza o campo de data inicial
    data_inicial = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]/div[3]/div[1]/div[1]/input"))
    )

    # Verifica se o campo é clicável
    driver.execute_script("arguments[0].scrollIntoView(true);", data_inicial)
    driver.execute_script("arguments[0].value = arguments[1];", data_inicial, "")
    
    # Alterando a data com JavaScript
    driver.execute_script("arguments[0].value = '1991-01-01';", data_inicial)


    # Clique em aplicar para confirmar as alterações
    aplicar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]/div[3]/div[2]"))
    )

    # Rola até o botão para torná-lo visível
    driver.execute_script("arguments[0].scrollIntoView(true);", aplicar)
    print("Botão aplicar visível.")

    # Aguarda um pouco para garantir que o scroll foi concluído
    time.sleep(1)

    # Verifica se há pop-ups e os fecha
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Fechar') or contains(@aria-label, 'Close')]"))
        )
        close_button.click()
        print("Modal fechado com sucesso.")
    except Exception as e:
        print("Nenhum modal encontrado.", e)

    # Tenta clicar no botão usando JavaScript
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
