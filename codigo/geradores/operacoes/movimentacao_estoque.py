# MOVIMENTAÇAO ESTOQUE

import pandas as pd

def gerar_movimentacao_estoque(dados):

    df_movimentacoes = []
    id_movimentacao = 1

    for i, item in dados.itens_pedido.iterrows():

        pedido = dados.pedidos[dados.pedidos["id_pedido"] == item["id_pedido"]].iloc[0]

        if pedido["status"] not in ["pago", "enviado"]:
            continue

        estoque = dados.estoque[
            (dados.estoque["id_loja"] == pedido["id_loja"]) &
            (dados.estoque["id_produto"] == item["id_produto"])
        ].iloc[0]

        df_movimentacoes.append({
            "id_movimentacao": id_movimentacao,
            "id_estoque": estoque["id_estoque"],
            "id_item_pedido": item["id_item_pedido"],
            "tipo_movimentacao": "Saída",
            "quantidade": item["quantidade"],
            "id_calendario": pedido["id_calendario"]
        })
        id_movimentacao += 1

    return pd.DataFrame(df_movimentacoes)

if __name__ == "__main__":

    from codigo.geradores.apoio.motor_simulacao import executar_simulacao

    dados = executar_simulacao()
    df_movimentacao = gerar_movimentacao_estoque(dados)
    print(df_movimentacao.head())

