# Dicionário de Dados · Amplo Varejo S.A.

Este documento descreve o Data Warehouse `amplo_varejo_dw` (modelo estrela) e as medidas DAX do dashboard.
A seção de medidas é gerada a partir do modelo semântico (`dashboard/amplo_varejo.SemanticModel`), então reflete
exatamente o que está no Power BI.

---

## Regras gerais das medidas

| Regra | Definição |
|---|---|
| Receita, custo, lucro e produtos vendidos | Consideram apenas pedidos **não cancelados** (`sk_status <> 3`) |
| Taxa de cancelamento | Pedidos cancelados ÷ **total** de pedidos (cancelados + válidos) |
| Receita perdida | Soma de `sub_total` dos pedidos cancelados |
| Meta | `fato_metas` não tem data: o mês do calendário é aplicado com `TREATAS` |
| Estoque | Entradas − saídas; valor a custo do produto |
| Excesso de estoque | Valor acima de 3 meses de cobertura, calculado por loja × produto |

---

## Tabelas do Data Warehouse

### Fatos

**fato_vendas** · 1 linha por item de pedido

| Coluna | Tipo | Descrição |
|---|---|---|
| sk_venda | BIGINT | Chave da linha |
| sk_calendario, sk_cliente, sk_vendedor, sk_loja, sk_produto, sk_status | INT | Chaves para as dimensões |
| id_pedido | INT | Dimensão degenerada: agrupa os itens do mesmo pedido |
| id_item_pedido | INT | Rastreabilidade com o banco operacional |
| quantidade | INT | Unidades vendidas |
| valor_unitario, desconto | DECIMAL | Preço praticado e desconto do item |
| sub_total | DECIMAL | Valor do item após desconto |
| custo_total | DECIMAL | Calculado no ETL: quantidade × custo do produto |
| margem | DECIMAL | Calculado no ETL: sub_total − custo_total |

**fato_movimentacao_estoque** · 1 linha por movimentação

| Coluna | Tipo | Descrição |
|---|---|---|
| sk_movimentacao | BIGINT | Chave da linha |
| sk_calendario, sk_loja, sk_produto | INT | Chaves para as dimensões |
| id_item_pedido | INT | Venda de origem (apenas saídas) |
| tipo_movimentacao | ENUM | `Entrada` (estoque inicial) ou `Saída` (venda paga ou enviada) |
| quantidade | INT | Unidades movimentadas |

**fato_metas** · 1 linha por loja × mês

| Coluna | Tipo | Descrição |
|---|---|---|
| sk_meta | INT | Chave da linha |
| mes | INT | Mês (1 a 12) |
| sk_loja | INT | Chave da loja |
| meta_faturamento | INT | Meta de receita do mês |
| meta_pedidos | INT | Meta de pedidos do mês |
| meta_ticket_medio | INT | meta_faturamento ÷ meta_pedidos |

### Dimensões

| Tabela | Chave | Principais colunas |
|---|---|---|
| dim_calendario | sk_calendario | data, ano, mes, nome_mes, trimestre, semestre, dia_semana, dia_util, final_de_semana, indice_sazonalidade, classificacao_sazonalidade |
| dim_loja | sk_loja | nome_loja, endereco, nome_estado, uf, regiao |
| dim_produto | sk_produto | nome_produto, nome_categoria, preco, custo, ativo |
| dim_cliente | sk_cliente | nome_cliente, cidade, id_loja (dados fictícios gerados com Faker) |
| dim_vendedor | sk_vendedor | nome_vendedor, data_admissao, nome_loja, uf_loja, regiao_loja |
| dim_status_pedido | sk_status | status: 1 pendente, 2 pago, **3 cancelado**, 4 enviado |

### Tabela de apoio do relatório

| Tabela | Descrição |
|---|---|
| Plano_Prescritivo | Tabela fixa (DATATABLE) com as 3 frentes do plano de ação: ordem, decisão, dono, prazo, indicador, valor recuperável, esforço, confiança e prioridade |

---

## Medidas DAX


### Medidas base

**Receita_Total**
```dax
CALCULATE(SUM('FATO Vendas'[sub_total]), 'FATO Vendas'[sk_status] <> 3)
```

**Custo_Total**
```dax
CALCULATE(SUM('FATO Vendas'[custo_total]), 'FATO Vendas'[sk_status] <> 3)
```

**Lucro_Total**
```dax
[Receita_Total] - [Custo_Total]
```

**Margem %**
```dax
DIVIDE([Lucro_Total], [Receita_Total])
```

**Quantidade_Pedidos**
```dax
CALCULATE(DISTINCTCOUNT('FATO Vendas'[id_pedido]),'FATO Vendas'[sk_status] <> 3)
```

**Quantidade_Vendida**
```dax
CALCULATE(SUM('FATO Vendas'[quantidade]),'FATO Vendas'[sk_status] <> 3)
```

**Ticket_Médio**
```dax
DIVIDE([Receita_Total], [Quantidade_Pedidos])
```


### Metas e desempenho

**Clientes_Ativos**
```dax
CALCULATE(DISTINCTCOUNT('FATO Vendas'[sk_cliente]),'FATO Vendas'[sk_status] <> 3)
```

**Meta_Faturamento**
```dax
CALCULATE(SUM('FATO Metas'[meta_faturamento]), TREATAS(VALUES('DIM Calendario'[mes]), 'FATO Metas'[mes]))
```

**Meta_Pedidos**
```dax
CALCULATE(SUM('FATO Metas'[meta_pedidos]), TREATAS(VALUES('DIM Calendario'[mes]), 'FATO Metas'[mes]))
```

**Meta x Realizado %**
```dax
DIVIDE([Receita_Total],[Meta_Faturamento])
```

**Diferença Meta**
```dax
[Receita_Total] - [Meta_Faturamento]
```

**Falta para Meta %**
```dax
1 - DIVIDE([Receita_Total],[Meta_Faturamento])
```

**Ranking Loja**
```dax

RANKX(
    ALLSELECTED('DIM Lojas'[nome_loja]),
    [Receita_Total],
    ,
    DESC,
    DENSE
)
```

**Lojas_Ativas**
```dax

DISTINCTCOUNT('FATO Vendas'[sk_loja])
```


### Produtos e estoque

**Produtos_Vendidos**
```dax
CALCULATE(SUM('FATO Vendas'[quantidade]), 'FATO Vendas'[sk_status] <> 3)
```

**Entradas**
```dax
CALCULATE( SUM('FATO Movimentacão Estoque'[quantidade]), 'FATO Movimentacão Estoque'[tipo_movimentacao] = "Entrada")
```

**Saidas**
```dax
CALCULATE( SUM('FATO Movimentacão Estoque'[quantidade]), 'FATO Movimentacão Estoque'[tipo_movimentacao] = "Saída")
```

**Estoque_Atual**
```dax
[Entradas] - [Saidas]
```

**Valor_Estoque**
```dax
SUMX(
    VALUES('DIM Produtos'[sk_produto]),
    [Estoque_Atual] * CALCULATE(MAX('DIM Produtos'[custo]))
)
```

**Participacao_Produto**
```dax
DIVIDE([Receita_Total],CALCULATE([Receita_Total], ALL('DIM Produtos')))
```


### Clientes

**Frequencia_Compra**
```dax

DIVIDE(
    [Quantidade_Pedidos],
    DISTINCTCOUNT('DIM Cliente'[sk_cliente])
)
```


### Cancelamentos

**Pedidos Cancelados**
```dax
CALCULATE(DISTINCTCOUNT('FATO Vendas'[id_pedido]), 'FATO Vendas'[sk_status] = 3 )
```

**Taxa Cancelamento**
```dax
DIVIDE([Pedidos Cancelados], [Pedidos Totais], 0)
```

**Receita Perdida**
```dax
CALCULATE(SUM('FATO Vendas'[sub_total]), 'FATO Vendas'[sk_status] = 3)
```

**Meta % Cancelamento**
```dax
0.03
```

**Desvio Meta Cancelamento**
```dax
[Taxa Cancelamento] - [Meta % Cancelamento]
```

**Desvio Meta Cancelamento (p.p.)**
```dax

([Taxa Cancelamento] - [Meta % Cancelamento]) * 100
```

**% Cancelamentos por Região**
```dax

DIVIDE(
    [Pedidos Cancelados],
    CALCULATE(
        [Pedidos Cancelados],
        ALL('DIM Lojas'[regiao])
    ),
    0
)
```


### Diagnóstico (novas)

**Pedidos Totais**
```dax
DISTINCTCOUNT('FATO Vendas'[id_pedido])
```

**Cancelamento x Meta**
```dax
DIVIDE([Taxa Cancelamento], [Meta % Cancelamento])
```

**Gap Meta Rede**
```dax
MAX(0, [Meta_Faturamento] - [Receita_Total])
```

**Lojas Avaliadas**
```dax
COUNTROWS(FILTER(VALUES('DIM Lojas'[sk_loja]), NOT ISBLANK([Meta_Faturamento])))
```

**Lojas Abaixo Meta**
```dax
COUNTROWS(FILTER(VALUES('DIM Lojas'[sk_loja]), [Meta x Realizado %] < 1))
```

**Gap Lojas Abaixo Meta**
```dax
SUMX(
    FILTER(VALUES('DIM Lojas'[sk_loja]), [Meta x Realizado %] < 1),
    [Meta_Faturamento] - [Receita_Total]
)
```

**Lojas Abaixo 90%**
```dax
COUNTROWS(FILTER(VALUES('DIM Lojas'[sk_loja]), [Meta x Realizado %] < 0.9))
```

**Gap Lojas Abaixo 90%**
```dax
SUMX(
    FILTER(VALUES('DIM Lojas'[sk_loja]), [Meta x Realizado %] < 0.9),
    [Meta_Faturamento] - [Receita_Total]
)
```

**Estoque Final (un)**
```dax
CALCULATE([Estoque_Atual], REMOVEFILTERS('DIM Calendario'))
```

**Vendas Ano (un)**
```dax
CALCULATE([Saidas], REMOVEFILTERS('DIM Calendario'))
```

**Valor Estoque Final**
```dax
CALCULATE([Valor_Estoque], REMOVEFILTERS('DIM Calendario'))
```

**Cobertura Estoque (meses)**
```dax
DIVIDE([Estoque Final (un)], DIVIDE([Vendas Ano (un)], 12))
```

**Excesso Estoque**
```dax
-- valor a custo acima de 3 meses de cobertura, por loja e produto
SUMX(
    CROSSJOIN(VALUES('DIM Lojas'[sk_loja]), VALUES('DIM Produtos'[sk_produto])),
    VAR _final = [Estoque Final (un)]
    VAR _vendaMes = DIVIDE([Vendas Ano (un)], 12)
    VAR _excesso = IF(_vendaMes > 0, MAX(0, _final - 3 * _vendaMes), MAX(0, _final))
    RETURN _excesso * CALCULATE(MAX('DIM Produtos'[custo]))
)
```

**Excesso Estoque %**
```dax
DIVIDE([Excesso Estoque], [Valor Estoque Final])
```

**Combinações Sem Venda**
```dax
COUNTROWS(
    FILTER(
        CROSSJOIN(VALUES('DIM Lojas'[sk_loja]), VALUES('DIM Produtos'[sk_produto])),
        [Estoque Final (un)] > 0 && [Vendas Ano (un)] = 0
    )
)
```

**Pedidos Média por Loja**
```dax
CALCULATE(DIVIDE([Quantidade_Pedidos], DISTINCTCOUNT('FATO Vendas'[sk_loja])), REMOVEFILTERS('DIM Lojas'))
```

**Ticket Médio Rede**
```dax
CALCULATE([Ticket_Médio], REMOVEFILTERS('DIM Lojas'))
```

**Taxa Cancelamento Rede**
```dax
CALCULATE([Taxa Cancelamento], REMOVEFILTERS('DIM Lojas'))
```

**Pedidos vs Média**
```dax
DIVIDE([Quantidade_Pedidos], [Pedidos Média por Loja]) - 1
```

**Ticket vs Média**
```dax
DIVIDE([Ticket_Médio], [Ticket Médio Rede]) - 1
```

**Participação Receita**
```dax
DIVIDE([Receita_Total], CALCULATE([Receita_Total], ALLSELECTED()))
```


### Textos dinâmicos (novas)

Medidas de texto usadas nos títulos dinâmicos, cartões e tooltips. Mudam com os filtros e com a loja do drill-through.

`Txt Resposta`, `Txt KPI Receita`, `Txt Ctx Receita`, `Txt KPI Lucro`, `Txt Ctx Lucro`, `Txt KPI Pedidos`, `Txt Ctx Pedidos`, `Txt KPI Cancelamento`, `Txt Ctx Cancelamento`, `Txt KPI Lojas`, `Txt Ctx Lojas`, `Txt Receita Perdida`, `Txt Gap Lojas`, `Txt Excesso Estoque`, `Txt Titulo Contexto`, `Txt Titulo Cancelamento`, `Txt Titulo Lojas`, `Txt Titulo Estoque`, `Txt Titulo Loja`, `Txt KPI Loja Receita`, `Txt Ctx Loja Receita`, `Txt Ctx Loja Pedidos`, `Txt Ctx Loja Ticket`, `Txt Ctx Loja Cancelamento`, `Txt KPI Ticket`, `Txt Diagnostico Loja`, `Txt Acao Loja`, `Txt Tooltip Regiao`


### Formatação condicional (novas)

Cores calculadas para a formatação condicional dos visuais (verde, âmbar e vermelho da paleta).

`Cor Atingimento`, `Cor Cancelamento`
