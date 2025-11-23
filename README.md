# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 1</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 2</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 3</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 4</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 5</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Tutor</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Coordenador</a>


## 📜 Descrição

### 🏗️ Arquitetura e Estrutura do Projeto

Para atender ao objetivo de consolidar todas as funcionalidades desenvolvidas ao longo das Fases 1 a 6 em um único sistema integrado, optamos por construir uma aplicação web completa, com um painel de navegação onde o usuário pode acessar cada uma das funções implementadas nos meses anteriores — como cálculo de área, consultas de sensores IoT, análises preditivas, visão computacional e integração com AWS.

### 🔧 Tecnologias e Estratégia de Implementação

A infraestrutura do sistema foi construída utilizando Docker, de forma que todo o ambiente (backend, banco de dados e dependências) pudesse ser executado com apenas um comando, garantindo:

- Reprodutibilidade

- Facilidade de instalação

- Padronização entre ambientes

- Isolamento das dependências

Dentro do ambiente Docker, utilizamos:

<b>🐍 Backend — Python + Flask</b>

O backend foi desenvolvido em Python, utilizando o microframework Flask, por sua leveza, simplicidade e excelente integração com APIs, dashboards e serviços externos (IoT, R, YOLO, AWS etc.).
O Flask também permite estruturar o projeto em blueprints e trabalhar com HTML (Jinja2), REST APIs, autenticação e dashboards em uma mesma aplicação.

<b>🗄️ Banco de Dados — MySQL</b>

Inicialmente, o plano era utilizar Oracle Database XE, porém durante os testes o Oracle apresentou:

- dificuldades na configuração de usuários e permissões,

- lentidão no processo de inicialização,

- necessidade de scripts adicionais para habilitar criação de schemas,

- baixa compatibilidade com ferramentas como PyCharm e SQLAlchemy.

Por esse motivo, migramos para o MySQL, que ofereceu:

- configuração extremamente simples no Docker,

- integração perfeita com o SQLAlchemy,

- criação rápida das tabelas de forma automática,

- codificação UTF-8 já habilitada,

- maior velocidade e praticidade para desenvolvimento acadêmico.

Mesmo com a troca do banco, mantivemos os princípios de modelagem relacional definidos na Fase 2, adaptando apenas os tipos e restrições das tabelas.

### 📁 Estrutura Integrada

O resultado é um sistema completo onde:

- o Flask gerencia as rotas e páginas do painel,

- o MySQL armazena todos os dados de culturas, produtos, sensores e cálculos,

- o Docker Compose orquestra os serviços com um único comando,

- e cada módulo desenvolvido nas fases anteriores pode ser executado diretamente pelo usuário através do painel unificado.

# FASE 1

O sistema de cálculo para área plantada sofreu significativas alterações em decorrência do conhecimento adquirido de banco de dados nas fases posteriores.  
A principal mudança foi que os arrays e *dicts* estáticos dentro do código passam a ser tabelas SQL, permitindo assim que o sistema se torne dinâmico, com a possibilidade de o usuário cadastrar novas culturas.

As tabelas são criadas e populadas na primeira inicialização do Docker (`docker-compose up --build`) em ordem crescente de cada prefixo dos arquivos `.sql` em `src/app/db/migrations`.

O Painel está acessível através do navegador, onde 

---

### 🧩 Antes
```python
cultures = ['milho', 'laranja']
products = {'milho': 'Fosfato Monoamônico', 'laranja': 'Diclorofenoxiacético'}
productsQtd = {'Fosfato Monoamônico': 5, 'Diclorofenoxiacético': 0.15}
formats = {'milho': 'retangulo', 'laranja': 'triangulo'}
streets = {'milho': 1, 'laranja': 2}
spaceBetweenStreets = 1
```
# Depois (DLL)
```sql
-- src/app/db/migrations/010_schema.sql

CREATE TABLE format_type (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(30) NOT NULL UNIQUE,
  description VARCHAR(120)
) ENGINE=InnoDB;

CREATE TABLE product (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL UNIQUE,
  dosage_per_m2 DECIMAL(18,4) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE culture (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(60) NOT NULL UNIQUE,
  product_id INT NOT NULL,
  format_id INT NOT NULL,
  street_size_m DECIMAL(18,4) NOT NULL,
  CONSTRAINT fk_culture_product
    FOREIGN KEY (product_id) REFERENCES product(id)
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_culture_format
    FOREIGN KEY (format_id) REFERENCES format_type(id)
      ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE system_param (
  `key` VARCHAR(80) PRIMARY KEY,
  value_str VARCHAR(4000),
  value_num DECIMAL(18,4)
) ENGINE=InnoDB;

-- src/app/db/migrations/090_seed.sql

```
---

## 🧩 Regras de Negócio e Relacionamentos do Modelo

### 1. TABELA FORMAT_TYPE

- Define os formatos geométricos possíveis para o cálculo da área de plantio (ex.: retângulo, triângulo).

- Cada formato é identificado unicamente por CODE.

### Regras:

- Um formato pode estar associado a várias culturas.
➜ Relação 1:N entre FORMAT_TYPE e CULTURE.

- Uma cultura pode ter apenas um formato.

---

### 2. TABELA PRODUCT

Representa o produto químico (fertilizante, herbicida etc.) utilizado em determinada cultura.

A coluna DOSAGE_PER_M2 define a quantidade aplicada por metro quadrado.

### Regras:

- Um produto pode ser usado por múltiplas culturas diferentes.
➜ Relação 1:N entre PRODUCT e CULTURE.

- Cada cultura está vinculada a apenas um produto.

---

### 3. TABELA CULTURE

- Define as culturas agrícolas (ex.: milho, laranja).

- Cada registro associa uma cultura a um produto e a um formato.

### Regras:

- Cada cultura possui:

- Um único produto (PRODUCT_ID → PRODUCT.ID);
  - Um único formato geométrico (FORMAT_ID → FORMAT_TYPE.ID);
  - Um valor de largura de rua (STREET_SIZE_M) que influencia o cálculo da área útil.
  - Uma mesma cultura não pode se repetir (coluna NAME é única).
  - As exclusões em cascata devem ser evitadas — recomenda-se controle lógico de deleção (ex.: flag “ativo”).

---

### 4. TABELA SYSTEM_PARAM

- Armazena parâmetros globais do sistema, como o espaçamento padrão entre ruas.

## 🔗 Resumo dos Relacionamentos
| Entidade Origem | Tipo de Relação | Entidade Destino | Cardinalidade | Regra |
|------------------|-----------------|------------------|----------------|-------|
| FORMAT_TYPE | 1 → N | CULTURE | Um formato pode ser usado por várias culturas | FK: `CULTURE.FORMAT_ID` |
| PRODUCT | 1 → N | CULTURE | Um produto pode ser usado em várias culturas | FK: `CULTURE.PRODUCT_ID` |
| SYSTEM_PARAM | Isolada | — | Tabela de parâmetros globais | Chave primária `KEY` |

### Regras:

- Cada parâmetro é identificado unicamente pela coluna KEY.

- Pode armazenar valores numéricos (VALUE_NUM) e textuais (VALUE_STR).

- Exemplo inicial:
('SPACE_BETWEEN_STREETS_M', 1) define 1 metro entre ruas como padrão global.

## 🧠 Exemplos de cenário prático

- “Milho” utiliza o formato retângulo e o produto Fosfato Monoamônico.

- “Laranja” utiliza o formato triângulo e o produto Diclorofenoxiacético.

- Ambos podem coexistir, e no futuro novas culturas podem ser inseridas sem alterar o código, apenas adicionando novos registros.

---

# FASE 2

## 🎯 Objetivo

Desenvolver um **Modelo Entidade-Relacionamento (MER)** e um **Diagrama Entidade-Relacionamento (DER)** que representem um sistema capaz de armazenar e processar dados de sensores utilizados em plantações, otimizando o uso de recursos como água e nutrientes.

## 🧠 Contexto do Problema

O produtor rural utiliza três tipos de sensores:

- **S1**: Sensor de Umidade
- **S2**: Sensor de pH
- **S3**: Sensor de Nutrientes (Fósforo e Potássio - NPK)

Esses sensores coletam dados em tempo real, enviando-os para um sistema central que:
- Processa os dados,
- Sugere ajustes na irrigação e aplicação de nutrientes,
- Utiliza dados históricos para prever necessidades futuras.

---

## 📝 Requisitos da Modelagem

### 1. Informações Relevantes
Abaixo, listamos algumas informações que o sistema deve permitir consultar:

- Quantidade total de água aplicada por mês
  - Dados: `data_hora`, `quantidade_agua`
- Variação do pH ao longo do ano
  - Dados: `data_hora`, `valor_ph`
- Níveis de fósforo e potássio ao longo do tempo
  - Dados: `data_hora`, `valor_fosforo`, `valor_potassio`

---

### 2. Entidades e Atributos (MER)

#### 🌾 Cultivo
- `id_cultivo` (PK)
- `nome_cultura` (varchar)
- `localizacao` (varchar)

#### 🌡️ Sensor
- `id_sensor` (PK)
- `tipo_sensor` (varchar) — ex: Umidade, pH, Nutriente
- `descricao` (varchar)

#### 📊 Leitura
- `id_leitura` (PK)
- `id_sensor` (FK)
- `id_cultivo` (FK)
- `data_hora` (datetime)
- `valor_umidade` (double)
- `valor_ph` (double)
- `valor_fosforo` (double)
- `valor_potassio` (double)

#### 💧 Irrigacao
- `id_irrigacao` (PK)
- `id_cultivo` (FK)
- `data_hora` (datetime)
- `quantidade_agua` (double)

---

### 3. Cardinalidades

- Um **Cultivo** pode estar relacionado a **muitas Leituras** (1:N)
- Um **Sensor** pode gerar **muitas Leituras** (1:N)
- Um **Cultivo** pode ter **muitas Irrigações** (1:N)

---

### 4. Relacionamentos

- `Cultivo (1) --- (N) Leitura`
- `Sensor (1) --- (N) Leitura`
- `Cultivo (1) --- (N) Irrigacao`

---

### 5. Tipos de Dados

| Atributo             | Tipo de Dado |
|----------------------|--------------|
| id_cultivo           | int (PK)     |
| nome_cultura         | varchar(100) |
| localizacao          | varchar(100) |
| id_sensor            | int (PK)     |
| tipo_sensor          | varchar(50)  |
| descricao            | varchar(255) |
| id_leitura           | int (PK)     |
| data_hora            | datetime     |
| valor_umidade        | double       |
| valor_ph             | double       |
| valor_fosforo        | double       |
| valor_potassio       | double       |
| id_irrigacao         | int (PK)     |
| quantidade_agua      | double       |

---

### Os arquivos gerados no Oracle Data Modeler estão disponíveis em: 
[📁 Modelagem Lógica do Banco de Dados](src/Modelagem%20Lógica%20do%20Banco%20de%20dados)

---

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

---

# FASE 3 - IOT e Automação Inteligente
## 🎯 Objetivo da Fase

Nesta etapa, simulamos um sistema IoT agrícola capaz de monitorar condições do solo (umidade, nutrientes e pH) e controlar automaticamente uma bomba de irrigação.
O foco é reproduzir, via Wokwi e ESP32, o comportamento de sensores reais utilizados no campo.

Também implementamos uma camada Python que recebe, armazena e manipula as leituras usando banco de dados SQL.

---
## 🔌 1. Sistema de Sensores – ESP32 (Wokwi)
### 🧱 Componentes Simulados

Como alguns sensores reais não existem na versão gratuita do Wokwi, foram utilizados equivalentes:

## Mapeamento dos Sensores e Componentes no Wokwi

| Sensor Real                  | Sensor/Componente no Wokwi     | Tipo     | Função                                   |
|------------------------------|---------------------------------|----------|-------------------------------------------|
| Sensor de Fósforo (P)        | Push Button (botão azul)        | Digital  | 0/1 (ausente/presente)                    |
| Sensor de Potássio (K)       | Push Button (botão verde)       | Digital  | 0/1                                       |
| Sensor de pH                 | LDR                             | Analógico| Varia conforme luz, simulando pH          |
| Sensor de Umidade do Solo    | DHT22                           | Digital  | Percentual de umidade                     |
| Atuador (Bomba de Irrigação) | Relé + LED embutido             | Digital  | Liga/desliga a irrigação                  |

### 📡 Funcionamento da Lógica

O ESP32:

- Lê todos os sensores em tempo real
- Converte as leituras brutas
- Aplique lógica automática:

<b>Regras Implementadas</b>
- Se umidade < 40% → bomba ON
- Se pH fora de 6.0–7.5 → bomba ON
- Se Fósforo E Potássio estiverem ausentes → bomba OFF
- Caso contrário → bomba segue último estado

### 🧩 Circuito Wokwi
O circuito completo encontra-se no repositório:

👉 /src/Fase 3 - IOT/

Inclui:
- main.cpp
- diagram.json
- platformio.ini
- print do circuito do arquivo: 
```bash
 /src/Fase 3 - IOT/wokwi-smart-irrigation-control.png
```

---

## 🗄️ 2. Armazenamento SQL com Python
### 🔧 Estrutura

Implementado em:
```bash
/src/app/services/iot_service.py
/src/app/db/models/iot_reading.py
/src/app/routes/api.py
```

Cada nova leitura é salva na tabela:

### Tabela iot_reading

## Estrutura da Tabela de Dados dos Sensores

| Campo       | Tipo      | Descrição                               |
|-------------|-----------|-------------------------------------------|
| id          | INT       | Identificador único do registro           |
| timestamp   | DATETIME  | Data e hora da leitura                    |
| humidity    | DECIMAL   | Umidade do solo (em %)                    |
| ph          | DECIMAL   | Valor de pH                               |
| phosphorus  | BOOLEAN   | Presença/ausência de fósforo (0/1)        |
| potassium   | BOOLEAN   | Presença/ausência de potássio (0/1)       |
| pump_on     | BOOLEAN   | Estado da bomba de irrigação (ligada? 0/1)|


O sistema:

- Simula leituras contínuas
- Armazena em MySQL
- Oferece CRUD básico
- Expõe API REST para integração
---
## 🌐 3. Rota Web (Flask)

<b>A página /dashboard/fase-3/iot permite:</b>
- Gerar leituras simuladas (botão “Gerar Leitura”)
- Exibir lista atualizada de medições
- Atualizar tabela via fetch AJAX

---
# 📊 FASE 4 – Dashboard com Data Science

## 🎯 Objetivo
Integrar Data Science ao sistema IoT:
- Processar dados históricos
- Calcular estatísticas
- Gerar gráficos
- Prever comportamento futuro (pequena regressão linear)

---

## 🧠 1. Processamento e Estatísticas

O controller da aplicação:
```bash
/src/app/controller/dashboard_controller.py
```

Gera:

### Estatísticas calculadas

- Umidade (máx, mín, média, desvio)

- pH (máx, mín, média, desvio)

- Percentual de fósforo presente

- Percentual de potássio presente

- Percentual da bomba ligada

Essas estatísticas são estruturadas como JSON:

```json
{
  "humidity": { "min": 24.5, "mean": 57.2, "max": 80.0, "std": 11.23 },
  "ph": { "min": 6.3, "mean": 7.25, "max": 8.0, "std": 0.39 },
  "nutrients": {
    "phosphorus_ok": 34.78,
    "potassium_ok": 29.34
  },
  "pump_on": 18.47
}

```

---

## 📈 2. Gráficos Automáticos
Gerados em:

```
/src/app/dashboard_phase4/analytics.py
```

Renderizados em:
```
/src/app/dashboard_phase4/charts.py
```

Gráficos salvos em:

```bash
/assets/plots/
```

Tipos de gráficos:
- Evolução da umidade
- Evolução do pH
- Frequência da bomba ligada
- Previsão de pH usando regressão linear

___

## 🖥️ 3. Interface Web da Dashboard

rota ``` /dashboard/fase4 ```

template 
``` /src/app/view/pages/dashboard-iot.html ```

Funcionalidades:
- Três tabelas lado a lado com estatísticas (umidade, pH, nutrientes)

- Galeria com os gráficos gerados

- Gráfico final com previsão ML

- Layout limpo e responsivo

---

# ✅ Conclusão das Fases 3 e 4

<b>✔ Integrado ao banco MySQL

✔ APIs funcionando

✔ Simulação IoT realista

✔ Dashboard estatística e preditiva integrada ao Flask

✔ Gráficos automáticos gerados no backend

✔ Tudo unificado dentro da estrutura do projeto final
</b>

---

# 🧪 Fase 5 — Machine Learning + Comparativo AWS

A Fase 5 consolida duas frentes principais do projeto:

1. <b>Aplicação de Machine Learning</b> para análise preditiva dos dados dos sensores.

2. <b>Comparação de custos na AWS</b> para definir a melhor opção de infraestrutura.

Essa fase inclui processamento dos dados, treinamento de modelos, avaliação das métricas, criação de gráficos explicativos e análise financeira usando a AWS Pricing Calculator.

## 📊 1. Machine Learning

Nesta etapa, foi construído um pipeline de Machine Learning utilizando o dataset crop_yield.csv, que contém dados agrícolas históricos com variáveis que influenciam diretamente a produtividade das colheitas.

### 📁 Dataset

O arquivo utilizado foi:

```bash
crop_yield.csv
```

### 📌 Colunas do dataset

As colunas utilizadas no treinamento do modelo foram:

- <b>Crop</b> → Tipo de cultura (ex.: arroz, milho, trigo)

- <b>Rainfall</b> → Pluviosidade anual (mm)

- <b>Temperature</b> → Temperatura média anual (°C)

- <b>Pesticide</b> → Quantidade de pesticidas utilizados (kg/ha)

- <b>Fertilizer</b> → Quantidade de fertilizantes (kg/ha)

- <b>Yield</b> → Produção agrícola (ton/ha) (variável alvo)

🔍 <i>Essas são as colunas clássicas do dataset de produtividade agrícola normalmente usado como base acadêmica para regressão.</i>

## 🎯 Objetivo

O objetivo do ML foi prever a produtividade agrícola (Yield) com base nas condições ambientais e insumos utilizados.

### 🔍 Modelos Avaliados

Nós treinamos e comparamos:

- <b>Linear Regression</b>

- <b>Random Forest</b>

- <b>KNN</b>

- <b>SVR</b>

Cada modelo foi avaliado por:

<b>MAE</b>

<b>MSE</b>

<b>RMSE</b>

<b>R²</b>

Esses resultados estão todos registrados em:

```bash
assets/plots/fase5/results.json
```

## 📈 Gráficos produzidos

Distribuição das features

- Boxplots

- Correlação

- Clusters K-Means

- Gráfico de comparação dos modelos

- Todos os PNG estão em:

```bash
assets/plots/fase5/
```


E são exibidos automaticamente no dashboard.

## 🖥️ 2. Comparativo de Custos — AWS

A segunda parte da Fase 5 envolveu uma análise de custos utilizando a
AWS Pricing Calculator, comparando cenários de execução da mesma instância EC2 nas regiões:

- São Paulo (BR)

- Norte da Virgínia (EUA)

📌 Configurações da Máquina Avaliada

- Linux

- 2 vCPUs

- 1 GiB RAM

- Até 5 Gbps de rede

- 50 GB de armazenamento

- 100% On-Demand

- Sem instâncias reservadas

### 💵 Comparação de Custos Mensais
## Comparação de Custos — AWS

| Região             | Compute SP | EC2 Instance SP | On-Demand | Spot |
|--------------------|-------------|------------------|-----------|-------|
| São Paulo          | 2.41        | 2.12             | 4.89      | 0.59  |
| Virgínia do Norte  | 1.53        | 1.31             | 3.07      | 1.59  |


## 🧾 Conclusão do Estudo

A opção mais barata encontrada foi:

- ➡️ EC2 Spot – Região São Paulo
- 💰 US$ 0.59 / mês

Apesar de Spot apresentar risco de interrupção, para um MVP o custo extremamente reduzido compensa a limitação, considerando:

- Não há requisito explícito de alta disponibilidade nesta fase

- O armazenamento deve permanecer dentro do Brasil (restrições legais)

- A latência local é menor

- O custo é significativamente inferior ao de outras regiões

### 📎 Documentos da Calculadora AWS

Os PDFs gerados na AWS Pricing Calculator estão disponíveis em:

[Comparativo AWS](src/app/assets/documents)

Links diretos:

[EC2 – North Virginia](src/app/assets/documents/ec2 - north virginia.pdf)

[EC2 – São Paulo](assets/documents/ec2 - sp.pdf)


## 🧭 Resultado Final da Fase 5

- ✔ Pipeline completo de Machine Learning
- ✔ Métricas de todos os modelos em JSON
- ✔ Gráficos gerados automaticamente
- ✔ Dashboard dedicado à Fase 5
- ✔ Comparativo técnico e financeiro entre regiões AWS
- ✔ PDFs anexos da AWS Calculator
- ✔ Recomendação final para arquitetura inicial da solução



---

## 🔧 Como executar o código

No terminal digite os seguintes comandos
```bash
cd src
docker-compose up --build
```
O docker irá montar as imagens do sistema junto das tabelas do MySql que substituem os arrays do código.
O sistema estará acessível pela URL: http://localhost:5000/dashboard


## 🗃 Histórico de lançamentos

* 0.5.0 - XX/XX/2024
    * 
* 0.4.0 - XX/XX/2024
    * 
* 0.3.0 - XX/XX/2024
    * 
* 0.2.0 - XX/XX/2024
    * 
* 0.1.0 - XX/XX/2024
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


