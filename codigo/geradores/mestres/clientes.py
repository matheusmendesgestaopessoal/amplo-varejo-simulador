# GERADOR DE CLIENTES

import pandas as pd
from codigo.utilitarios.faker import fake
from codigo.configuracoes.configuracao import QUANTIDADE_CLIENTES

def gerar_clientes(dados):
    df_clientes = []
    df_lojas = dados.lojas
    id_cliente = 1

    for i, loja in df_lojas.iterrows():
        df_clientes.append({
            "id_cliente": id_cliente,
            "nome_cliente": fake.name(),
            "cpf_cliente": fake.unique.cpf(),
            "email": fake.unique.email(),
            "cidade": fake.city(),
            "id_loja": loja["id_loja"]
        })
        id_cliente += 1

    while id_cliente <= QUANTIDADE_CLIENTES:

        loja = df_lojas.sample(1).iloc[0]

        df_clientes.append({
            "id_cliente": id_cliente,
            "nome_cliente": fake.name(),
            "cpf_cliente": fake.unique.cpf(),
            "email": fake.unique.email(),
            "cidade": fake.city(),
            "id_loja": loja["id_loja"]
        })
        id_cliente += 1
    return pd.DataFrame(df_clientes)

if __name__ == "__main__":
    df_clientes = gerar_clientes()
    print(df_clientes.head())
    