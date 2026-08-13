# GERADOR DE VENDEDORES

import pandas as pd
import random

from codigo.utilitarios.faker import fake
from codigo.configuracoes.configuracao import QUANTIDADE_VENDEDORES



def gerar_vendedores(df_lojas):
    df_vendedores = []
    quantidade_lojas = len(df_lojas)
    vendedor_por_loja = ( QUANTIDADE_VENDEDORES // quantidade_lojas )
    vendedores_restantes = ( QUANTIDADE_VENDEDORES % quantidade_lojas )
    id_vendedor = 1

    for indice, loja in df_lojas.iterrows():
        quantidade = vendedor_por_loja

        if indice < vendedores_restantes:
            quantidade += 1

        for i in range(quantidade):

            df_vendedores.append({
                "id_vendedor": id_vendedor,
                "nome_vendedor": fake.name(),
                "cpf_vendedor": fake.cpf(),
                "email": fake.email(),
                "data_admissao": fake.date_between(start_date="-10y", end_date="today"),
                "id_loja": loja["id_loja"]})
            id_vendedor += 1
            
    return pd.DataFrame(df_vendedores)

if __name__ == "__main__":

    from codigo.geradores.mestres.lojas import gerar_lojas
    from codigo.geradores.mestres.estados import gerar_estados

    df_lojas = gerar_lojas(gerar_estados())
    df_vendedores = gerar_vendedores(df_lojas)
    print(df_vendedores)
    
