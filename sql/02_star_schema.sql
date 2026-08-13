CREATE DATABASE amplo_varejo_dw DEFAULT CHARACTER SET utf8mb4; 
USE amplo_varejo_dw;

SET FOREIGN_KEY_CHECKS = 0;
-- Fonte: calendario + sazonalidade (join por mes)

CREATE TABLE IF NOT EXISTS dim_calendario (
sk_calendario INT UNSIGNED NOT NULL,
data DATE NOT NULL,
ano INT UNSIGNED NOT NULL,
mes INT UNSIGNED NOT NULL,
nome_mes VARCHAR(45) NOT NULL,
trimestre TINYINT NOT NULL,
semestre TINYINT NOT NULL,
dia TINYINT NOT NULL,
dia_semana VARCHAR(45) NOT NULL,
dia_util TINYINT NOT NULL,
final_de_semana TINYINT NOT NULL,
indice_sazonalidade DOUBLE NULL,-- de sazonalidade.indice_vendas
classificacao_sazonalidade VARCHAR(45) NULL, -- de sazonalidade.classificacao
PRIMARY KEY (sk_calendario)
) ENGINE = InnoDB;


-- Fonte: lojas + estados (desnormalizado)
CREATE TABLE IF NOT EXISTS dim_loja (
sk_loja INT UNSIGNED NOT NULL,   -- reaproveita id_loja
nome_loja VARCHAR(45) NOT NULL,
endereco VARCHAR(100) NOT NULL,
nome_estado VARCHAR(45) NOT NULL,
uf CHAR(2) NOT NULL,
regiao VARCHAR(45) NOT NULL,
PRIMARY KEY (sk_loja)
) ENGINE = InnoDB;

-- Fonte: produtos + categorias (desnormalizado)
 CREATE TABLE IF NOT EXISTS dim_produto (
sk_produto INT UNSIGNED NOT NULL,   -- reaproveita id_produto
nome_produto VARCHAR(45) NOT NULL,
nome_categoria VARCHAR(45) NOT NULL,
preco DECIMAL(10,2) UNSIGNED NOT NULL,
custo DECIMAL(10,2) UNSIGNED NOT NULL,
ativo TINYINT NOT NULL,
PRIMARY KEY (sk_produto)
) ENGINE = InnoDB;

-- Fonte: clientes
CREATE TABLE IF NOT EXISTS dim_cliente (
sk_cliente INT UNSIGNED NOT NULL,   -- reaproveita id_cliente
nome_cliente VARCHAR(45) NOT NULL,
cpf_cliente VARCHAR(14) NOT NULL,
email VARCHAR(45) NOT NULL,
cidade VARCHAR(45) NOT NULL,
id_loja INT UNSIGNED NOT NULL,
PRIMARY KEY (sk_cliente)
) ENGINE = InnoDB;

-- Fonte: vendedores + lojas (loja onde o vendedor atua, desnormalizado)
CREATE TABLE IF NOT EXISTS dim_vendedor (
sk_vendedor INT UNSIGNED NOT NULL,   -- reaproveita id_vendedor
nome_vendedor VARCHAR(45) NOT NULL,
data_admissao DATE NOT NULL,
nome_loja VARCHAR(45) NOT NULL,
uf_loja CHAR(2) NOT NULL,
regiao_loja VARCHAR(45) NOT NULL,
PRIMARY KEY (sk_vendedor)
) ENGINE = InnoDB;

-- dim_status_pedido (dimensão junk, pequena, do ENUM de pedidos.status)
CREATE TABLE IF NOT EXISTS dim_status_pedido (
sk_status TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
status VARCHAR(20) NOT NULL,
PRIMARY KEY (sk_status),
UNIQUE INDEX status_UNIQUE (status ASC)
) ENGINE = InnoDB;
 
INSERT INTO dim_status_pedido (status) VALUES ('pendente'), ('pago'), ('cancelado'), ('enviado');
  
-- FATOS
-- Grão: 1 linha por item de pedido (itens_pedido)
CREATE TABLE IF NOT EXISTS fato_vendas (
sk_venda BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
sk_calendario INT UNSIGNED NOT NULL,
sk_cliente INT UNSIGNED NOT NULL,
sk_vendedor INT UNSIGNED NOT NULL,
sk_loja INT UNSIGNED NOT NULL,
sk_produto INT UNSIGNED NOT NULL,
sk_status TINYINT UNSIGNED NOT NULL,
id_pedido INT UNSIGNED NOT NULL,    -- dimensão degenerada, agrupa itens do mesmo pedido
id_item_pedido INT UNSIGNED NOT NULL,    -- dimensão degenerada, rastreabilidade com o OLTP
quantidade INT UNSIGNED NOT NULL,
valor_unitario DECIMAL(10,2) UNSIGNED NOT NULL,
desconto DECIMAL(10,2) UNSIGNED NOT NULL,
sub_total DECIMAL(10,2) UNSIGNED NOT NULL,
custo_total DECIMAL(10,2) UNSIGNED NULL,   -- calculado no ETL: quantidade * custo do produto
margem DECIMAL(10,2) NULL,             -- calculado no ETL: sub_total - custo_total
PRIMARY KEY (sk_venda),
INDEX idx_fato_vendas_calendario (sk_calendario),
INDEX idx_fato_vendas_cliente (sk_cliente),
INDEX idx_fato_vendas_vendedor (sk_vendedor),
INDEX idx_fato_vendas_loja (sk_loja),
INDEX idx_fato_vendas_produto (sk_produto),
INDEX idx_fato_vendas_status (sk_status),
CONSTRAINT fk_fv_calendario FOREIGN KEY (sk_calendario) REFERENCES dim_calendario (sk_calendario),
CONSTRAINT fk_fv_cliente FOREIGN KEY (sk_cliente) REFERENCES dim_cliente (sk_cliente),
CONSTRAINT fk_fv_vendedor FOREIGN KEY (sk_vendedor) REFERENCES dim_vendedor (sk_vendedor),
CONSTRAINT fk_fv_loja FOREIGN KEY (sk_loja) REFERENCES dim_loja (sk_loja),
CONSTRAINT fk_fv_produto FOREIGN KEY (sk_produto) REFERENCES dim_produto (sk_produto),
CONSTRAINT fk_fv_status FOREIGN KEY (sk_status) REFERENCES dim_status_pedido (sk_status)
) ENGINE = InnoDB;

-- Grão: 1 linha por movimentação de estoque
CREATE TABLE IF NOT EXISTS fato_movimentacao_estoque (
sk_movimentacao BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
sk_calendario INT UNSIGNED NOT NULL,
sk_loja INT UNSIGNED NOT NULL,
sk_produto INT UNSIGNED NOT NULL,
id_item_pedido INT UNSIGNED NULL,        -- dimensão degenerada, liga de volta à venda de origem (quando aplicável)
tipo_movimentacao ENUM('Saída','Entrada') NOT NULL,
quantidade INT UNSIGNED NOT NULL,
PRIMARY KEY (sk_movimentacao),
INDEX idx_fme_calendario (sk_calendario),
INDEX idx_fme_loja (sk_loja),
INDEX idx_fme_produto (sk_produto),
CONSTRAINT fk_fme_calendario FOREIGN KEY (sk_calendario) REFERENCES dim_calendario (sk_calendario),
CONSTRAINT fk_fme_loja FOREIGN KEY (sk_loja) REFERENCES dim_loja (sk_loja),
CONSTRAINT fk_fme_produto FOREIGN KEY (sk_produto) REFERENCES dim_produto (sk_produto)
) ENGINE = InnoDB;

-- Grão: 1 linha por mês x loja (fato de planejamento, sem grão diário)
CREATE TABLE IF NOT EXISTS fato_metas (
sk_meta INT UNSIGNED NOT NULL AUTO_INCREMENT,
mes INT UNSIGNED NOT NULL,
sk_loja INT UNSIGNED NOT NULL,
meta_faturamento INT NOT NULL,
meta_pedidos INT NOT NULL,
meta_ticket_medio INT NOT NULL,
PRIMARY KEY (sk_meta),
INDEX idx_fm_loja (sk_loja),
CONSTRAINT fk_fm_loja FOREIGN KEY (sk_loja) REFERENCES dim_loja (sk_loja)
) ENGINE = InnoDB;
 
SET FOREIGN_KEY_CHECKS = 1;



