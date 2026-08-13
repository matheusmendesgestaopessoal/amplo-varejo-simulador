def validar_estoque(dados):

    print("\n===== VALIDAÇÃO DE ESTOQUE =====")

    valido = True

    # Estoque negativo
    estoque_negativo = dados.estoque[
        dados.estoque["quantidade"] < 0
    ]

    if len(estoque_negativo) > 0:

        print(
            f"ERRO: {len(estoque_negativo)} "
            f"registros com estoque negativo."
        )

        valido = False

    else:

        print("OK: nenhum estoque negativo.")

    # Movimentações
    if not dados.movimentacao_estoque.empty:

        saidas = dados.movimentacao_estoque[
            dados.movimentacao_estoque["tipo_movimentacao"]
            == "Saída"
        ]

        print(
            f"Saídas de estoque: {len(saidas)}"
        )

        entradas = dados.movimentacao_estoque[
            dados.movimentacao_estoque["tipo_movimentacao"]
            == "Entrada"
        ]

        print(
            f"Entradas de estoque: {len(entradas)}"
        )
    return valido