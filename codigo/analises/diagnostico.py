# DIAGNÓSTICO · números do relatório e do documento de recomendações

''' Recalcula, direto do Data Warehouse, todos os números citados no dashboard e em
docs/05_analise_e_recomendacoes.md. Serve de conferência: se o DW mudar, os
números do texto devem ser atualizados a partir desta saída.

Definições (as mesmas das medidas DAX):
- Receita válida = soma de sub_total dos pedidos não cancelados
- Taxa de cancelamento = pedidos cancelados / total de pedidos
- Atingimento = receita válida / meta de faturamento
- Excesso de estoque = valor a custo acima de 3 meses de cobertura, por loja e produto

Uso (na raiz do projeto):  python -m codigo.analises.diagnostico
'''

import math

import numpy as np
import pandas as pd

from codigo.configuracoes.database import conectar_dw

COBERTURA_SAUDAVEL = 3  # meses


def qui_quadrado(tabela):
    """Teste qui-quadrado de independência; p-valor pela aproximação de Wilson-Hilferty."""
    obs = tabela.to_numpy(float)
    esp = obs.sum(1, keepdims=True) * obs.sum(0, keepdims=True) / obs.sum()
    estat = ((obs - esp) ** 2 / esp).sum()
    gl = (obs.shape[0] - 1) * (obs.shape[1] - 1)
    z = ((estat / gl) ** (1 / 3) - (1 - 2 / (9 * gl))) / math.sqrt(2 / (9 * gl))
    return estat, gl, 0.5 * math.erfc(z / math.sqrt(2))


def main():
    e = conectar_dw()
    vendas = pd.read_sql(
        """SELECT v.id_pedido, v.sub_total, v.custo_total, s.status, c.mes, l.nome_loja, l.regiao, p.nome_categoria
           FROM fato_vendas v JOIN dim_status_pedido s USING(sk_status) JOIN dim_calendario c USING(sk_calendario)
           JOIN dim_loja l USING(sk_loja) JOIN dim_produto p USING(sk_produto)""", e)
    metas = pd.read_sql("SELECT m.*, l.nome_loja FROM fato_metas m JOIN dim_loja l USING(sk_loja)", e)
    mov = pd.read_sql(
        """SELECT m.sk_loja, m.sk_produto, m.tipo_movimentacao, m.quantidade, p.nome_produto, p.custo
           FROM fato_movimentacao_estoque m JOIN dim_produto p USING(sk_produto)""", e)

    pedidos = vendas.groupby("id_pedido").agg(status=("status", "first"), mes=("mes", "first"), regiao=("regiao", "first"),
                                              loja=("nome_loja", "first"), receita=("sub_total", "sum"), custo=("custo_total", "sum"))
    cancelado = pedidos["status"] == "cancelado"
    validos = pedidos[~cancelado]
    receita = validos["receita"].sum()
    meta = metas["meta_faturamento"].sum()

    print("== VISÃO GERAL")
    print(f"pedidos: {len(pedidos):,} · válidos: {len(validos):,} · cancelados: {cancelado.sum():,}")
    print(f"receita válida: R$ {receita/1e6:.2f} Mi · lucro: R$ {(receita - validos['custo'].sum())/1e6:.2f} Mi "
          f"· margem: {1 - validos['custo'].sum()/receita:.1%} · ticket: R$ {receita/len(validos):,.0f}")
    print(f"meta: R$ {meta/1e6:.2f} Mi · atingimento: {receita/meta:.1%}")

    print("\n== CANCELAMENTOS")
    taxa = cancelado.mean()
    perdida = pedidos.loc[cancelado, "receita"].sum()
    print(f"taxa: {taxa:.1%} (meta 3,0% · {taxa/0.03:.1f}x) · receita dos cancelados: R$ {perdida/1e6:.2f} Mi")
    for grupo in ["regiao", "mes", "loja"]:
        t = pedidos.groupby(grupo)["status"].apply(lambda s: (s == "cancelado").mean())
        estat, gl, p = qui_quadrado(pd.crosstab(pedidos[grupo], cancelado))
        print(f"  por {grupo:7}: de {t.min():.1%} a {t.max():.1%} · qui²={estat:.1f} (gl={gl}) · p={p:.2f}")
    cat = vendas.groupby(["id_pedido", "nome_categoria"])["status"].first().reset_index()
    estat, gl, p = qui_quadrado(pd.crosstab(cat["nome_categoria"], cat["status"] == "cancelado"))
    print(f"  por categoria: qui²={estat:.1f} (gl={gl}) · p={p:.2f}")
    for alvo in [0.06, 0.05, 0.03]:
        print(f"  receita recuperável se a taxa cair para {alvo:.0%}: R$ {perdida * (taxa - alvo) / taxa / 1e6:.2f} Mi")

    print("\n== LOJAS x META")
    lojas = validos.groupby("loja")["receita"].sum().to_frame().join(metas.groupby("nome_loja")["meta_faturamento"].sum())
    lojas["ating"] = lojas["receita"] / lojas["meta_faturamento"]
    lojas["gap"] = (lojas["meta_faturamento"] - lojas["receita"]).clip(lower=0)
    abaixo, abaixo90 = lojas[lojas["ating"] < 1], lojas[lojas["ating"] < 0.9]
    print(f"abaixo da meta: {len(abaixo)} de {len(lojas)} · gap R$ {abaixo['gap'].sum()/1e6:.2f} Mi")
    print(f"abaixo de 90%: {len(abaixo90)} lojas · gap R$ {abaixo90['gap'].sum()/1e6:.2f} Mi "
          f"({abaixo90['gap'].sum()/abaixo['gap'].sum():.0%} do gap)")
    print(f"menor atingimento: {lojas['ating'].idxmin()} ({lojas['ating'].min():.0%})")

    print("\n== ESTOQUE")
    mov["entrada"] = np.where(mov["tipo_movimentacao"] == "Entrada", mov["quantidade"], 0)
    mov["saida"] = np.where(mov["tipo_movimentacao"] != "Entrada", mov["quantidade"], 0)
    lp = mov.groupby(["sk_loja", "sk_produto", "nome_produto", "custo"])[["entrada", "saida"]].sum().reset_index()
    lp["final"] = lp["entrada"] - lp["saida"]
    lp["valor"] = lp["final"] * lp["custo"]
    venda_mes = lp["saida"] / 12
    lp["excesso"] = np.where(venda_mes > 0, (lp["final"] - COBERTURA_SAUDAVEL * venda_mes).clip(lower=0), lp["final"]) * lp["custo"]
    cmv_mes = (lp["saida"] * lp["custo"]).sum() / 12
    print(f"estoque final: R$ {lp['valor'].sum()/1e6:.2f} Mi a custo · {lp['valor'].sum()/cmv_mes:.1f} meses de venda")
    print(f"acima de {COBERTURA_SAUDAVEL} meses: R$ {lp['excesso'].sum()/1e6:.2f} Mi ({lp['excesso'].sum()/lp['valor'].sum():.0%})")
    sem_venda = lp[lp["saida"] == 0]
    print(f"loja-produto sem venda no ano: {len(sem_venda)} · R$ {sem_venda['valor'].sum()/1e3:.0f} mil")
    prod = lp.groupby("nome_produto")["excesso"].sum().sort_values(ascending=False)
    n50 = int((prod.cumsum() / prod.sum() <= 0.5).sum()) + 1
    print(f"{n50} de {len(prod)} produtos concentram metade do excesso: {', '.join(prod.index[:n50])}")
    for f in [0.4, 0.7]:
        print(f"  liberar {f:.0%} do excesso: R$ {lp['excesso'].sum() * f / 1e6:.2f} Mi em caixa")


if __name__ == "__main__":
    main()
