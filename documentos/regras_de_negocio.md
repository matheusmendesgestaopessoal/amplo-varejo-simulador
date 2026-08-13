# Documento de Regras de Negócio

## Dados Mestres e Cadastrais
As regras definidas para a geração dos dados são:

### Estados
- Todo estado deve possuir identificador único.
- Todos os 27 estados brasileiros devem possuir pelo menos uma loja.
- Todos os estados devem possuir vendedores.
- Todos os estados devem possuir pedidos.
- Todos os estados devem possuir vendas.
- A quantidade de lojas deve ser distribuída de acordo com o peso de cada região.

**Distribuição regional definida:**
- Sudeste: 45%
- Sul: 20%
- Nordeste: 20%
- Centro-Oeste: 10%
- Norte: 5%

### Lojas
- Toda loja deve possuir um identificador único.
- Toda loja deve pertencer a um estado válido.
- Toda loja deve possuir vendedores.
- A quantidade total de lojas depende do modo de execução do simulador.
- Toda loja deve possuir produtos em estoque.
- Toda loja deve possuir clientes relacionados às suas operações.
- A quantidade de lojas deve respeitar a distribuição regional estabelecida.
- Toda loja deve possuir um identificador único.

### Vendedores
- Todo vendedor deve possuir identificador único.
- Todo vendedor deve estar associado a uma loja.
- Toda loja deve possuir vendedores.
- Os vendedores devem ser distribuídos de forma equilibrada entre as lojas.
- Um pedido deve possuir um vendedor válido.
- O vendedor associado ao pedido deve pertencer à loja do pedido.

### Clientes
- Todo cliente deve possuir identificador único.
- Todo cliente deve possuir cadastro.
- Todo cliente deve possuir identificador único.
- CPF deve ser único.
- E-mail deve ser único.
- Os clientes devem ser distribuídos de acordo com a participação das regiões.
- Toda loja deve possuir clientes relacionados às suas operações.
- Um pedido não pode ser realizado por um cliente inexistente.

### Categorias
- Toda categoria possui identificador único.
- Toda categoria possui nome.
- Todo produto deve pertencer a uma categoria existente.
- A categoria é utilizada para agrupamento e análise dos produtos no Data Warehouse e Power BI.

**Categorias oficiais:**
- Casa
- Eletro
- Tecnologia
- Escritório

### Produtos
- Todo produto deve possuir identificador único.
- Todo produto deve pertencer a uma categoria.
- Todo produto deve possuir preço definido previamente.
- Todo produto deve possuir custo.
- O custo deve ser inferior ao preço de venda.
- Os valores devem ser compatíveis com o tipo de produto.
- Todo produto do catálogo deve possuir disponibilidade de estoque nas lojas.

---

## Operações e Dados Transacionais

### Pedidos
- Todo pedido possui identificador único.
- Todo pedido deve possuir cliente.
- Todo pedido deve possuir vendedor.
- Todo pedido deve possuir loja.
- O vendedor deve pertencer à loja do pedido.
- Todo pedido deve possuir uma data válida.
- Todo pedido deve possuir pelo menos um item.
- Um pedido pode possuir múltiplos itens.
- Pedidos devem ser distribuídos regionalmente.
- Pedidos devem possuir status.
- Pedidos cancelados não devem representar vendas efetivamente realizadas.

### Itens do pedido
- Todo item deve pertencer a um pedido válido.
- Todo item deve possuir um produto válido.
- A quantidade deve ser maior que zero.
- O preço utilizado deve corresponder ao preço do produto no momento da geração.
- O subtotal deve ser calculado a partir da quantidade e do preço.
- Um pedido pode possuir entre 1 e 5 itens.
- Cada item pode possuir entre 1 e 3 unidades.

### Estoque
- Toda loja deve possuir estoque.
- Todo produto deve possuir estoque nas lojas.
- Estoque inicial não pode ser negativo.
- Saídas de estoque somente devem ocorrer para pedidos efetivamente finalizados.
- Uma operação de venda não pode retirar quantidade superior ao estoque disponível.
- Entradas representam reposição de estoque.
- Movimentações devem estar vinculadas à loja e ao produto corretos.

### Movimentação de Estoque
**Tipos de movimentação:** Entradas e Saídas.

- Toda movimentação deve possuir loja.
- Toda movimentação deve possuir produto.
- Toda movimentação deve possuir data.
- Toda movimentação deve possuir quantidade.
- Toda movimentação deve possuir tipo.
- Saídas devem estar relacionadas a itens de pedidos.
- Pedidos cancelados não devem gerar saída de estoque.
- A quantidade retirada deve corresponder à quantidade efetivamente vendida.

---

## Dados de Apoio da Simulação

### Calendário
- Deve possuir todas as datas do período definido.
- Não pode possuir lacunas.
- Deve conter:
  - data;
  - ano;
  - mês;
  - nome do mês;
  - trimestre;
  - semestre;
  - dia;
  - dia da semana;
  - indicador de dia útil;
  - indicador de final de semana.

### Sazonalidade
- Cada mês deve possuir um índice de sazonalidade.
- O índice deve ser maior que zero.
- O índice pode aumentar ou reduzir a demanda.
- A sazonalidade é utilizada pelo motor de simulação para determinar a demanda diária.
- A sazonalidade é relacionada ao calendário através do mês.

### Campanhas
- Uma campanha possui período de atuação.
- Possui nome.
- Pode influenciar a demanda.
- O impacto da campanha é aplicado pelo motor de simulação.
- Campanhas podem representar ações como:
  - Semana do Cliente;
  - Black Friday;
  - Queima de Estoque;
  - campanhas promocionais.

### Eventos
- Um evento possui período de ocorrência.
- Possui tipo.
- Possui impacto sobre a operação.
- Pode afetar determinada região, loja ou operação, dependendo da implementação do cenário.
- O impacto deve ser considerado pelo motor de simulação.

### Metas
- Toda meta deve possuir uma loja.
- Toda meta deve possuir um período.
- Deve possuir meta de faturamento.
- Deve possuir meta de pedidos.
- Deve possuir meta de ticket médio.
- As metas devem permitir comparação entre Realizado × Meta no Data Warehouse e Power BI.