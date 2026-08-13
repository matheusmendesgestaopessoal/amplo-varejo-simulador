from pathlib import Path

def exportar_csv(dados):

    pasta = Path("dados/brutos_csv")
    pasta.mkdir(parents=True, exist_ok=True)

    tabelas = {
        "calendario": dados.calendario,
        "sazonalidade": dados.sazonalidade,
        "campanhas": dados.campanhas,
        "eventos": dados.eventos,
        "metas": dados.metas,
        "estados": dados.estados,
        "lojas": dados.lojas,
        "vendedores": dados.vendedores,
        "categorias": dados.categorias,
        "produtos": dados.produtos,
        "clientes": dados.clientes,
        "pedidos": dados.pedidos,
        "itens_pedido": dados.itens_pedido,
        "estoque": dados.estoque,
        "movimentacao_estoque": dados.movimentacao_estoque
        }
    
    print("\nExportando CSVs...\n")

    for nome, tabela in tabelas.items():
        if tabela is None:
            continue

        caminho = pasta / f"{nome}.csv"
        tabela.to_csv(caminho, index=False, sep=";",encoding="utf-8-sig")

        print(f"{nome:<25} OK")

    print("\nTodos os arquivos foram exportados.")
        