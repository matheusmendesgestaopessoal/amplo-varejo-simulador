def validar_cobertura(dados):

    print("\n===== VALIDAÇÃO DE COBERTURA =====")

    # Estados com lojas
    estados_com_lojas = dados.lojas["id_estado"].nunique()
    total_estados = len(dados.estados)

    print(
        f"Estados com lojas: "
        f"{estados_com_lojas}/{total_estados}"
    )

    # Lojas com vendedores
    lojas_com_vendedores = dados.vendedores["id_loja"].nunique()
    total_lojas = len(dados.lojas)

    print(
        f"Lojas com vendedores: "
        f"{lojas_com_vendedores}/{total_lojas}"
    )

    # Lojas com clientes
    lojas_com_clientes = dados.clientes["id_loja"].nunique()

    print(
        f"Lojas com clientes: "
        f"{lojas_com_clientes}/{total_lojas}"
    )

    # Estados com pedidos
    estados_com_pedidos = dados.pedidos.merge(
        dados.lojas,
        on="id_loja"
    )["id_estado"].nunique()

    print(
        f"Estados com pedidos: "
        f"{estados_com_pedidos}/{total_estados}"
    )
    return True