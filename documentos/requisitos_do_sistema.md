# Documento de Requisitos do Sistema

## Requisitos Funcionais

### RF01 - Configuração da simulação
O sistema deve permitir definir:
- modo de execução;
- período da simulação;
- quantidade de lojas;
- quantidade de clientes;
- quantidade de vendedores;
- quantidade de pedidos;
- parâmetros de estoque;
- quantidade de itens por pedido.

### RF02 - Geração do calendário
O sistema deve gerar o calendário correspondente ao período configurado.

### RF03 - Geração dos estados
O sistema deve gerar os 27 estados brasileiros e suas respectivas regiões.

### RF04 - Geração das lojas
O sistema deve gerar lojas distribuídas entre as regiões brasileiras conforme os pesos definidos.

### RF05 - Geração dos vendedores
O sistema deve distribuir vendedores entre as lojas.

### RF06 - Geração dos clientes
O sistema deve gerar clientes fictícios e distribuí-los conforme as regras regionais estabelecidas.

### RF07 - Geração dos produtos
O sistema deve gerar os produtos a partir do catálogo definido, utilizando preços e custos previamente estabelecidos.

### RF08 - Geração de pedidos
O sistema deve gerar pedidos ao longo do período da simulação.

### RF09 - Geração de itens
O sistema deve gerar um ou mais itens para cada pedido.

### RF10 - Geração do estoque
O sistema deve gerar estoque inicial para os produtos em cada loja.

### RF11 - Geração das movimentações
O sistema deve gerar movimentações de estoque relacionadas às operações realizadas.

### RF12 - Aplicação de sazonalidade
O sistema deve permitir representar diferentes níveis de demanda ao longo do período.

### RF13 - Aplicação de eventos e campanhas
O sistema deve permitir representar eventos e campanhas capazes de alterar o comportamento da demanda.

### RF14 - Validação
O sistema deve validar a consistência dos dados gerados antes da utilização.

### RF15 - Exportação
O sistema deve permitir exportar os dados gerados para:
- CSV;
- banco OLTP.

### RF16 - Data Warehouse
O projeto deve permitir transformar os dados do OLTP em um Data Warehouse dimensional.

### RF17 - Análise
Os dados do DW devem estar disponíveis para análise no Power BI.

---

## Requisitos Não Funcionais

### RNF01 - Integridade
Os dados devem respeitar integridade referencial entre as entidades.

### RNF02 - Consistência
Os dados gerados devem respeitar as regras de negócio estabelecidas.

### RNF03 - Reprodutibilidade
O simulador deve utilizar uma semente de aleatoriedade configurável, permitindo reproduzir uma geração.  
Atualmente: `SEMENTE_ALEATORIA = 42`

### RNF04 - Escalabilidade
O sistema deve possuir diferentes modos de execução:
1. desenvolvimento
2. teste
3. produção

permitindo trabalhar com diferentes volumes de dados.

### RNF05 - Manutenibilidade
A geração deve estar organizada em módulos independentes, permitindo alterar uma entidade sem modificar todo o sistema.

### RNF06 - Interoperabilidade
Os dados devem poder ser utilizados por diferentes ferramentas através de CSV, SQL e Data Warehouse.

### RNF07 - Rastreabilidade
Os registros devem possuir identificadores que permitam relacionar as operações entre OLTP, DW e fontes originais.

### RNF08 - Qualidade
O sistema deve possuir mecanismos de validação capazes de identificar:
- registros ausentes;
- relacionamentos inválidos;
- estados sem lojas;
- lojas sem vendedores;
- estados sem pedidos;
- estoques negativos;
- inconsistências entre tabelas.