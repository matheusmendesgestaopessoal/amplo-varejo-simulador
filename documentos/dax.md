# Documentação de Medidas DAX — Amplo Varejo S.A.

Todas as métricas foram construídas dinamicamente no Power BI utilizando DAX sobre o Data Warehouse dimensional (Star Schema).

---

### Vendas e Indicadores Financeiros

**DAX**

Receita_Total = SUM('FATO Vendas'[sub_total])

Custo_Total = SUM('FATO Vendas'[Custo_Total])

Lucro_Total = [Receita_Total] - [Custo_Total]

Margem % = DIVIDE([Lucro_Total], [Receita_Total])

Ticket_Médio = DIVIDE([Receita_Total], [Quantidade_Pedidos])

Quantidade_Pedidos = 
CALCULATE(
    DISTINCTCOUNT('FATO Vendas'[id_pedido]),
    'FATO Vendas'[sk_status] <> 3
)

Quantidade_Vendida = 
CALCULATE(
    SUM('FATO Vendas'[quantidade]),
    'FATO Vendas'[sk_status] <> 3
)

Produtos_Vendidos = SUM('FATO Vendas'[quantidade])

Participacao_Produto = 
DIVIDE(
    [Receita_Total],
    CALCULATE([Receita_Total], ALL('DIM Produtos'))
)

---

### Metas e Desempenho Comercial

Meta_Faturamento = 
SUM('FATO Metas'[meta_faturamento])

Meta_Pedidos = 
SUM('FATO Metas'[meta_pedidos])

Meta x Realizado % = 
DIVIDE([Receita_Total], [Meta_Faturamento])

Diferença Meta = 
[Receita_Total] - [Meta_Faturamento]

Falta para Meta % = 
1 - DIVIDE([Receita_Total], [Meta_Faturamento])

Ranking Loja = 
RANKX(
    ALLSELECTED('DIM Lojas'[nome_loja]),
    [Receita_Total],
    ,
    DESC,
    DENSE
)

---

## Cancelamentos e Análise de Perdas

Pedidos Cancelados = 
CALCULATE(
    DISTINCTCOUNT('FATO Vendas'[id_pedido]), 
    'FATO Vendas'[sk_status] = 3
)

Receita Perdida = CALCULATE([Receita_Total], 'FATO Vendas'[sk_status] = 3)

Taxa Cancelamento = DIVIDE([Pedidos Cancelados], [Quantidade_Pedidos], 0)

Meta % Cancelamento = 0.03

Desvio Meta Cancelamento = [Taxa Cancelamento] - [Meta % Cancelamento]

Desvio Meta Cancelamento (p.p.) = ([Taxa Cancelamento] - [Meta % Cancelamento]) * 100

% Cancelamentos por Região = 
DIVIDE(
    [Pedidos Cancelados],
    CALCULATE(
        [Pedidos Cancelados],
        ALL('DIM Lojas'[regiao])
    ),
    0
)

---

## Clientes e Operações de Loja

Clientes_Ativos = 
CALCULATE(
    DISTINCTCOUNT('FATO Vendas'[sk_cliente]),
    'FATO Vendas'[sk_status] <> 3
)

Frequencia_Compra = 
DIVIDE(
    [Quantidade_Pedidos],
    DISTINCTCOUNT('DIM Cliente'[sk_cliente])
)

Lojas_Ativas = DISTINCTCOUNT('FATO Vendas'[sk_loja])

---

## Gestão de Estoque e Logística

Entradas = 
CALCULATE(
    SUM('FATO Movimentacão Estoque'[quantidade]), 
    'FATO Movimentacão Estoque'[tipo_movimentacao] = "Entrada"
)

Saidas = 
CALCULATE(
    SUM('FATO Movimentacão Estoque'[quantidade]), 
    'FATO Movimentacão Estoque'[tipo_movimentacao] = "Saída"
)

Estoque_Atual = [Entradas] - [Saidas]

Valor_Estoque = 
SUMX(
    VALUES('DIM Produtos'[sk_produto]),
    [Estoque_Atual] * MAX('DIM Produtos'[custo])
)