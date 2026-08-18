import random
import pandas as pd

from codigo.simulacao.demanda import calcular_demanda_dia

def gerar_pedidos(dados):

    df_pedidos = []
    id_pedido = 1
    lojas_com_regiao = dados.lojas.merge(dados.estados[["id_estado", "regiao"]], on="id_estado")
    regioes = lojas_com_regiao["regiao"].unique()

    for i, linha in dados.calendario.iterrows():
        data = linha["data"]

        for regiao in regioes:
            quantidade_pedidos = calcular_demanda_dia(dados, data, regiao)
            lojas_regiao = lojas_com_regiao[lojas_com_regiao["regiao"] == regiao]

            for i in range(quantidade_pedidos):

                loja = lojas_regiao.sample(1).iloc[0]
                clientes_loja = dados.clientes[dados.clientes["id_loja"] == loja["id_loja"]]
                vendedores_loja = dados.vendedores[dados.vendedores["id_loja"] == loja["id_loja"]]

                if clientes_loja.empty or vendedores_loja.empty:
                    continue
                
                cliente = clientes_loja.sample(1).iloc[0]
                vendedor = vendedores_loja.sample(1).iloc[0]

                status = random.choices(["pendente", "pago", "cancelado", "enviado"],
                                        weights=[5, 81, 9, 5],k=1)[0]

                df_pedidos.append({
                    "id_pedido": id_pedido,
                    "id_calendario": linha["id_calendario"],
                    "id_cliente": cliente["id_cliente"],
                    "id_vendedor": vendedor["id_vendedor"],
                    "id_loja": loja["id_loja"],
                    "status": status })
                id_pedido += 1
    return pd.DataFrame(df_pedidos)

if __name__ == "__main__":

    from codigo.geradores.apoio.dados_simulacao import DadosSimulacao
    from codigo.simulacao.calendario import gerar_calendario
    from codigo.geradores.mestres.clientes import gerar_clientes
    from codigo.geradores.mestres.estados import gerar_estados
    from codigo.geradores.mestres.lojas import gerar_lojas
    from codigo.geradores.mestres.vendedores import gerar_vendedores
    from codigo.simulacao.demanda import calcular_demanda_dia
    from codigo.simulacao.sazonalidade import gerar_sazonalidade
    from codigo.simulacao.campanhas import gerar_campanhas
    from codigo.simulacao.eventos import gerar_eventos

    dados = DadosSimulacao()

    dados.sazonalidade = gerar_sazonalidade()
    dados.campanhas = gerar_campanhas()
    dados.eventos = gerar_eventos()

    dados.calendario = gerar_calendario()

    dados.estados = gerar_estados()
    dados.lojas = gerar_lojas(dados.estados)
    dados.vendedores = gerar_vendedores(dados.lojas)
    dados.clientes = gerar_clientes()

    df_pedidos = gerar_pedidos(dados)

    print(df_pedidos.head(10))
    print(f"\nTotal de pedidos: {len(df_pedidos)}")