# 🔋 Sistema de Análise de Consumo Energético (CDS)

## 📝 Sumário
- [🔋 Sistema de Análise de Consumo Energético (CDS)](#-sistema-de-análise-de-consumo-energético-cds)
  - [📝 Sumário](#-sumário)
  - [👀 Visão Geral](#-visão-geral)
  - [🏗 Arquitetura](#-arquitetura)
  - [📁 Estrutura do Projeto](#-estrutura-do-projeto)
  - [⚙️ Configuração](#️-configuração)
    - [Pré-requisitos](#pré-requisitos)
    - [Instalação](#instalação)
- [Edite .env com suas credenciais](#edite-env-com-suas-credenciais)
  - [🚀 Execução](#-execução)
  - [📊 Pipeline de Dados](#-pipeline-de-dados)
    - [Coleta (ANEEL)](#coleta-aneel)
    - [Processamento](#processamento)
    - [Armazenamento](#armazenamento)
  - [🔗 Integração](#-integração)
    - [Com AICSS](#com-aicss)
    - [Com SCR](#com-scr)
  - [📈 Métricas e KPIs](#-métricas-e-kpis)
  - [🔒 Segurança](#-segurança)
  - [📚 Documentação API](#-documentação-api)
  - [🔄 Manutenção](#-manutenção)
  - [📱 Interface Web](#-interface-web)
  - [🌐 Endpoints API](#-endpoints-api)
    - [Dados ANEEL](#dados-aneel)
    - [Análise](#análise)
    - [Integração AICSS](#integração-aicss)
  - [🤝 Contribuição](#-contribuição)
  - [📊 Visualização](#-visualização)
    - [Dashboards](#dashboards)
    - [Relatórios](#relatórios)
  - [📄 Licença](#-licença)
  - [🔗 Links Úteis](#-links-úteis)

## 👀 Visão Geral
Sistema de análise de consumo energético que integra dados da ANEEL com informações do sistema AICSS para fornecer insights sobre padrões de consumo e eficiência energética.

## 🏗 Arquitetura

                    +------------+     +-----------+     +------------+
                    |  ANEEL API |     |AICSS Data|     |Sensor Data|
                    +------------+     +-----------+     +------------+
                           |                |                |
                           v                v                v
                                  +----------------+
                                  |   ETL Layer    |
                                  +----------------+
                                          |
                                          v
                                  +----------------+
                                  | PostgreSQL DB  |
                                  +----------------+
                                          |
                                          v
                                  +----------------+
                                  |Analytics Layer |
                                  +----------------+
                                       |     |
                                       v     v
                            +----------+     +-----------+
                            |Visualização    |Predições  |
                            +----------+     +-----------+

flowchart LR
    subgraph Fontes de Dados style fill:#f9f,stroke:#333
        A((ANEEL API)) --> ETL((ETL Layer))
        B(AICSS Data) --> ETL
        C(Sensor Data) --> ETL
    end

    ETL --> D{PostgreSQL DB}
    D --> E(Analytics Layer)
    E --> F(Visualização)
    E --> G(Predições)



## 📁 Estrutura do Projeto

cds/
├── docker/              # Containers e configurações
├── scripts/            # Scripts Python para ETL
│   ├── crawler.py     # Coleta dados ANEEL
│   ├── etl.py        # Processamento
│   └── pipeline.py   # Orquestração
├── sql/               # Schemas e queries
│   ├── schema.sql
│   └── queries/
├── data/              # Dados brutos e processados
└── README.md

## ⚙️ Configuração

### Pré-requisitos
- Docker e Docker Compose
- Python 3.8+
- PostgreSQL 13+
- pip (Python package manager)

### Instalação
1. Clone o repositório:

```bash
git clone <repository-url>
cd cds
```
2. Configure o ambiente:

python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt

3. Configure as variáveis de ambiente:

cp .env.example .env
# Edite .env com suas credenciais

## 🚀 Execução

1. Inicie os containers:

docker-compose up -d

2. Execute o pipeline:

python scripts/pipeline.py

## 📊 Pipeline de Dados

### Coleta (ANEEL)
- API REST para dados oficiais
- Periodicidade: Diária
- Formato: JSON/CSV

### Processamento
- Limpeza e validação
- Transformação de formatos
- Enriquecimento com dados AICSS (referência em `aicss/readme.md`, linhas 447-450)

### Armazenamento
- PostgreSQL com particionamento
- Índices otimizados
- Backup automático

## 🔗 Integração

### Com AICSS
- Dados de sensores (referência em `aicss/src/main.cpp`, linhas 5-10)
- Métricas de consumo
- Alertas em tempo real

### Com SCR
- Exportação para análise R (referência em `aicss/readme.md`, linhas 457-460)
- Importação de predições
- Métricas de desempenho

## 📈 Métricas e KPIs
- Tempo de processamento ETL
- Latência de queries
- Taxa de sucesso de coleta
- Qualidade dos dados

## 🔒 Segurança
- Autenticação JWT
- SSL/TLS
- Backup automático
- Logs de auditoria

## 📚 Documentação API
Disponível em: `/docs/api.md`

## 🔄 Manutenção
- Backup diário automatizado
- Monitoramento 24/7
- Alertas em tempo real
- Logs detalhados

## 📱 Interface Web
- Dashboard em tempo real
- Gráficos interativos
- Relatórios customizados
- Controle de acesso

## 🌐 Endpoints API

### Dados ANEEL

``` http
GET /api/v1/aneel/consumo
GET /api/v1/aneel/tarifas
POST /api/v1/aneel/sync
```

### Análise

``` http
GET /api/v1/analytics/consumo
GET /api/v1/analytics/previsao
GET /api/v1/analytics/relatorios
```
### Integração AICSS

``` http
POST /api/v1/aicss/dados
GET /api/v1/aicss/status
PUT /api/v1/aicss/config
```

## 🤝 Contribuição
1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request



## 📊 Visualização

### Dashboards
- Consumo em tempo real
- Histórico por período
- Previsões futuras
- Alertas e notificações

### Relatórios
- Diários
- Semanais
- Mensais
- Personalizados

## 📄 Licença
Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 🔗 Links Úteis
- [Documentação API](/docs/api.md)
- [Guia de Contribuição](/CONTRIBUTING.md)
- [Changelog](/CHANGELOG.md)
