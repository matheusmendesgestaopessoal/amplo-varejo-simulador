import random
import pandas as pd

from codigo.configuracoes.configuracao import ITENS_MINIMOS_PEDIDO, ITENS_MAXIMOS_PEDIDO, QUANTIDADE_MINIMA_ITEM, QUANTIDADE_MAXIMA_ITEM
from codigo.utilitarios.catalogo_produtos import PESO_CATEGORIA
from codigo.simulacao.demanda import calcular_peso_categorias_dia

def gerar_itens_pedido(dados):

    df_itens_pedido = []
    id_item = 1
    pedidos_com_data = dados.pedidos.merge(
        dados.calendario[["id_calendario", "data"]], on="id_calendario"
    )

    for i, pedido in pedidos_com_data.iterrows():

        pesos_categoria_dia = calcular_peso_categorias_dia(dados, pedido["data"])
        pesos_produto = dados.produtos["categoria"].map(pesos_categoria_dia)

        quantidade_itens = random.randint(ITENS_MINIMOS_PEDIDO, ITENS_MAXIMOS_PEDIDO)
        quantidade_itens = min(quantidade_itens, len(dados.produtos))

        produtos_do_pedido = dados.produtos.sample(
            n=quantidade_itens, replace=False, weights=pesos_produto
        )

        for i, produto in produtos_do_pedido.iterrows():
            quantidade_por_produtos = random.randint(QUANTIDADE_MINIMA_ITEM, QUANTIDADE_MAXIMA_ITEM)
            preco_unitario = produto["preco"]
            desconto = 0.00
            valor_item = round((preco_unitario * quantidade_por_produtos) - desconto,2)
            df_itens_pedido.append({
                "id_item_pedido": id_item,
                "id_pedido": pedido["id_pedido"],
                "id_produto": produto["id_produto"],
                "quantidade": quantidade_por_produtos,
                "valor_unitario": preco_unitario,
                "desconto": desconto,
                "sub_total": valor_item,})
            id_item += 1
    return pd.DataFrame(df_itens_pedido)

if __name__ == "__main__":

    from codigo.geradores.apoio.motor_simulacao import executar_simulacao
    dados = executar_simulacao()
    dados.itens_pedido = gerar_itens_pedido(dados)

    print(dados.itens_pedido.head())

    print(f"\nItens gerados: {len(dados.itens_pedido)}")


