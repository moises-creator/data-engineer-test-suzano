from selenium import webdriver
from datetime import datetime
import requests 
import json
from rich import print
import psycopg2

# Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="investing-extract",
    user="postgres",
    password="simba123",
    host="34.173.89.99",
    port="5432"
)

data_hoje = datetime.now().strftime('%Y-%m-%d')

options = webdriver.ChromeOptions()
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


# Abrir o site para estabelecer o contexto
driver.get("https://www.investing.com/")

# Substituir a data na URL dinamicamente
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
data_bloomberg = driver.execute_script(script)
data_bloomberg = json.loads(data_bloomberg)

with open('data_bloomberg.json', 'w') as json_file:
    json.dump(data_bloomberg, json_file, indent=4)

print(data_bloomberg)

#URL_USD_CNY
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

data_usd_cny = driver.execute_script(script)
data_usd_cny = json.loads(data_usd_cny)

with open('data_usd_cny.json', 'w') as json_file:
    json.dump(data_usd_cny, json_file, indent=4)

print(data_usd_cny)


#PARTE FINAL
url = "https://sbcharts.investing.com/events_charts/eu/596.json"

# Fazer a requisição GET
response = requests.get(url)

# Verificar o status e processar os dados
if response.status_code == 200:
    data = response.json()  # Converte a resposta JSON em um dicionário Python
    print(data)
    with open('data_china.json', 'w') as json_file:
      json.dump(data, json_file, indent=4)
else:
    print(f"Erro: {response.status_code}")

# Fechar o driver
driver.quit()

#Insercao:

cursor = conn.cursor()

# Criar a tabela (se ainda não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Bloomberg_Commodity_Index (
    date DATE NOT NULL,
    close DECIMAL(10, 2),
    open DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    volume BIGINT,
    PRIMARY KEY (date)
);
""")

conn.commit()

# Carregar o arquivo JSON
with open('data_bloomberg.json', 'r') as file:
    data = json.load(file)

# Iterar sobre os dados e inserir no banco
for entry in data['data']:
    date = entry['rowDateTimestamp'][:10]  # Extrair apenas a data
    close = float(entry['last_closeRaw'])
    open_ = float(entry['last_openRaw'])
    high = float(entry['last_maxRaw'])
    low = float(entry['last_minRaw'])
    volume = int(entry['volumeRaw']) if entry['volumeRaw'] else 0  # Substituir valor vazio por 0

    cursor.execute("""
        INSERT INTO Bloomberg_Commodity_Index (date, close, open, high, low, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO NOTHING;
    """, (date, close, open_, high, low, volume))
conn.commit()

# Criar a tabela (se ainda não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS usd_cny (
    date DATE NOT NULL,
    close DECIMAL(10, 2),
    open DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    volume BIGINT,
    PRIMARY KEY (date)
);
""")
conn.commit()

# Carregar o arquivo JSON
with open('data_usd_cny.json', 'r') as file:
    data = json.load(file)

# Iterar sobre os dados e inserir no banco
for entry in data['data']:
    date = entry['rowDateTimestamp'][:10]  # Extrair apenas a data
    close = float(entry['last_closeRaw'])
    open_ = float(entry['last_openRaw'])
    high = float(entry['last_maxRaw'])
    low = float(entry['last_minRaw'])
    volume = int(entry['volumeRaw']) if entry['volumeRaw'] else 0  # Substituir valor vazio por 0

    cursor.execute("""
        INSERT INTO usd_cny (date, close, open, high, low, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO NOTHING;
    """, (date, close, open_, high, low, volume))
conn.commit()

# Criar a tabela, caso não exista
cursor.execute("""
CREATE TABLE IF NOT EXISTS chinese_caixin_services_index (
    date DATE NOT NULL,
    actual_state VARCHAR(255),
    close DECIMAL(10, 2),
    forecast DECIMAL(10, 2),
    PRIMARY KEY (date)
)
""")
conn.commit()

# Carregar o arquivo JSON
with open('data_china.json', 'r') as file:
    data = json.load(file)

# Iterar sobre os dados e inserir no banco
for entry in data['attr']:
    timestamp = int(entry['timestamp']) // 1000  # Converter de milissegundos para segundos
    date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
    actual_state = entry['actual_state']
    close = entry['actual']
    forecast = entry['forecast'] if entry['forecast'] is not None else None

    cursor.execute("""
    INSERT INTO chinese_caixin_services_index (date, actual_state, close, forecast)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (date) DO NOTHING;
    """, (date, actual_state, close, forecast))

# Confirmar as alterações e fechar a conexão
conn.commit()
cursor.close()
conn.close()
