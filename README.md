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

## Melhorias da FASE 1

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

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

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


