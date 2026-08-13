# CATALOGO DE EVENTOS

''' Define os eventos extraordinários que podem ocorrer
durante a simulação e alterar o comportamento das vendas. '''

import pandas as pd


def gerar_eventos():
    eventos = [
    {
        "id_evento": 1,
        "nome_evento": "Entrada de Concorrente",
        "tipo": "Mercado",
        "categoria": "Todas",
        "regiao": "Sudeste",
        "probabilidade": 0.03,
        "impacto_vendas": -0.20,
        "duracao_dias": 90,
        "prioridade": 3,
        "ativo": True,
        "descricao": "Novo concorrente reduz as vendas da região."
    },
    {
        "id_evento": 2,
        "nome_evento": "Campanha Nacional",
        "tipo": "Marketing",
        "categoria": "Todas",
        "regiao": "Todas",
        "probabilidade": 0.02,
        "impacto_vendas": 0.25,
        "duracao_dias": 30,
        "prioridade": 2,
        "ativo": True,
        "descricao": "Campanha nacional aumenta as vendas."
    },
    {
        "id_evento": 3,
        "nome_evento": "Problema Logístico",
        "tipo": "Operacional",
        "categoria": "Todas",
        "regiao": "Sul",
        "probabilidade": 0.02,
        "impacto_vendas": -0.15,
        "duracao_dias": 20,
        "prioridade": 4,
        "ativo": True,
        "descricao": "Atrasos reduzem a quantidade de pedidos."
    },
    {
        "id_evento": 4,
        "nome_evento": "Produto Viral",
        "tipo": "Mercado",
        "categoria": "Tecnologia",
        "regiao": "Todas",
        "probabilidade": 0.01,
        "impacto_vendas": 0.40,
        "duracao_dias": 45,
        "prioridade": 5,
        "ativo": True,
        "descricao": "Produto ganha destaque e aumenta as vendas."
    },
    {
        "id_evento": 5,
        "nome_evento": "Ruptura de Estoque",
        "tipo": "Operacional",
        "categoria": "Eletro",
        "regiao": "Nordeste",
        "probabilidade": 0.02,
        "impacto_vendas": -0.30,
        "duracao_dias": 15,
        "prioridade": 5,
        "ativo": True,
        "descricao": "Falta de estoque reduz as vendas."
    },
    {
        "id_evento": 6,
        "nome_evento": "Crise Econômica Regional",
        "tipo": "Econômico",
        "categoria": "Todas",
        "regiao": "Centro-Oeste",
        "probabilidade": 0.01,
        "impacto_vendas": -0.25,
        "duracao_dias": 120,
        "prioridade": 5,
        "ativo": True,
        "descricao": "Redução temporária do consumo."
        }]
    return pd.DataFrame(eventos)

if __name__ == "__main__":
    eventos = gerar_eventos()
    print(eventos)