def validar_integridade(dados):

    print("\n===== VALIDAÇÃO DE INTEGRIDADE =====")

    erros = 0

    # Cliente precisa existir
    clientes_invalidos = dados.pedidos[
        ~dados.pedidos["id_cliente"].isin(
            dados.clientes["id_cliente"]
        )
    ]

    if len(clientes_invalidos) > 0:
        print(
            f"ERRO: {len(clientes_invalidos)} "
            f"pedidos possuem cliente inválido."
        )
        erros += 1

    # Vendedor precisa existir
    vendedores_invalidos = dados.pedidos[
        ~dados.pedidos["id_vendedor"].isin(
            dados.vendedores["id_vendedor"]
        )
    ]

    if len(vendedores_invalidos) > 0:
        print(
            f"ERRO: {len(vendedores_invalidos)} "
            f"pedidos possuem vendedor inválido."
        )
        erros += 1

    # Loja precisa existir
    lojas_invalidas = dados.pedidos[
        ~dados.pedidos["id_loja"].isin(
            dados.lojas["id_loja"]
        )
    ]

    if len(lojas_invalidas) > 0:
        print(
            f"ERRO: {len(lojas_invalidas)} "
            f"pedidos possuem loja inválida."
        )
        erros += 1

    # Produto precisa existir
    produtos_invalidos = dados.itens_pedido[
        ~dados.itens_pedido["id_produto"].isin(
            dados.produtos["id_produto"]
        )
    ]

    if len(produtos_invalidos) > 0:
        print(
            f"ERRO: {len(produtos_invalidos)} "
            f"itens possuem produto inválido."
        )
        erros += 1

    if erros == 0:
        print("OK: nenhuma inconsistência encontrada.")
        return True

    return False
        