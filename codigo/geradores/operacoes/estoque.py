# GERADOR DE ESTOQUE

import random
import pandas as pd

from codigo.configuracoes.configuracao import ESTOQUE_MINIMO, ESTOQUE_MAXIMO

def gerar_estoque(dados):

    df_estoque = []
    id_estoque = 1

    for i, loja in dados.lojas.iterrows():
        for i, produto in dados.produtos.iterrows():

            quantidade_produto_estoque = random.randint(ESTOQUE_MINIMO, ESTOQUE_MAXIMO)

            df_estoque.append({
                "id_estoque": id_estoque,
                "id_loja": loja["id_loja"],
                "id_produto": produto["id_produto"],
                "quantidade": quantidade_produto_estoque
                })
            id_estoque += 1
    return pd.DataFrame(df_estoque)

if __name__ == "__main__":

    from codigo.geradores.apoio.motor_simulacao import executar_simulacao

    dados = executar_simulacao()
    df_estoque = gerar_estoque(dados)
    print(df_estoque.head())
    print(f"\nTotal registros: {len(df_estoque)}")

