### Português [(English version here)](README.md)

# Pipeline de análise de e-commerce

[![UV](https://img.shields.io/badge/uv-261231?logo=UV&logoColor=de5fea)](https://github.com/astral-sh/uv)
[![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter%20Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-6599c3?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Pandas](https://img.shields.io/badge/-Pandas-130654?&logo=pandas)](https://pandas.pydata.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-667566?logo=sqlalchemy&logoColor=d72407)](https://www.sqlalchemy.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)

<p align="center">
  <img src="img\ecommerce.png" alt="Imagem de capa do repositório">
</p>

## Visão geral do projeto

Um projeto simples desenvolvido para criar um pipeline para coleta de dados, configuração do banco de dados, analisar e visualizar dados de varejo.  
**Objetivo:** Simular uma tarefa do mundo real para melhorar minhas habilidades de engenharia de dados.
<br>

## Fontes de dados

- **E-Commerce Data**: Disponível [no Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data).
- Também está ena [pasta `data`](data) desse repositório, em formato ZIP.
<br>

## Recursos e componentes

### 1. Coleta e limpeza de dados

- Puxar dados de vendas do dataset do Kaggle (disponível publicamente no link [acima](#data-sources))
- Usar [Jupyter Notebooks](notebooks) para explorar e analisar de maneira inicial os dados
- Limpar os dados — lidar com valores ausentes, remover duplicatas, corrigir tipos de dados etc.
- Documentar os problemas de encontrados

### 2. Configuração do banco de dados

- Configurar um banco de dados PostgreSQL no Docker
- Projetar e criar tabelas apropriadas e com indexação adequada
- Carregar os dados limpos no banco de dados

### 3. Consultas analíticas

- Consultas SQL para responder algumas perguntas de negócios:
    - Tendências mensais de receita 
    - Os 15 produtos mais vendidos 
    - Valor médio do pedido pelo país do cliente 
    - Segmentação do cliente por comportamento de compra (análise RFM) 

### 4. Dashboard simples

- Painel básico usando o streamlit
- visualizações simples com os resultados das consultas acima

### 5. Documentação

- README com instruções de configuração
- Comentários no código, quando necessário
- Breve resumo dos insights descobertos

## Tecnologias usadas

- **Python**: Limpeza de dados, processamento e conexão de banco de dados (`pandas`,` sqlalchemy`)
- **Jupyter Notebooks**: EDA e teste de tratamento de dados
- **PostgreSQL**: Armazenamento de dados
- **Streamlit**: Visualização de dados
- **Docker**: Conteinerização de todas as dependências do projeto
<br>

## Como rodar

### Pré-requisitos
Certifique-se de que tenha os seguintes componentes instalados: <br>
- [Docker](https://docs.docker.com/get-started/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
<br>

### Executando o projeto
1. **Clone o repositório**
   ```sh
   git clone https://github.com/sch-paulo/ecommerce-analytics-pipeline.git
   cd ecommerce-analytics-pipeline
   ```

2. **Configure um arquivo para as variáveis de ambiente**
- Na pasta raiz do projeto, crie um arquivo `.env` contendo as seguintes credenciais:
    - `POSTGRES_DB`=*nome_db*
    - `POSTGRES_USER`=*seu_usuario*
    - `POSTGRES_PASSWORD`=*sua_senha*
- Deixei um arquivo de exemplo para que seja possível verificar a sua estrutura (você ainda precisará renomeá-lo caso queira utilizá-lo).

3. **Inicie a aplicação pelo Docker Compose**
    ```sh
    docker-compose up --build
    ```

    - Uma parte chata desse processo é que o contêiner do dashboard precisa esperar o serviço de ETL finalizar o processo por completo e, por siso, pode levar alguns minutos para que todas as linhas sejam inseridas no banco de dados.

4. **Acesse a aplicação**
- Depois de executada, acesse-a através do link http://localhost:8501 (essa é a porta que usei para o dashboard no `docker-compose.yml`, se você alterá-la, vai precisar mudar no link também).

5. **Visualização**
- O dashboard apresenta alguns visuais separados por guias, que representam cada uma das consultas.

6. **Acessando os dados**
- No SGBD que estiver usando (DBeaver, pgAdmin, etc.), cria uma conexão usando as seguintes credenciais:
    - **Host name:**  `localhost` (para acessos dentro do contêiner, use `postgres`) <br> 
    - **Port:** `5433` (preste a atenção aqui, pois não é a mesma porta usada pelo contêiner)<br> 
- A partir daqui, use as mesmas credenciais que inseriu no arquivo `.env`.
    - **Maintenance database:** `nome_db` <br> 
    - **Username:** `seu_usuario` <br> 
    - **Password:** `sua_senha`
<br>

## Resultados e Insights
### 1. Tendências mensais de receita <br /> 
O período de dezembro de 2010 a dezembro de 2011 mostrou uma volatilidade moderada. A receita atingiu o pico em novembro de 2011 a $1.456.145,80, impulsionado pelo maior crescimento mensal de 49,34% em setembro e um forte aumento de 36,17% em novembro. Falando sobre meses ruins, janeiro (-25,21%) e abril de 2011 (-27,81%) tiveram o declínio mais significativo do período.

### 2. Top 15 produtos mais vendidos <br /> 
Com mais de \$164.000 em receita, o produto *REGENCY CAKESTAND 3 TIER* é o líder claro no ranking de mais vendidos. Concluindo o pódio estão *PARTY BUNTING*, com mais de \$98.000, e *WHITE HANGING HEART T-LIGHT HOLDER*, com aproximadamente \$97.800 em receita. A diversidade de produtos entre os 15 primeiros mostra uma variedade de itens que geram receita, de suprimentos de festas a itens de decoração.

### 3. Valor médio de pedido por país <br /> 
Embora o Reino Unido tenha um valor médio de ordem de \$347,72 (não sendo o mais alto), é o país que gera mais receita, com um total de \$8 milhões, representando impressionantes 84,3% da receita total. Por outro lado, a Holanda possui o maior valor de ordem média de \$2.818,43, mas sua receita total inferior a \$285.000 representa apenas 2,9% do total, indicando um volume de ordem inferior, mas um bilhete médio muito alto. Dos 37 países com pedidos, apenas 18 deles representam pelo menos mais de 0,1% da receita (mais de \$10.000).

### 4. Segmentação do cliente <br /> 
Para esta análise RFM, dividimos cada métrica (recência dos dias desde a última compra, frequência de compras e valor monetário total gasto) em 5 quintis, atribuindo pontuações de 1 a 5 para cada um, onde 5 representa o melhor desempenho. Para a Recência, pontuações mais altas foram concedidas a clientes com menos dias desde a última compra. Para frequência e valor monetário, pontuações mais altas foram atribuídas a clientes com maior frequência e gastos mais altos. A soma dessas três pontuações foi usada para categorizar os clientes em segmentos distintos.

**Segmentação e distribuição dos clientes**:
| Classificação             | % dos clientes | Total de clientes | Recência média (dias) | Frequência média | Valor monetário médio |
|---------------------|----------------|-----------------|---------------------|----------------|---------------------|
| Campeões           | 21.6%          | 945             | 12.4                | 14.1           | $6,215.23           |
| Clientes fiéis     | 17.3%          | 758             | 42.8                | 4.6            | $1,403.79           |
| Potenciais leais | 22.6%          | 989             | 77.2                | 2.5            | $706.68             |
| Em risco             | 17.0%          | 742             | 104.5               | 1.7            | $391.71             |
| Perdidos                | 21.5%          | 938             | 221.8               | 1.2            | $203.05             |


- **Campeões**: Estes são os melhores clientes. Com uma recência média de apenas 12 dias, uma alta frequência de mais de 14 compras e um valor monetário médio de mais de \$6.000, eles são os clientes mais recentes, mais frequentes e mais altos. Eles são a base dos negócios e merecem atenção especial para retenção e recompensas.

- **Loyal Customers**: Customers who buy regularly and spend a good amount. With an average recency of 43 days, a frequency of 4.6 purchases, and an average spend of $1,403, they are valuable customers who respond well to personalized offers and loyalty programs.
- **Clientes fiéis**: Clientes que compram regularmente e gastam uma boa quantia. Com uma recência média de 43 dias, uma frequência de 4,6 compras e um gasto médio de \$1.403, são clientes valiosos que respondem bem a ofertas personalizadas e programas de fidelidade.

- **Potenciais leais**: Esses clientes compraram recentemente, mas ainda não com a mesma frequência ou valor que os clientes fiéis. Com uma recência média de 77 dias, 2,5 compras e um gasto médio de \$707, eles têm um bom potencial para se tornarem clientes fiéis com o envolvimento certo, como campanhas para incentivar as compras repetidas.

- **At Risk**: Customers who have not purchased in a while but have had a good history. With an average recency of 104 days, low frequency (1.7 purchase), and an average monetary value of $392, they need re-engagement campaigns to prevent them from becoming “Lost”.
- **Em risco**: Os clientes que não compraram há algum tempo, mas tiveram um bom histórico. Com uma recência média de 104 dias, baixa frequência (1,7 compra) e um valor monetário médio de \$392, eles precisam de campanhas de reengajamento para impedir que se tornem clientes perdidos.

- **Perdidos**: Eles representam uma parte significativa da base de clientes que não comprou há muito tempo. Com uma recência média de 222 dias, frequência muito baixa (1,2 compra) e um gasto médio de apenas \$203, a estratégia para esse grupo pode ser tentar reativá-los com ofertas muito agressivas ou apenas focar os esforços em outros clientes mais lucrativos.
<br>

## Estrutura do projeto
```graphql
ecommerce-analytics-pipeline/
├── app/                     # Dashboard
│   ├── Dockerfile
│   ├── dashboard.py
│   └── requirements.txt
├── config/                  # Arquivos de configuração
│   └── country_map.py
├── data/                    # Dados de entrada brutos
│   ├── data.csv
│   └── ecommerce-data.zip
├── notebooks/               # Notebooks Jupyter para EDA e limpeza
│   ├── 01_data_exploration.ipynb
│   └── 02_data_cleaning.ipynb
├── schema/                  # Definições de esquema do banco de dados
│   └── models.py
├── scripts/                 # Consultas SQL para análises
│   ├── 01_monthly_revenue_trends.sql
│   ├── 02_top_best_selling.sql
│   ├── 03_average_order_by_country.sql
│   └── 04_customer_segmentation.sql
├── src/                     # Scripts principais de ETL
│   ├── Dockerfile
│   ├── clean_data.py
│   ├── database.py
│   ├── load_to_db.py
│   └── requirements.txt
├── .env                     # Arquivo de variáveis de ambiente
├── README.md                # Documentação do projeto (versão em inglês)
├── README-pt-br.md          # Documentação do projeto (versão em português)
├── docker-compose.yml       # Orquestração de contêineres
└── requirements_project.txt # Dependências de todo o projeto
```