# GERADOR DE PRODUTOS

import pandas as pd

from codigo.utilitarios.catalogo_produtos import PRODUTOS


def gerar_produtos(dados):
    df_produtos = []
    id_produto = 1

    for i, categoria in dados.categorias.iterrows():

        categoria_produto = categoria["nome_categoria"]

        for produto in PRODUTOS[categoria_produto]:

            df_produtos.append({
            "id_produto": id_produto,
            "nome_produto": produto["nome"],
            "categoria": categoria_produto,
            "preco": produto["preco_venda"],
            "custo": produto["custo"],
            "ativo": True,
            "id_categoria": categoria["id_categoria"]
            })
            id_produto += 1

    return pd.DataFrame(df_produtos)


if __name__ == "__main__":

    from codigo.geradores.mestres.categorias import gerar_categorias
    from codigo.geradores.apoio.motor_simulacao import executar_simulacao

    dados = executar_simulacao()
    df_categorias = gerar_categorias()
    df_produtos = gerar_produtos(dados)
    print(df_produtos)

