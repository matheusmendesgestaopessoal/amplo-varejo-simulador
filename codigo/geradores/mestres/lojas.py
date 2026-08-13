# GERADOR DE LOJAS

import random
import pandas as pd
from codigo.configuracoes.configuracao import QUANTIDADE_LOJAS
from codigo.utilitarios.faker import fake
from codigo.utilitarios.regioes import pesos # Dicionario de porcetagem por regioes

def gerar_lojas(df_estados):
    df_lojas = []
    id_loja = 1

    for regiao, percentual in pesos.items():
        estados = df_estados[df_estados["regiao"] == regiao]
        quantidade_lojas = round(QUANTIDADE_LOJAS * percentual / 100)
        quantidade_lojas = max(quantidade_lojas, len(estados))
        estados_escolhidos = list(estados["id_estado"])

        while len(estados_escolhidos) < quantidade_lojas:
            estados_escolhidos.append(random.choice(list(estados["id_estado"])))
    
        for id_estado in estados_escolhidos:
            estado = estados[estados["id_estado"] == id_estado].iloc[0]

            df_lojas.append({
                "id_loja": id_loja,
                "nome_loja": (
                    f"Amplo Varejo - "
                    f"{estado['uf']} {id_loja:03}"
                ),
                "endereco": fake.address(),
                "id_estado": id_estado
            })
            id_loja += 1

    return pd.DataFrame(df_lojas)

if __name__ == "__main__":

    from codigo.geradores.mestres.estados import gerar_estados

    df_estados = gerar_estados()
    df_lojas = gerar_lojas(df_estados)
    
    print(df_lojas)

