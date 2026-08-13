# SAZONALIDADE

''' Define o comportamento esperado das vendas ao longo do ano.
Os índices serão utilizados pelo motor de simulação para
ajustar o volume diário de pedidos. '''

import pandas as pd


def gerar_sazonalidade():

    df_sazonalidade = [{
            "mes": 1,
            "nome_mes": "Janeiro",
            "indice_vendas": 0.95,
            "classificacao": "Baixa",
            "descricao": "Pós-Natal, redução no consumo."
        },
        {
            "mes": 2,
            "nome_mes": "Fevereiro",
            "indice_vendas": 0.90,
            "classificacao": "Baixa",
            "descricao": "Mês mais curto e menor volume de vendas."
        },
        {
            "mes": 3,
            "nome_mes": "Março",
            "indice_vendas": 1.00,
            "classificacao": "Normal",
            "descricao": "Mercado estabilizado."
        },
        {
            "mes": 4,
            "nome_mes": "Abril",
            "indice_vendas": 0.98,
            "classificacao": "Normal",
            "descricao": "Pequena desaceleração."
        },
        {
            "mes": 5,
            "nome_mes": "Maio",
            "indice_vendas": 1.10,
            "classificacao": "Alta",
            "descricao": "Aumento devido ao Dia das Mães."
        },
        {
            "mes": 6,
            "nome_mes": "Junho",
            "indice_vendas": 1.03,
            "classificacao": "Normal",
            "descricao": "Estabilidade."
        },
        {
            "mes": 7,
            "nome_mes": "Julho",
            "indice_vendas": 1.05,
            "classificacao": "Normal",
            "descricao": "Férias escolares."
        },
        {
            "mes": 8,
            "nome_mes": "Agosto",
            "indice_vendas": 0.97,
            "classificacao": "Normal",
            "descricao": "Pequena retração."
        },
        {
            "mes": 9,
            "nome_mes": "Setembro",
            "indice_vendas": 1.02,
            "classificacao": "Normal",
            "descricao": "Retomada gradual."
        },
        {
            "mes": 10,
            "nome_mes": "Outubro",
            "indice_vendas": 1.08,
            "classificacao": "Alta",
            "descricao": "Dia das Crianças."
        },
        {
            "mes": 11,
            "nome_mes": "Novembro",
            "indice_vendas": 1.20,
            "classificacao": "Muito Alta",
            "descricao": "Black Friday."
        },
        {
            "mes": 12,
            "nome_mes": "Dezembro",
            "indice_vendas": 1.35,
            "classificacao": "Muito Alta",
            "descricao": "Natal e compras de fim de ano."
        }]
    return pd.DataFrame(df_sazonalidade)

if __name__ == "__main__":

    df_sazonalidade = gerar_sazonalidade()
    print(df_sazonalidade)