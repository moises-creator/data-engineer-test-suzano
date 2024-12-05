# 🛠 Data Engineer Test Solution

## 🚀 Projeto: Automação de Coleta e Armazenamento de Dados Econômicos

Este projeto tem como objetivo criar um pipeline para coletar, processar e armazenar dados econômicos a partir do site **Investing.com**, utilizando ferramentas modernas de orquestração, containerização e computação em nuvem.

---

## 📋 **Descrição do Problema**

### Dados Requeridos:
1. **Chinese Caixin Services Index**:
   - Fonte: [Investing.com](https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596)
   - Período: Mensal, de 2012 até o presente.
   - Campos: `date`, `actual_state`, `close`, `forecast`.

2. **Bloomberg Commodity Index**:
   - Fonte: [Investing.com](https://br.investing.com/indices/bloomberg-commodity)
   - Período: Mensal, de 1991 até o presente.
   - Campos: `date`, `close`, `open`, `high`, `low`, `volume`.

3. **USD/CNY**:
   - Fonte: [Investing.com](https://br.investing.com/currencies/usd-cny)
   - Período: Mensal, de 1991 até o presente.
   - Campos: `date`, `close`, `open`, `high`, `low`, `volume`.

### Objetivo:
Criar um pipeline para coletar esses dados automaticamente e armazená-los em um banco de dados relacional.

---

## 📂 **Estrutura do Projeto**

```bash
.
├── dags/                          # Código principal do DAG
│   ├── scraping_to_cloud_sql.py   # Orquestração do pipeline
├── include/                       # Recursos auxiliares
│   ├── sql/                       # Scripts SQL
│   │   ├── create_tables.sql      # Criação das tabelas no Cloud SQL
│   │   ├── load_bloomberg.sql     # Inserção de dados do Bloomberg
│   │   ├── load_usd_cny.sql       # Inserção de dados do USD/CNY
│   │   ├── load_china_index.sql   # Inserção de dados do índice chinês
│   ├── scraping_utils.py          # Funções de scraping
├── Dockerfile                     # Configuração do container
├── requirements.txt               # Dependências Python
├── .env                           # Variáveis sensíveis (não versionado)
└── README.md                      # Documentação do projeto
```

---

## 🛠️ **Tecnologias Utilizadas**

### Linguagem e Ferramentas:
- **Python** 🐍: Linguagem principal para desenvolvimento.
- **Apache Airflow** 🌬️: Orquestração de pipelines de dados.
- **Astro CLI** 🚀: Para gerenciamento de Airflow no Docker.
- **Docker** 🐳: Containerização do ambiente.
- **Google Cloud SQL** ☁️: Banco de dados relacional para armazenamento.

### Bibliotecas Python:
- **Selenium** 🖱️: Para automação de scraping web.
- **Requests** 🌐: Para consumo de APIs REST.
- **psycopg2** 🛢️: Para conexão ao banco de dados PostgreSQL.
- **python-dotenv** 🔑: Para gerenciamento de variáveis sensíveis.
- **rich** ✨: Para mensagens de console mais amigáveis.

---

## ⚙️ **Instalação e Configuração**

### 1. Pré-requisitos:
- **Docker** instalado ([Guia de Instalação](https://docs.docker.com/get-docker/)).
- **Astro CLI** instalado ([Guia de Instalação](https://docs.astronomer.io/astro/cli/install-cli)).

### 2. Configuração do Ambiente:
1. Clone este repositório:
   ```bash
   git clone git@github.com:moises-creator/data-engineer-test.git
   cd data-engineer-test
   ```

2. Configure as variáveis de ambiente:
   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```env
   DB_CONNECTION_ID=pg_default
   ```

3. Instale as dependências locais (opcional para desenvolvimento):
   ```bash
   pip install -r requirements.txt
   ```

---

### 3. Inicialize o Ambiente Astro CLI:
1. Suba os serviços com Docker:
   ```bash
   astro dev start
   ```

2. Acesse o Airflow UI:
   - URL: [http://localhost:8080](http://localhost:8080)
   - Usuário: `admin`
   - Senha: `admin`

3. Execute o DAG `scraping_to_cloud_sql` na interface.

---

## 🗂️ **Fluxo do Pipeline**

1. **Scraping dos Dados**:
   - Três tarefas paralelas coletam os dados usando **Selenium** e **Requests**.
   - Os dados são salvos em arquivos JSON no diretório `/tmp`.

2. **Criação de Tabelas**:
   - Um operador (`CloudSQLExecuteQueryOperator`) cria as tabelas no Google Cloud SQL.

3. **Carregamento dos Dados**:
   - Tarefas paralelas inserem os dados nas tabelas respectivas.

4. **Orquestração**:
   - As tarefas são orquestradas usando o **chain** do Airflow:
     ```python
     chain(
         scrape_bloomberg_task, 
         scrape_usd_cny_task, 
         scrape_china_index_task,
         create_tables_task,
         load_bloomberg_task, 
         load_usd_cny_task, 
         load_china_index_task,
     )
     ```

---

## 📈 **Consultando os Dados**

Após a execução do pipeline, os dados podem ser consultados no banco **Google Cloud SQL** via qualquer ferramenta de consulta SQL, como o DBeaver ou o cliente psql.

---

## 📋 **Melhorias Futuras**
- ✅ Implementar monitoramento com **Airflow SLA** para garantir alertas em falhas.
- ✅ Migrar o banco de dados para um ambiente **BigQuery** para análise de dados escalável.
- ✅ Automatizar a integração com um dashboard.
- ✅ Implementar Data Quality usando **Soda**.
- ✅ Aplicar **dbt** para modelagem dos dados.

--- 

## ✨ **Contato**
Em caso de dúvidas ou sugestões, entre em contato comigo pelo GitHub ou LinkedIn.

