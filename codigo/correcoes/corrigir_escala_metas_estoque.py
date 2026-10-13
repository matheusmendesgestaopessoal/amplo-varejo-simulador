# CORREÇÃO DE ESCALA · METAS E ESTOQUE (2026-10-12)

''' Corrige a escala das metas e do estoque inicial nos dados já gerados,
sem gerar nenhum pedido novo.

Problema encontrado:
- As metas eram sorteadas entre R$ 500 mil e R$ 900 mil por loja/mês, valores
  calibrados para o modo "producao". No modo "desenvolvimento" (o dos dados
  publicados), cada loja vende ~R$ 33 mil/mês: a meta ficava ~20x acima da venda.
- O estoque inicial era sorteado entre 20 e 500 unidades por loja/produto,
  enquanto cada loja vende ~6 unidades de cada produto no ano: todo produto
  parecia parado.

Correção (determinística, preserva a variação aleatória original de cada linha):
- Meta de faturamento da loja no mês = venda média por loja da região no mês
  x fator de desafio entre 0,95 e 1,15, derivado do sorteio original.
  Mesma lógica para a meta de pedidos.
- Estoque inicial = unidades vendidas da loja/produto no ano + sobra no fim do
  ano equivalente a 0,5 a 6 meses de venda (cobertura), proporcional ao sorteio
  original. Mínimo de 1 unidade de sobra.

Uso (na raiz do projeto):
    python -m codigo.correcoes.corrigir_escala_metas_estoque
Depois recarregue o banco e o DW:
    python -c "from codigo.exportadores.exportar_mysql import exportar_mysql; exportar_mysql()"
    python -c "from codigo.dw.atualizar_dw import executar_carga_dw; executar_carga_dw()"
'''

from pathlib import Path

import pandas as pd

PASTA = Path("dados/brutos_csv")
LER = dict(sep=";", encoding="utf-8-sig")
SALVAR = dict(sep=";", encoding="utf-8-sig", index=False, lineterminator="\r\n")  # mesmo formato dos CSVs originais

# Faixas do sorteio original (codigo/simulacao/metas.py e configuracao.py)
META_FAT_MIN, META_FAT_MAX = 500_000, 900_000
META_PED_MIN, META_PED_MAX = 900, 1_800
ESTOQUE_MIN, ESTOQUE_MAX = 20, 500

# Novas faixas
FATOR_MIN, FATOR_MAX = 0.95, 1.15   # desafio da meta: de 5% abaixo a 15% acima da média
COBERTURA_MIN, COBERTURA_MAX = 0.5, 6.0   # meses de venda que sobram em estoque no fim do ano


def _fator(valor, minimo, maximo):
    """Converte o sorteio original (minimo..maximo) num fator de desafio (0,95..1,15)."""
    return FATOR_MIN + (FATOR_MAX - FATOR_MIN) * (valor - minimo) / (maximo - minimo)


def corrigir():
    metas = pd.read_csv(PASTA / "metas.csv", **LER)

    if metas["meta_faturamento"].max() < META_FAT_MIN:
        print("Correção já aplicada (metas já estão na escala nova). Nada a fazer.")
        return

    pedidos = pd.read_csv(PASTA / "pedidos.csv", **LER)
    itens = pd.read_csv(PASTA / "itens_pedido.csv", **LER)
    calendario = pd.read_csv(PASTA / "calendario.csv", **LER)
    lojas = pd.read_csv(PASTA / "lojas.csv", **LER)
    estados = pd.read_csv(PASTA / "estados.csv", **LER)
    estoque = pd.read_csv(PASTA / "estoque.csv", **LER)
    movimentacao = pd.read_csv(PASTA / "movimentacao_estoque.csv", **LER)

    # ---------------- vendas válidas (sem cancelados) por loja/mês ----------------
    lojas = lojas.merge(estados[["id_estado", "regiao"]], on="id_estado")
    validos = pedidos[pedidos["status"] != "cancelado"].merge(
        calendario[["id_calendario", "mes"]], on="id_calendario"
    )
    receita_pedido = itens.groupby("id_pedido", as_index=False)["sub_total"].sum()
    validos = validos.merge(receita_pedido, on="id_pedido").merge(lojas[["id_loja", "regiao"]], on="id_loja")

    lojas_por_regiao = lojas.groupby("regiao")["id_loja"].nunique()
    por_regiao_mes = validos.groupby(["regiao", "mes"]).agg(receita=("sub_total", "sum"), pedidos=("id_pedido", "nunique"))
    por_regiao_mes["receita_media_loja"] = por_regiao_mes["receita"] / por_regiao_mes.index.get_level_values("regiao").map(lojas_por_regiao)
    por_regiao_mes["pedidos_media_loja"] = por_regiao_mes["pedidos"] / por_regiao_mes.index.get_level_values("regiao").map(lojas_por_regiao)

    # ---------------- metas ----------------
    metas = metas.merge(lojas[["id_loja", "regiao"]], on="id_loja")
    base = por_regiao_mes.loc[list(zip(metas["regiao"], metas["mes"]))]
    metas["meta_faturamento"] = (
        base["receita_media_loja"].to_numpy() * _fator(metas["meta_faturamento"], META_FAT_MIN, META_FAT_MAX)
    ).round(-2).astype(int)
    metas["meta_pedidos"] = (
        base["pedidos_media_loja"].to_numpy() * _fator(metas["meta_pedidos"], META_PED_MIN, META_PED_MAX)
    ).round().clip(lower=1).astype(int)
    metas["meta_ticket_medio"] = (metas["meta_faturamento"] / metas["meta_pedidos"]).round(2)
    metas = metas.drop(columns="regiao")

    # ---------------- estoque inicial ----------------
    saidas = movimentacao[movimentacao["tipo_movimentacao"] == "Saída"]
    vendidas = estoque["id_estoque"].map(saidas.groupby("id_estoque")["quantidade"].sum()).fillna(0)
    meses = COBERTURA_MIN + (COBERTURA_MAX - COBERTURA_MIN) * (estoque["quantidade"] - ESTOQUE_MIN) / (ESTOQUE_MAX - ESTOQUE_MIN)
    sobra = (vendidas / 12 * meses).round().clip(lower=1)
    estoque["quantidade"] = (vendidas + sobra).astype(int)

    entradas = movimentacao["tipo_movimentacao"] == "entrada"
    movimentacao.loc[entradas, "quantidade"] = (
        movimentacao.loc[entradas, "id_estoque"].map(estoque.set_index("id_estoque")["quantidade"]).astype(float)
    )

    metas.to_csv(PASTA / "metas.csv", **SALVAR)
    estoque.to_csv(PASTA / "estoque.csv", **SALVAR)
    movimentacao.to_csv(PASTA / "movimentacao_estoque.csv", **SALVAR)

    print(f"Metas corrigidas: R$ {metas['meta_faturamento'].sum()/1e6:.2f} Mi no ano "
          f"(vendas válidas: R$ {validos['sub_total'].sum()/1e6:.2f} Mi)")
    print(f"Estoque inicial corrigido: {estoque['quantidade'].sum():,} unidades "
          f"(vendidas no ano: {int(vendidas.sum()):,})")


if __name__ == "__main__":
    corrigir()
