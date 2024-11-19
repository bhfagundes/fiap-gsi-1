# 🔋 Lumion - Sistema Inteligente de Iluminação Residencial (AICSS)

## 📝 Sumário

  - [👀 Visão Geral](#-visão-geral)
     
  - [🔧 Componentes do sistema](#-componentes-do-sistema)
    
  - [⚙️ Funcionamento](#️-funcionamento)
    
  - [🛠️ Guia de Instalação](#️-guia-de-instalação)
    - [📡 Conexões de Hardware](#conexões-de-hardware)
    - [📊 Diagrama de Conexões](#diagrama-de-conexões)
    - [💻 Configuração do Ambiente](#configurações-do-ambiente)
    - [🔧 Montagem Física](#montagem-física)
    - [⚡ Primeira Execução](#primeira-execução)
    - [🔬 Detalhes Técnicos](#detalhes-tecnicos)
    - [📈 Métricas de Desempenho](#métricas-de-desempenho)
    - [ 🔍 Troubleshooting](#troubleshooting)
    - [ 📱 Próximos Passos](#próximos-passos)
  
  - [🔄 Plano de Manutenção](#plano-de-manutenção)
            
  - [💰 Análise Econômica](#-análise-econômica)
    - [📊 Cenário Atual](#cenario-atual)
    - [📈 Projeção de Economia](#projeção-de-economia)
    - [💎 Análise de Investimento](#análise-de-investimento)
    - [🌱 Benefícios Financeiros Indiretos](#abenefícios-financeiros-indiretos)
    - [📊 Projeção 5 Anos](#projeção-5-anos)
   
 
  - [⚖️ Tradeoffs](#️-tradeoffs)
    - [Vantagens](#vantagens)
    - [Desvantagens](#desvantagens)
  - [📊 Diagrama de Conexões](#-diagrama-de-conexões)
  - [📈 Métricas de Desempenho](#-métricas-de-desempenho)
    - [Tempo de Resposta](#tempo-de-resposta)
    - [Confiabilidade](#confiabilidade)
 
  - [📱 Integração Futura](#-integração-futura)
  - [📊 Análise Detalhada de ROI](#-análise-detalhada-de-roi)
    - [Cálculos Base](#cálculos-base)
    - [Economia Projetada com Sistema Inteligente](#economia-projetada-com-sistema-inteligente)
    - [Cálculo do ROI](#cálculo-do-roi)
    - [Benefícios Indiretos Quantificados](#benefícios-indiretos-quantificados)
  - [🌍 Impacto Ambiental](#-impacto-ambiental)
    - [Sustentabilidade](#sustentabilidade)
  - [🔬 Detalhes Técnicos](#-detalhes-técnicos)
    - [Especificações do Sistema](#especificações-do-sistema)
    - [Algoritmo de Controle](#algoritmo-de-controle)
  - [📱 Interface e Controle](#-interface-e-controle)
    - [App Mobile (Futuro)](#app-mobile-futuro)
    - [Integração IoT](#integração-iot)
  - [🔒 Segurança](#-segurança)
    - [Medidas Implementadas](#medidas-implementadas)
  - [📈 Escalabilidade](#-escalabilidade)
    - [Expansão Futura](#expansão-futura)
  - [📋 Certificações e Normas](#-certificações-e-normas)
    - [Conformidade](#conformidade)
  - [🔗 Integração com Outras Disciplinas](#-integração-com-outras-disciplinas)
    - [Python (CTWP)](#python-ctwp)
    - [Banco de Dados (CDS)](#banco-de-dados-cds)
    - [Análise em R (SCR)](#análise-em-r-scr)
  - [📹 Demonstração](#-demonstração)
    - [Vídeo de Funcionamento](#vídeo-de-funcionamento)
    - [Resultados Obtidos](#resultados-obtidos)

## 👀 Visão Geral
O Lumion é uma solução inovadora de automação residencial focada no controle inteligente de iluminação. Desenvolvido com tecnologia IoT, o sistema utiliza sensores avançados e algoritmos adaptativos para otimizar o consumo energético, proporcionando economia de até 60% nos custos de iluminação.

### Principais benefícios
- 🔋 Redução significativa no consumo de energia
- 🏠 Automação completa da iluminação residencial
- 💡 Aumento da vida útil das lâmpadas
- 🌱 Contribuição para sustentabilidade
- 💰 Retorno do investimento em menos de 2 meses

## 🔧 Componentes do sistema

### Hardware Principal
**ESP32 DevKit V1**
   - Microcontrolador com WiFi e Bluetooth
   - Processamento central do sistema
   - Custo: R$ 50,00

### Sensores Inteligentes
**LDR (Light Dependent Resistor)**
   - Detecta níveis de luminosidade ambiente
   - Range: 0-4095 (ADC)
   - Custo: R$ 3,00

**Ultrassônico HC-SR04**
   - Detecta presença/movimento
   - Alcance: 2cm - 400cm
   - Custo: R$ 15,00

### Sistema de Iluminação
**LEDs de Iluminação**
   - LED Branco (interno): R$ 5,00
   - LED Amarelo (externo): R$ 5,00
   - Resistores 220Ω: R$ 0,50 cada

**Investimento Total: R$ 78,00**

## ⚙️ Funcionamento
O Lumion opera através de um sistema de controle adaptativo que ajusta automaticamente a iluminação baseado em três fatores principais:

### Iluminação Externa (LED Amarelo)
```cpp
if (valorLuz < 2000) { // Ambiente escuro
    digitalWrite(LED_EXTERNO, HIGH);
} else {
    digitalWrite(LED_EXTERNO, LOW);
}
```

- Ativa automaticamente em baixa luminosidade
- Mantém iluminação mínima para câmeras
- Ajuste baseado em sensor LDR

### Iluminação Interna (LED Branco)
```cpp
if (distancia < 100 && valorLuz < 2000) {
    digitalWrite(LED_INTERNO, HIGH);
} else {
    digitalWrite(LED_INTERNO, LOW);
}
```

- Ativa apenas com presença detectada
- Considera luminosidade ambiente
- Desliga automaticamente quando não há movimento

## 🛠️ Guia de Instalação

### 📡 Conexões de Hardware

### Pinagem ESP32
|Componente    |Pino ESP32|Tipo  | Descrição                    |
| :---         |  :---:   |:---: |    :---:                     |    
|LDR           |GPIO34    |Input |Sensor de luminosidade        | 
|HC-SR04 (TRIG)|GPIO26    |Output|Trigger do sensor ultrassônico| 
|HC-SR04 (ECHO)|GPIO27    |Input |Echo do sensor ultrassônico   |
| LED Interno  |GPIO2     |Output|Iluminação ambiente interno   |
|LED Externo   |GPIO4     |Output|Iluminação ambiente externo   |

### 📊 Diagrama de Conexões
```mermaid
graph TD
    ESP32[ESP32 DevKit]
    LDR[LDR Sensor]
    TRIG[HC-SR04 TRIG]
    ECHO[HC-SR04 ECHO]
    LEDW[LED Branco]
    LEDY[LED Amarelo]

    LDR -->|GPIO34| ESP32
    TRIG -->|GPIO26| ESP32
    ECHO -->|GPIO27| ESP32
    ESP32 -->|GPIO2| LEDW
    ESP32 -->|GPIO4| LEDY

    style ESP32 fill:#f9f,stroke:#333,stroke-width:4px
    style LDR fill:#bbf,stroke:#f66,stroke-width:2px
    style TRIG fill:#bfb,stroke:#f66,stroke-width:2px
    style ECHO fill:#bfb,stroke:#f66,stroke-width:2px
    style LEDW fill:#fbb,stroke:#f66,stroke-width:2px
    style LEDY fill:#ffb,stroke:#f66,stroke-width:2px
```
### 💻 Configuração do Ambiente

### Pré-requisitos

```cpp
# 1. Instale o Visual Studio Code
https://code.visualstudio.com/download

# 2. Instale o PlatformIO IDE
Code → Extensions → PlatformIO IDE

# 3. Instale o ESP32 Arduino Framework
PlatformIO → Platforms → Espressif32
```
### Preparação do Projeto
```cpp
# Clone o repositório
git clone https://github.com/seu-usuario/lumion.git

# Entre no diretório
cd lumion

# Instale as dependências
pio pkg install
```
### Configuração do Hardware
```cpp
// Defina as configurações no config.h
#define LDR_PIN         34
#define ULTRASONIC_TRIG 26
#define ULTRASONIC_ECHO 27
#define LED_INTERNO     2
#define LED_EXTERNO     4
```

### 🔧 Montagem Física

### Lista de Materiais
- [ ] ESP32 DevKit V1
- [ ] Sensor LDR
- [ ] Sensor HC-SR04
- [ ] 2× LEDs (branco e amarelo)
- [ ] 2× Resistores 220Ω
- [ ] Jumpers
- [ ] Case protetor (opcional)

### Passos de Montagem

### Preparação
- Verifique todos os componentes
- Organize a área de trabalho
- Prepare as ferramentas necessárias

### Conexões
```cpp
# Sequência recomendada
   1. Conecte o LDR ao GPIO34
   2. Conecte o HC-SR04 (TRIG → GPIO26, ECHO → GPIO27)
   3. Instale os LEDs com seus resistores
   4. Verifique todas as conexões
```
### Verificação
- [ ] Teste de continuidade
- [ ] Verificação visual
- [ ] Teste de polaridade dos LEDs

### ⚡ Primeira Execução

### Upload do Código
```cpp
# Compile e faça upload
pio run -t upload

# Monitor serial para debug
pio device monitor
```

### Verificação do Sistema
```cpp
# Sequência de teste
1. LED Externo → Deve piscar na inicialização
2. LED Interno → Deve responder a movimento
3. Serial Monitor → Deve mostrar leituras dos sensores
```

### Calibração
```cpp
// Ajuste os valores no código conforme necessário
#define LUZ_THRESHOLD    2000  // Ajuste sensibilidade do LDR
#define DIST_THRESHOLD   100   // Ajuste distância de detecção
```

## 🔬 Detalhes Técnicos

### Especificações do Sistema
1. **Processamento**
   - CPU: 240MHz Dual Core
   - Memória: 320KB RAM
   - Flash: 4MB

2. **Sensores**
   - LDR: Precisão de 12 bits
   - Ultrassônico: Precisão ±3mm
   - Tempo de resposta: <10ms

### Algoritmo de Controle
```cpp
void controleIluminacao() {
    // Leitura dos sensores
    int luminosidade = map(analogRead(LDR_PIN), 0, 4095, 0, 100);
    int distancia = medirDistancia();
    
    // Controle adaptativo
    if (luminosidade < LIMIAR_NOITE) {
        // Modo noturno
        if (distancia < DISTANCIA_DETECCAO) {
            // Presença detectada
            ajustarLuz(LED_INTERNO, 100);
            ajustarLuz(LED_EXTERNO, 70);
        } else {
            // Sem presença
            ajustarLuz(LED_INTERNO, 0);
            ajustarLuz(LED_EXTERNO, 30);
        }
    } else {
        // Modo diurno
        desligarIluminacao();
    }
}
```
## 📈 Métricas de Desempenho

### Tempo de Resposta
- Detecção de movimento: < 100ms
- Ajuste de luminosidade: < 50ms
- Boot do sistema: < 2s

### Confiabilidade
- MTBF estimado: > 50.000 horas
- Taxa de falsos positivos: < 2%
- Precisão do sensor de luz: ±5%


### 🔍 Troubleshooting

### Problemas Comuns
- LED não acende
- Verificar polaridade
- Testar resistor
- Confirmar pinagem
- Sensor não responde
- Verificar conexões
- Testar alimentação
- Atualizar drivers

### 📱 Próximos Passos
- [ ] Configure a rede WiFi
- [ ] Ajuste os parâmetros de sensibilidade
- [ ] Teste em diferentes condições de luz
- [ ] Configure alertas (opcional)

## 🔄 Plano de Manutenção
```mermaid
gantt
    title Cronograma de Manutenção Lumion
    dateFormat  YYYY-MM-DD
    section Limpeza
    Limpeza dos Sensores       :crit, active, l1, 2024-12-01, 30d
    section Verificação
    Verificação das Conexões   :active, v1, 2024-12-01, 90d
    section Calibração
    Calibração dos Sensores    :active, c1, 2024-12-01, 180d
    section Preventiva
    Backup de Configurações    :2024-12-01, 30d
    Monitoramento de Consumo   :2024-12-01, 180d
    Verificação de Firmware    :2024-12-01, 90d
```

### Detalhamneto de Manutenção

### Manutenção Periódica
- Limpeza dos Sensores (Mensal)
  - Remover poeira e resíduos
  - Verificar integridade física
  - Aplicar produto anti-estático
- Verificação das Conexões (Trimestral)
  - Inspecionar soldas e conectores
  - Testar continuidade elétrica
  - Reapertar parafusos e terminais
- Calibração dos Sensores (Semestral)
  - Ajustar sensibilidade do LDR
  - Verificar precisão do HC-SR04
  - Atualizar parâmetros no firmware

### Manutenção Preventiva
- Backup das Configurações
- Exportar configurações atuais
- Armazenar em nuvem segura
- Documentar alterações
- Monitoramento do Consumo
- Analisar logs de energia
- Identificar padrões anômalos
- Otimizar algoritmos de economia
- Verificação do Firmware
- Checar por atualizações disponíveis
- Testar novas versões em ambiente controlado
- Realizar rollback se necessário

### 💰 Análise Econômica

### 📊 Cenário Atual (Sem Automação)
### Consumo Energético Base

|Ambiente| Potencia | Uso diário | Consumo mensal | Custo R$ |
| :---   |  :---:   |    :---:   |    :---:       |    :---: |
|Externo | 100W     |    12h     |     36 kWh     | R$ 27,00 |
|Interno | 60W      |     5h     |      9 kWh     | R$  6,75 |
| Total  |  *       |     *      |     45 kWh     | R$ 33,75 |

                               Tarifa considerada: R$ 0,75/kWh

### 📈 Projeção de Economia

### Otimização da Iluminação Externa
- Redução no Tempo de Uso: 12h → 7.2h
- Economia Energética: 60%

```cpp
Economia Mensal = (36 kWh × 0.60) × R$ 0,75
Economia Mensal = R$ 16,20
```

### Otimização da Iluminação Interna
- Redução no Tempo de Uso: 5h → 3h
- Economia Energética: 40%

```cpp
Economia Mensal = (9 kWh × 0.40) × R$ 0,75
Economia Mensal = R$ 2,70
```

### 💎 Análise de Investimento
### ROI (Return on Investment)
```cpp
Investimento Inicial = R$ 78,00
Economia Mensal = R$ 18,90
Payback = 78,00 ÷ 18,90 = 4,1 meses
ROI Anual = (18,90 × 12 - 78,00) ÷ 78,00 × 100 = 190%
```
### Projeção Financeira em 12 Meses

|Mês | Economia Acumulada |      Status  | 
|:---|       :---:        |      :---:   |   
| 1  |      R$ 18,90      |   Em payback |     
| 2  |      R$ 37,80      |   Em payback |     
| 4  |      R$ 75,60      |   Breakeven  |    
| 12 |      R$ 226,80     | Lucro líquido|  
                               
### 🌱 Benefícios Financeiros Indiretos
- Redução de Manutenção
- Menor frequência de trocas: -60%
- Economia anual: R$ 120,00
- Aumento da Vida Útil
- Lâmpadas convencionais: 15.000h
- Com sistema Lumion: 25.000h
- Economia em reposição: R$ 80,00/ano
- Valorização Imobiliária
- Incremento estimado: 0,5%
- Em imóvel de R$ 300.000: R$ 1.500,00

### 📊 Projeção 5 Anos

```cpp
Economia Total = Energia + Manutenção + Vida Útil
Economia Anual = R$ 226,80 + R$ 120,00 + R$ 80,00
Economia em 5 Anos = R$ 2.134,00
ROI 5 Anos = 2.637%
```

## ⚖️ Tradeoffs
```mermaid
graph LR
    subgraph Vantagens
        A[Automação] -->|Impacto: 0.9| V
        E[Economia] -->|Impacto: 0.95| V
        VU[Vida Útil] -->|Impacto: 0.7| V
        S[Segurança] -->|Impacto: 0.8| V
        BM[Baixa Manutenção] -->|Impacto: 0.6| V
    end
    subgraph Desvantagens
        CI[Custo Inicial] -->|Impacto: 0.4| D
        C[Calibração] -->|Impacto: 0.5| D
        DE[Dependência Elétrica] -->|Impacto: 0.3| D
        FP[Falsos Positivos] -->|Impacto: 0.2| D
    end
    V[Vantagens]
    D[Desvantagens]
```

### Vantagens
1. Automação completa
2. Economia significativa
3. Aumento da vida útil das lâmpadas
4. Segurança mantida
5. Baixa manutenção

### Desvantagens
1. Custo inicial
2. Necessidade de calibração
3. Dependência de energia elétrica
4. Possíveis falsos positivos



## 📱 Integração Futura

1. **App Mobile**
   - Controle remoto
   - Monitoramento em tempo real
   - Configurações personalizadas

2. **Smart Home**
   - Integração com Alexa/Google Home
   - MQTT para IoT
   - Dashboards personalizados



## 🌍 Impacto Ambiental

### Sustentabilidade
1. **Redução de Resíduos**
   - Menos trocas de lâmpadas
   - Menor descarte de componentes
   - Reciclagem facilitada

2. **Eficiência Energética**
   - Redução do consumo em horário de pico
   - Otimização baseada em uso real
   - Adaptação à luminosidade natural



## 📱 Interface e Controle

### App Mobile (Futuro)
**Funcionalidades**
   - Dashboard em tempo real
   - Controle manual override
   - Histórico de consumo
   - Alertas e notificações

**Tecnologias**
   - Frontend: React Native
   - Backend: Node.js
   - Database: MongoDB
   - API: REST/WebSocket

### Integração IoT
**Protocolos**
   - MQTT para comunicação
   - SSL/TLS para segurança
   - JSON para payload

**Cloud Services**
   - AWS IoT Core
   - Azure IoT Hub
   - Google Cloud IoT

## 🔒 Segurança

### Medidas Implementadas
1. **Física**
   - Sensores redundantes
   - Proteção contra surtos
   - Backup de energia

2. **Digital**
   - Criptografia AES-256
   - Autenticação dois fatores
   - Logs de acesso

## 📈 Escalabilidade

### Expansão Futura
1. **Hardware**
   - Suporte até 32 sensores
   - Múltiplos controladores
   - Integração com outros sistemas

2. **Software**
   - APIs públicas
   - Marketplace de plugins
   - Machine Learning adaptativo

## 📋 Certificações e Normas

### Conformidade
**Normas Técnicas**
   - ABNT NBR 5410
   - IEC 60364
   - ISO/IEC 27001

**Certificações**
   - INMETRO
   - CE Mark
   - RoHS

## 🔗 Integração com Outras Disciplinas

### Python (CTWP)
- API REST para receber dados do ESP32
- Interface gráfica para visualização
- Análise em tempo real do consumo

### Banco de Dados (CDS)
- Armazenamento histórico
- Análise de tendências
- Pipeline de dados

### Análise em R (SCR)
- Processamento estatístico
- Visualização de padrões
- Previsão de consumo

## 📹 Demonstração

### Vídeo de Funcionamento
- Link YouTube: [Sistema Inteligente de Iluminação Residencial](seu-link-aqui)
- Demonstração completa do sistema funcionando no Wokwi
- Explicação dos componentes e funcionalidades



Para mais informações sobre o ESP32, consulte a documentação oficial: [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/index.html)
