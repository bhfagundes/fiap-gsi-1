# 🔋 Lumion - Análises Estatísticas  (SCR)

## 📝 Sumário

  - [👀 Visão Geral](#-visão-geral)
    
  - [🚀 Funcionalidades](#-funcionalidades)

  - [📋 Pré-requisitos](#-pré-requisitos)

  - [📦 Pacotes Necessários](#-pacotes-necessarios)

  - [⚙️ Configuração](#-configuração)
    
  - [🛠️ Instalação](#-instalação)
   
  - [🚀 Execução](#-execução)

  - [📊 Resultados](#-resutados)

  - [🤝 Contribuição](#-contribuição)

  - [📄 Licença](#-licença)


## 👀 Visão Geral
Análise de dados energéticos da ANEEL, este projeto realiza uma análise estatísticas dos dados de geração distribuída disponibilizados pela Agência Nacional de Energia Elétrica - ANEEL, com o objetivo de identificar padrões de consumo energético e oportunidades de transição para fontes sustentáveis.


## 🚀 Funcionalidades
- Download automático dos dados da ANEEL
- Processamento e limpeza dos dados
- Análises estatísticas detalhadas
- Visualizações gráficas
- Geração de relatório em HTML
  
## 📋 Pré-requisitos
- R (versão recomendada: 4.0.0 ou superior)
- RStudio (opcional)

## 📦 Pacotes Necessários

O script instalará automaticamente os seguintes pacotes, se necessário:
- stringi
- tidyverse
- plotly
- lubridate
- scales
- gridExtra
- forecast
- ggplot2
- dplyr
- tidyr


## ⚙️ Configuração

Você pode ajustar os seguintes parâmetros no início do script:
```
ANEEL_URL: URL para o download dos dados da ANEEL
```
```
local_file: Caminho local para salvar os dados baixados
```

### 🛠️ Instalação
1. Clone o repositório:
```
git clone https://github.com/seu-usuario/aneel-data-analysis.git
```
2. Navegue até o diretório do projeto:

```
cd aneel-data-analysis
```
3. Abra o script main.R no RStudio ou no seu editor de preferência.


## 🚀 Execução
Execute o script principal:

R
```
source("main.R")
```
O script irá:

- Baixar os dados mais recentes da ANEEL (se necessário)
- Processar e analisar os dados
- Gerar visualizações
- Criar um relatório em HTML

## 📊 Resultados
Após a execução:

- /resultados/: Diretório com arquivos CSV contendo análises detalhadas
- /resultados/plots/: Diretório com visualizações gráficas
- /relatorio_energia.html/: Relatório completo em formato HTML

## 🤝 Contribuição
1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença
Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
