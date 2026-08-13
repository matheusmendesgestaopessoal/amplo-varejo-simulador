# GERADOR DE REGIÕES

import pandas as pd

from codigo.utilitarios.regioes import ESTADOS_REGIOES

def gerar_estados():

    df_estados = []

    for id_estado, item in enumerate(ESTADOS_REGIOES.items(), start=1):
        chave, valor = item
        estado, regiao = valor

        df_estados.append({
        "id_estado": id_estado,
        "nome_estado": estado,
        "uf": chave,
        "regiao": regiao
        })
    return pd.DataFrame(df_estados)

if __name__ == "__main__":

    df_estados = gerar_estados()    
    print(df_estados)
