# GERADOR DE CATEGORIAS

import pandas as pd

def gerar_categorias():
    df_categorias = [
        {
            "id_categoria": 1,
            "nome_categoria": "Casa",
            "descricao": "Móveis, decoração e utilidades domésticas"
        },
        {
            "id_categoria": 2,
            "nome_categoria": "Eletro",
            "descricao": "Linha branca, linha marrom e pequenos eletrodomésticos"
        },
        {
            "id_categoria": 3,
            "nome_categoria": "Tecnologia",
            "descricao": "Celulares, informática e acessórios"
        },
        {
            "id_categoria": 4,
            "nome_categoria": "Escritório",
            "descricao": "Papelaria, mobiliário corporativo e suprimentos"
        }
    ]
    return pd.DataFrame(df_categorias)

if __name__ == "__main__":

    df_categorias = gerar_categorias()
    print(df_categorias)

    