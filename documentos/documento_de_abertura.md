# Documento de Abertura do Projeto

**Projeto:** Ecossistema de Dados — Amplo Varejo S.A.  
**Empresa:** Amplo Varejo S.A.  
**Tipo:** Projeto de Engenharia e Análise de Dados  
**Natureza:** Projeto simulado para portfólio  
**Área:** Dados, Business Intelligence e Analytics  
**Tecnologias principais:** Python, SQL, ETL, Data Warehouse e Power BI  

---

## 1. Contexto da Empresa

### 1.1 Sobre a empresa
A Amplo Varejo S.A. é uma empresa fictícia criada para representar, de forma realista, o ambiente operacional de uma grande organização do setor varejista.

A empresa atua no varejo multicategoria, comercializando produtos por meio de uma rede de lojas físicas distribuídas pelas cinco regiões brasileiras:
- Sudeste;
- Sul;
- Nordeste;
- Centro-Oeste;
- Norte.

A operação da empresa envolve diferentes áreas e entidades de negócio, incluindo clientes, vendedores, produtos, categorias, lojas, regiões, estoque, pedidos, vendas e metas comerciais.

Cada unidade possui sua própria operação comercial, gerando diariamente dados relacionados às vendas, clientes, vendedores, produtos e movimentações de estoque.

---

## 2. Contexto do Projeto
A Amplo Varejo S.A. identificou uma queda aproximada de 12% no faturamento nos últimos seis meses, mas a diretoria não consegue identificar claramente onde essa redução está concentrada ou quais fatores podem estar relacionados ao resultado.

Diante desse cenário, o projeto propõe a construção de uma estrutura de dados capaz de integrar as informações da operação e permitir uma análise detalhada do desempenho da empresa, considerando regiões, lojas, produtos, categorias, vendedores, metas e períodos.

A partir dessa análise, busca-se identificar os principais pontos de impacto e levantar possíveis fatores associados à queda do faturamento.

---

## 3. Problema de Negócio
A diretoria da Amplo Varejo S.A. identificou uma queda aproximada de 12% no faturamento durante os últimos seis meses.

Apesar de possuir dados sobre vendas, lojas, regiões, produtos, vendedores e metas, a empresa não consegue identificar claramente:
- onde a queda está concentrada;
- quais regiões foram mais afetadas;
- quais lojas apresentaram maior redução;
- quais categorias e produtos contribuíram para o resultado;
- se existem diferenças relevantes entre vendedores;
- se as metas estão sendo atingidas;
- se fatores como sazonalidade, campanhas ou disponibilidade de estoque podem estar relacionados ao comportamento observado.

A diretoria, portanto, necessita de uma análise estruturada que permita compreender o desempenho comercial e identificar possíveis fatores associados à redução do faturamento.

---

## 4. Pergunta Central do Projeto
A investigação será orientada pela seguinte pergunta:

> **Onde está ocorrendo a queda do faturamento e quais fatores podem estar relacionados a esse comportamento?**

Essa pergunta será utilizada como principal direcionador das etapas de geração, organização, transformação e análise dos dados.

---

## 5. Objetivos do Projeto

### 5.1 Objetivo Geral
Investigar a queda aproximada de 12% no faturamento da Amplo Varejo S.A., identificando onde a redução está concentrada e quais fatores podem estar associados ao resultado.

### 5.2 Objetivos Específicos
O projeto deverá permitir:
1. acompanhar a evolução do faturamento ao longo do tempo;
2. identificar regiões com maior redução no faturamento;
3. identificar lojas com pior desempenho;
4. analisar o comportamento das categorias de produtos;
5. identificar produtos com maior impacto sobre a variação das vendas;
6. comparar o desempenho dos vendedores;
7. analisar o cumprimento das metas comerciais;
8. investigar possíveis efeitos de sazonalidade;
9. analisar possíveis relações entre campanhas e desempenho de vendas;
10. investigar, quando aplicável, possíveis relações entre disponibilidade de estoque e vendas;
11. gerar indicadores para acompanhamento do desempenho comercial;
12. produzir evidências que apoiem recomendações para a gestão.

---

## 6. Escopo da Análise e KPI’S
A investigação será realizada a partir de diferentes dimensões do negócio.

### 6.1 Tempo
Serão analisados:
- evolução do faturamento;
- variação mensal;
- comparação entre períodos;
- comportamento ao longo dos seis meses de queda;
- possíveis padrões de sazonalidade;
- períodos promocionais e campanhas.

### 6.2 Regiões
Serão analisados:
- faturamento por região;
- crescimento ou queda percentual;
- participação de cada região no faturamento;
- comparação do desempenho entre regiões.

As cinco regiões consideradas serão:
- Sudeste;
- Sul;
- Nordeste;
- Centro-Oeste;
- Norte.

### 6.3 Lojas
Serão analisados:
- faturamento por loja;
- variação do faturamento;
- participação da loja no resultado;
- desempenho em relação às metas;
- identificação das unidades com maior impacto negativo.

### 6.4 Categorias e Produtos
Serão analisados:
- faturamento por categoria;
- evolução das vendas;
- participação das categorias;
- produtos com maior redução;
- produtos com maior contribuição para o faturamento;
- alterações na composição das vendas.

### 6.5 Vendedores
Serão analisados:
- faturamento por vendedor;
- quantidade de vendas;
- ticket médio;
- desempenho em relação às metas;
- comparação entre vendedores e equipes.

### 6.6 Metas
Serão analisados:
- meta estabelecida;
- faturamento realizado;
- percentual de atingimento;
- diferença entre meta e realizado;
- desempenho por região e loja.

### 6.7 Estoque
Quando os dados simulados permitirem, será investigada a possível relação entre:
- disponibilidade de produtos;
- rupturas de estoque;
- volume de vendas;
- desempenho de determinadas lojas ou categorias.

O estoque será tratado como uma possível variável explicativa, e não como causa previamente determinada da queda.

---

## 7. Indicadores Principais
Entre os principais indicadores que poderão compor a solução estão:

### Indicadores financeiros
- Faturamento;
- Variação percentual do faturamento;
- Faturamento por período;
- Faturamento por região;
- Faturamento por loja;
- Faturamento por categoria;
- Faturamento por produto.

### Indicadores comerciais
- Quantidade de pedidos;
- Quantidade de itens vendidos;
- Ticket médio;
- Vendas por vendedor;
- Meta x realizado;
- Percentual de atingimento da meta.

### Indicadores operacionais
- Disponibilidade de estoque;
- Ruptura de estoque;
- Estoque por produto;
- Estoque por loja.

Os indicadores definitivos serão definidos de acordo com a estrutura dos dados gerados e com as necessidades identificadas durante a análise.

---

## 8. Solução Proposta
Para responder ao problema de negócio, será desenvolvido um fluxo completo de Engenharia e Análise de Dados.

A arquitetura conceitual do projeto será:
- Regras de Negócio
- Banco de Dados OLTP
- Geração dos Dados com Python
- Arquivos CSV
- ETL / Transformação
- Data Warehouse
- Power BI
- Indicadores
- Análise dos Dados
- Identificação dos Problemas
- Recomendações Estratégicas

A solução terá como objetivo reproduzir um fluxo próximo ao encontrado em um ambiente profissional de dados, desde a geração e armazenamento das informações até sua utilização para suporte à tomada de decisão.

---

## 9. Componentes do Projeto
O projeto será dividido nos seguintes componentes:

### 9.1 Regras de Negócio
Definição das regras que representam o funcionamento da empresa, incluindo:
- comportamento das vendas;
- relacionamento entre entidades;
- funcionamento das lojas;
- comportamento dos clientes;
- metas;
- estoque;
- sazonalidade;
- campanhas;
- eventos que afetam a operação.

### 9.2 Geração dos Dados
Será desenvolvido um processo utilizando Python para gerar os dados simulados da empresa.

Os dados deverão representar diferentes entidades e eventos da operação, permitindo a criação de um ambiente de dados suficientemente realista para as análises propostas.

### 9.3 Banco de Dados OLTP
Os dados operacionais serão organizados em um banco de dados relacional, representando o ambiente transacional da empresa.

### 9.4 ETL
Será desenvolvido um processo de Extração, Transformação e Carga (ETL) para preparar os dados para análise.

Essa etapa poderá envolver:
- tratamento de dados;
- padronização;
- validação;
- transformação;
- integração;
- criação de métricas necessárias para análise.

### 9.5 Data Warehouse
Os dados transformados serão organizados em uma estrutura dimensional adequada para análises e consultas analíticas.

### 9.6 Power BI
O Power BI será utilizado para construir os dashboards e disponibilizar os principais indicadores e análises para acompanhamento do desempenho empresarial.

### 9.7 Análise e Recomendações
Após a construção dos indicadores, os dados serão analisados para identificar:
- pontos de concentração da queda;
- regiões e lojas críticas;
- categorias e produtos afetados;
- diferenças de desempenho;
- desvios em relação às metas;
- possíveis fatores associados ao resultado.

A etapa final deverá transformar os resultados encontrados em insights e recomendações de negócio.

---

## 10. Resultado Esperado
Ao final do projeto, espera-se responder de maneira fundamentada à pergunta:

> **Onde ocorreu a queda de faturamento, quais áreas foram mais impactadas e quais fatores podem explicar esse comportamento?**

A análise deverá permitir identificar os principais pontos de atenção da operação e fornecer informações capazes de apoiar decisões relacionadas a:
- vendas;
- lojas;
- regiões;
- produtos;
- categorias;
- vendedores;
- metas;
- campanhas;
- estoque.

O resultado final não será apenas um dashboard, mas uma solução de dados completa, capaz de transformar dados operacionais em informações para apoio à tomada de decisão.

---

## 11. Critérios de Sucesso
O projeto será considerado bem-sucedido quando for capaz de:
1. gerar dados coerentes com as regras de negócio definidas;
2. integrar diferentes áreas da operação;
3. disponibilizar os dados em uma estrutura adequada para análise;
4. apresentar indicadores confiáveis;
5. identificar onde a queda de faturamento está concentrada;
6. apontar possíveis fatores relacionados ao comportamento observado;
7. permitir análises por diferentes dimensões do negócio;
8. apresentar os resultados de forma clara no Power BI;
9. gerar recomendações fundamentadas nos dados.

---

## 12. Entregáveis
Os principais entregáveis previstos são:

### Engenharia de Dados
- documentação das regras de negócio;
- gerador de dados em Python;
- arquivos CSV;
- banco de dados OLTP;
- processos de ETL;
- Data Warehouse.

### Business Intelligence
- modelo analítico;
- indicadores;
- dashboards em Power BI;
- análises por diferentes dimensões.

### Análise de Negócio
- identificação dos principais pontos de impacto;
- análise das possíveis causas;
- insights;
- recomendações estratégicas;
- resumo executivo dos resultados.

---

## 13. Limitações e Premissas
Por se tratar de um projeto simulado, os dados utilizados serão artificialmente gerados com base em regras de negócio definidas para representar uma operação varejista.

A queda de aproximadamente 12% no faturamento será utilizada como premissa inicial do cenário de negócio.

As possíveis causas da queda não serão determinadas antecipadamente. Elas deverão ser investigadas a partir dos dados gerados.

Dessa forma, fatores como sazonalidade, campanhas, desempenho de vendedores, categorias, lojas e estoque serão tratados como hipóteses de investigação.

---

## 14. Resumo Executivo
A Amplo Varejo S.A. é uma empresa fictícia criada para simular o ambiente de dados de uma grande organização do setor varejista.

No cenário proposto, a empresa apresentou uma queda aproximada de 12% no faturamento durante os últimos seis meses, porém a diretoria não possui clareza sobre onde essa redução está concentrada ou quais fatores podem estar relacionados ao resultado.

Para investigar o problema, será desenvolvido um ecossistema completo de dados, envolvendo regras de negócio, geração de dados com Python, banco de dados OLTP, processos de ETL, Data Warehouse, Power BI e análise de indicadores.

A investigação terá como foco o desempenho ao longo do tempo e as dimensões de região, loja, categoria, produto, vendedor, metas e, quando aplicável, estoque.

O objetivo final é transformar os dados operacionais simulados em informações capazes de identificar os principais pontos de impacto sobre o faturamento, levantar possíveis explicações para a queda e fornecer recomendações baseadas em evidências para apoiar a tomada de decisão.

