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
│   ├── dag_investing.py           # Orquestração do pipeline
├── include/                       # Recursos auxiliares
│   ├── task_groups/               # Task Groups usados no DAG
│   │   ├── create_tables.py       # Task para criar tabelas no SQL
│   │   ├── load_bg.py             # Task para carregar dados do Bloomberg
│   │   ├── scraper.py             # Função de scraping centralizada
│   │   ├── upload_gcs.py          # Task para upload ao Google Cloud Storage
│   │   ├── scraping_operations.py # Outras operações de scraping
├── terraform/                     # Arquivos para provisionamento via Terraform
│   ├── main.tf                    # Configuração principal do Terraform
│   ├── variables.tf               # Variáveis para parametrização
│   ├── terraform.tfvars           # Configuração de outputs do Terraform
├── plugins/                       # Plugins personalizados
├── tests/                         # Testes unitários do projeto
├── Dockerfile                     # Configuração do container
├── docker-compose.override.yml    # Configuração adicional do Docker Compose
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
- **Terraform** ⚙️: Provisionamento de infraestrutura como código.
- **Google Cloud SQL** ☁️: Banco de dados relacional para armazenamento.

### Bibliotecas Python:
- **Selenium** 🖱️: Para automação de scraping web.
- **Requests** 🌐: Para consumo de APIs REST.
- **rich** ✨: Para mensagens de console mais amigáveis.

---

## ⚙️ **Instalação e Configuração**

### 1. Pré-requisitos:
- **Docker** instalado ([Guia de Instalação](https://docs.docker.com/get-docker/)).
- **Astro CLI** instalado ([Guia de Instalação](https://docs.astronomer.io/astro/cli/install-cli)).
- **Terraform** instalado ([Guia de Instalação](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)).

### 2. Configuração do Ambiente:
1. Clone este repositório:
   ```bash
   git clone git@github.com:moises-creator/data-engineer-test.git
   cd data-engineer-test
   ```

2. Configure as variáveis de ambiente:
   Navegue até o diretório `terraform`:
   ```
   cd terraform
   ```

### 3. Inicialize o Terraform:
1. Digite o comando:
   ```bash
   terraform init
   terraform apply
   ```
Obs: Para destruir o projeto, execute o comando `terraform destroy`. Aguarde alguns minutos para a instância estar completa para execução. 

2. Acesse o Airflow UI:
   - URL: acesse o ip externo da instância criada pelo terraform, tire o `s` do https e acrescente a porta na frente da url, exemplo: `http://34.123.54.2:8081`
   - Usuário: `admin`
   - Senha: `admin`
3. Acrescente a conexão com o gcp utilizando a interface `Connections`:
3.1 Project ID: `google_cloud_default`
3.2 Escolha `GoogleBigQuery`
3.3 Copie e cole a chave json criada no service account do IAM responsável pelo projeto no campo `KeyFile JSON`.


4. Execute a DAG `dag_investing` na interface.
```Obs: O site `investing.com` é um pouco pesado para a máquina virtual selecionada, caso apresente falhas na primeira e segunda tentativa, execute novamente por gentileza.```

---

5. Por fim, execute o seguinte comando no terminal local para excluir a instância:
```terraform destroy```

## 🗂️ **Fluxo do Pipeline**

1. **Cria bucket**:

1. **Scraping dos Dados**:

2. **Carrega os dados no gcs(bucket)**:

3. **Cria dataset no BigQuery**:

4. **Carrega os dados do bucket para o BigQuery**:

---

## 📈 **Consultando os Dados**

Após a execução do pipeline, os dados podem ser consultados no banco **Google Big Query** via qualquer ferramenta de consulta SQL.

---

## 📋 **Melhorias Futuras**
- ✅ Automatizar a integração com um dashboard.
- ✅ Implementar Data Quality usando **Soda**.
- ✅ Aplicar **dbt** para modelagem dos dados.

--- 

## ✨ **Contato**
Em caso de dúvidas ou sugestões, entre em contato comigo pelo GitHub ou LinkedIn.

