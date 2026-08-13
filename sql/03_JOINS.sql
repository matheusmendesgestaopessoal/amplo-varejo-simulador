USE amplo_varejo_dw;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE fato_vendas;
TRUNCATE TABLE fato_movimentacao_estoque;
TRUNCATE TABLE fato_metas;
TRUNCATE TABLE dim_calendario;
TRUNCATE TABLE dim_loja;
TRUNCATE TABLE dim_produto;
TRUNCATE TABLE dim_cliente;
TRUNCATE TABLE dim_vendedor;
-- dim_status_pedido NÃO é truncada -- ela é fixa (seed do DDL)

INSERT INTO dim_calendario (sk_calendario, data, ano, mes, nome_mes, trimestre, semestre, dia,
dia_semana, dia_util, final_de_semana, indice_sazonalidade, classificacao_sazonalidade)
SELECT c.id_calendario, c.data, c.ano, c.mes, c.nome_mes, c.trimestre, c.semestre, c.dia,
c.dia_semana, c.dia_util, c.final_de_semana, s.indice_vendas, s.classificacao
FROM amplo_varejo.calendario c
LEFT JOIN amplo_varejo.sazonalidade s ON s.mes = c.mes;

-- dim_loja (lojas + estados)
INSERT INTO dim_loja (sk_loja, nome_loja, endereco, nome_estado, uf, regiao)
SELECT l.id_loja, l.nome_loja, l.endereco, e.nome_estado, e.uf, e.regiao
FROM amplo_varejo.lojas l
LEFT JOIN amplo_varejo.estados e ON e.id_estado = l.id_estado;


-- dim_produto (produtos + categorias)
INSERT INTO dim_produto (sk_produto, nome_produto, nome_categoria, preco, custo, ativo)
SELECT p.id_produto, p.nome_produto, cat.nome_categoria, p.preco, p.custo, p.ativo
FROM amplo_varejo.produtos p
LEFT JOIN amplo_varejo.categorias cat ON cat.id_categoria = p.id_categoria;



-- dim_cliente
INSERT INTO dim_cliente (sk_cliente, nome_cliente, cpf_cliente, email, cidade, id_loja)
SELECT id_cliente, nome_cliente, cpf_cliente, email, cidade, id_loja
FROM amplo_varejo.clientes;
 
-- dim_vendedor (vendedores + lojas + estados, desnormalizado)
INSERT INTO dim_vendedor (sk_vendedor, nome_vendedor, data_admissao, nome_loja, uf_loja, regiao_loja)
SELECT
  v.id_vendedor, v.nome_vendedor, v.data_admissao, l.nome_loja, e.uf, e.regiao
FROM amplo_varejo.vendedores v
LEFT JOIN amplo_varejo.lojas l ON l.id_loja = v.id_loja
LEFT JOIN amplo_varejo.estados e ON e.id_estado = l.id_estado;

-- 2. FATOS

-- fato_vendas (grão: item de pedido)
INSERT INTO fato_vendas
(sk_calendario, sk_cliente, sk_vendedor, sk_loja, sk_produto, sk_status,
id_pedido, id_item_pedido, quantidade, valor_unitario, desconto,
sub_total, custo_total, margem)
SELECT
ped.id_calendario,
ped.id_cliente,
ped.id_vendedor,
ped.id_loja,
it.id_produto,
dsp.sk_status,
it.id_pedido,
it.id_item_pedido,
it.quantidade,
it.valor_unitario,
it.desconto,
it.sub_total,
ROUND(it.quantidade * prod.custo, 2) AS custo_total,
ROUND(it.sub_total - (it.quantidade * prod.custo), 2) AS margem
FROM amplo_varejo.itens_pedido it
JOIN amplo_varejo.pedidos ped ON ped.id_pedido = it.id_pedido
JOIN amplo_varejo.produtos prod ON prod.id_produto = it.id_produto
JOIN dim_status_pedido dsp ON dsp.status = ped.status;

-- fato_movimentacao_estoque (grão: movimentação individual)
INSERT INTO fato_movimentacao_estoque (sk_calendario, sk_loja, sk_produto, id_item_pedido, tipo_movimentacao, quantidade)
SELECT
mov.id_calendario,
est.id_loja,
est.id_produto,
mov.id_item_pedido,
mov.tipo_movimentacao,
mov.quantidade
FROM amplo_varejo.movimentacao_estoque mov
JOIN amplo_varejo.estoque est ON est.id_estoque = mov.id_estoque;

-- fato_metas (grão: mês x loja)
INSERT INTO fato_metas (mes, sk_loja, meta_faturamento, meta_pedidos, meta_ticket_medio)
SELECT mes, id_loja, meta_faturamento, meta_pedidos, meta_ticket_medio
FROM amplo_varejo.metas;
 
SET FOREIGN_KEY_CHECKS = 1;

-- Conferência rápida de volumetria
-- =====================================================================
SELECT 'dim_calendario' AS tabela, COUNT(*) AS linhas FROM dim_calendario
UNION ALL SELECT 'dim_loja', COUNT(*) FROM dim_loja
UNION ALL SELECT 'dim_produto', COUNT(*) FROM dim_produto
UNION ALL SELECT 'dim_cliente', COUNT(*) FROM dim_cliente
UNION ALL SELECT 'dim_vendedor', COUNT(*) FROM dim_vendedor
UNION ALL SELECT 'dim_status_pedido', COUNT(*) FROM dim_status_pedido
UNION ALL SELECT 'fato_vendas', COUNT(*) FROM fato_vendas
UNION ALL SELECT 'fato_movimentacao_estoque', COUNT(*) FROM fato_movimentacao_estoque
UNION ALL SELECT 'fato_metas', COUNT(*) FROM fato_metas;

USE amplo_varejo_dw;

