USE amplo_varejo_dw;

-- View 1 — vw_kpis_gerais
CREATE OR REPLACE VIEW vw_kpis_gerais AS

SELECT
COUNT(DISTINCT id_pedido) AS total_pedidos,
COUNT(DISTINCT sk_cliente) AS clientes_ativos,
SUM(quantidade) AS itens_vendidos,
ROUND(SUM(sub_total),2) AS receita_total,
ROUND(SUM(custo_total),2) AS custo_total,
ROUND(SUM(margem),2) AS lucro_total,
ROUND(AVG(sub_total),2) AS ticket_medio,
ROUND(
(SUM(margem) / NULLIF(SUM(sub_total),0))*100
,2) AS margem_percentual
FROM fato_vendas;

-- View 2 — Receita Mensal
CREATE OR REPLACE VIEW vw_receita_mensal AS
SELECT
c.ano,
c.mes,
c.nome_mes,
SUM(f.sub_total) AS receita,
SUM(f.margem) AS lucro,
COUNT(DISTINCT f.id_pedido) AS pedidos,
SUM(f.quantidade) AS itens_vendidos
FROM fato_vendas f
INNER JOIN dim_calendario c
ON f.sk_calendario = c.sk_calendario
GROUP BY c.ano, c.mes, c.nome_mes
ORDER BY c.ano, c.mes;

-- View 3 — Meta x Realizado
CREATE OR REPLACE VIEW vw_meta_realizado AS
SELECT
m.mes,
l.nome_loja,
SUM(m.meta_faturamento) AS meta,
COALESCE(SUM(f.sub_total),0) AS realizado,
ROUND(
(COALESCE(SUM(f.sub_total),0) /
NULLIF(SUM(m.meta_faturamento),0))*100
,2) AS percentual_meta
FROM fato_metas m
INNER JOIN dim_loja l ON m.sk_loja = l.sk_loja
LEFT JOIN fato_vendas f ON f.sk_loja = m.sk_loja
LEFT JOIN dim_calendario c ON c.sk_calendario = f.sk_calendario AND c.mes = m.mes
GROUP BY m.mes, l.nome_loja;

-- View 4 — Receita por Estado

CREATE OR REPLACE VIEW vw_receita_estado AS
SELECT
l.nome_estado,
l.uf,
l.regiao,
SUM(f.sub_total) AS receita,
SUM(f.margem) AS lucro,
COUNT(DISTINCT f.id_pedido) AS pedidos
FROM fato_vendas f
INNER JOIN dim_loja l
ON f.sk_loja = l.sk_loja
GROUP BY
l.nome_estado,
l.uf,
l.regiao
ORDER BY receita DESC;

-- View 5 — Receita por Categoria
CREATE OR REPLACE VIEW vw_receita_categoria AS
SELECT
p.nome_categoria,
SUM(f.sub_total) AS receita,
SUM(f.quantidade) AS itens,
SUM(f.margem) AS lucro,
COUNT(DISTINCT f.id_pedido) AS pedidos
FROM fato_vendas f
INNER JOIN dim_produto p
ON f.sk_produto = p.sk_produto
GROUP BY
p.nome_categoria
ORDER BY receita DESC;

