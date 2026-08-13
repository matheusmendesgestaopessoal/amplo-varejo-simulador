from pathlib import Path

import pandas as pd
from sqlalchemy import text

from codigo.configuracoes.database import conectar_mysql


def exportar_mysql():

    engine = conectar_mysql()
    pasta = Path("dados/brutos_csv")
    tabelas = [
        "calendario",
        "sazonalidade",
        "campanhas",
        "eventos",
        "estados",
        "lojas",
        "clientes",
        "vendedores",
        "categorias",
        "produtos",
        "metas",
        "pedidos",
        "itens_pedido",
        "estoque",
        "movimentacao_estoque"
    ]

    with engine.begin() as conexao:

        print("\nLimpando banco...")

        conexao.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

        for tabela in reversed(tabelas):
            conexao.execute(text(f"TRUNCATE TABLE {tabela};"))

        conexao.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    print("Banco limpo com sucesso.\n")

    print("Importando tabelas...\n")

    

    for tabela in tabelas:

        caminho = pasta / f"{tabela}.csv"

        if not caminho.exists():
            print(f"{tabela:<25} Arquivo não encontrado")
            continue
        try:
            df = pd.read_csv(caminho,sep=";")
            df.to_sql(tabela,engine,if_exists="append",index=False)
            print(f"{tabela:<25} OK")
        except Exception as erro:
            print(f"{tabela:<25} ERRO")
            print(erro)

    print("\nImportação finalizada.")

if __name__ == "__main__":
    exportar_mysql()