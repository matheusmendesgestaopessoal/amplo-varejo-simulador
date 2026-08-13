# METAS

''' Define as metas comerciais da empresa para cada mês do ano.
Essas metas serão utilizadas para comparação com as vendas
geradas pelo simulador. '''

import pandas as pd
import random

def gerar_metas(dados):

    df_metas = []
    id_meta = 1

    for mes in range(1,13):
        for i, loja in dados.lojas.iterrows():
            meta_faturamento = random.randint(500000, 900000)
            meta_pedidos = random.randint(900, 1800)

            df_metas.append({
                "id_meta": id_meta,
                "mes": mes,
                "id_loja": loja["id_loja"],
                "meta_faturamento": meta_faturamento,
                "meta_pedidos": meta_pedidos,
                "meta_ticket_medio": round(meta_faturamento / meta_pedidos, 2)
            })
            id_meta += 1
    return pd.DataFrame(df_metas)

if __name__ == "__main__":

    from codigo.geradores.apoio.motor_simulacao import executar_simulacao

    dados = executar_simulacao()
    df_metas = gerar_metas(dados)
    print(df_metas)