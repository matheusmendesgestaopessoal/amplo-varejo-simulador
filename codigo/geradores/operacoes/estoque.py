# GERADOR DE ESTOQUE

''' Gera o estoque inicial de cada produto em cada loja.

O estoque inicial cobre as vendas do ano (pedidos pagos ou enviados) e deixa uma
sobra equivalente a COBERTURA_MINIMA_MESES..COBERTURA_MAXIMA_MESES meses de venda.
Assim nenhum saldo fica negativo e o estoque acompanha a escala da simulação. '''

import random

import pandas as pd

from codigo.configuracoes.configuracao import COBERTURA_MAXIMA_MESES, COBERTURA_MINIMA_MESES


def gerar_estoque(dados):

    vendidos = (
        dados.itens_pedido
        .merge(dados.pedidos[["id_pedido", "id_loja", "status"]], on="id_pedido")
        .query("status in ['pago', 'enviado']")
        .groupby(["id_loja", "id_produto"])["quantidade"].sum()
    )

    df_estoque = []
    id_estoque = 1

    for i, loja in dados.lojas.iterrows():
        for i, produto in dados.produtos.iterrows():

            vendas_ano = int(vendidos.get((loja["id_loja"], produto["id_produto"]), 0))
            meses_cobertura = random.uniform(COBERTURA_MINIMA_MESES, COBERTURA_MAXIMA_MESES)
            sobra = max(1, round(vendas_ano / 12 * meses_cobertura))

            df_estoque.append({
                "id_estoque": id_estoque,
                "id_loja": loja["id_loja"],
                "id_produto": produto["id_produto"],
                "quantidade": vendas_ano + sobra
                })
            id_estoque += 1
    return pd.DataFrame(df_estoque)

if __name__ == "__main__":

    from codigo.geradores.apoio.motor_simulacao import executar_simulacao

    dados = executar_simulacao()
    print(dados.estoque.head())
    print(f"\nTotal registros: {len(dados.estoque)}")
