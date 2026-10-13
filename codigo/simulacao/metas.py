# METAS

''' Define as metas comerciais de cada loja para cada mês do ano.

A meta parte da venda média por loja da região naquele mês (o que é realista
esperar) e aplica um fator de desafio entre FATOR_META_MINIMO e FATOR_META_MAXIMO.
Por isso as metas são geradas depois dos pedidos e itens, e acompanham a escala
de qualquer modo de execução (desenvolvimento, teste ou produção). '''

import random

import pandas as pd

from codigo.configuracoes.configuracao import FATOR_META_MAXIMO, FATOR_META_MINIMO


def gerar_metas(dados):

    lojas = dados.lojas.merge(dados.estados[["id_estado", "regiao"]], on="id_estado")
    lojas_por_regiao = lojas.groupby("regiao")["id_loja"].nunique()

    receita_pedido = dados.itens_pedido.groupby("id_pedido", as_index=False)["sub_total"].sum()
    validos = (
        dados.pedidos[dados.pedidos["status"] != "cancelado"]
        .merge(dados.calendario[["id_calendario", "mes"]], on="id_calendario")
        .merge(receita_pedido, on="id_pedido")
        .merge(lojas[["id_loja", "regiao"]], on="id_loja")
    )
    base = validos.groupby(["regiao", "mes"]).agg(receita=("sub_total", "sum"), pedidos=("id_pedido", "nunique"))
    regioes = base.index.get_level_values("regiao")
    base["receita_media_loja"] = base["receita"] / regioes.map(lojas_por_regiao)
    base["pedidos_media_loja"] = base["pedidos"] / regioes.map(lojas_por_regiao)

    df_metas = []
    id_meta = 1

    for mes in range(1, 13):
        for i, loja in lojas.iterrows():
            media = base.loc[(loja["regiao"], mes)]
            meta_faturamento = round(media["receita_media_loja"] * random.uniform(FATOR_META_MINIMO, FATOR_META_MAXIMO), -2)
            meta_pedidos = max(1, round(media["pedidos_media_loja"] * random.uniform(FATOR_META_MINIMO, FATOR_META_MAXIMO)))

            df_metas.append({
                "id_meta": id_meta,
                "mes": mes,
                "id_loja": loja["id_loja"],
                "meta_faturamento": int(meta_faturamento),
                "meta_pedidos": meta_pedidos,
                "meta_ticket_medio": round(meta_faturamento / meta_pedidos, 2)
            })
            id_meta += 1
    return pd.DataFrame(df_metas)

if __name__ == "__main__":

    from codigo.geradores.apoio.motor_simulacao import executar_simulacao

    dados = executar_simulacao()
    print(dados.metas)
