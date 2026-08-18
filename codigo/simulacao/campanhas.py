# CAMPANHAS

''' Define todas as campanhas comerciais da empresa.
As campanhas serão utilizadas pelo motor de simulação
para aumentar o volume de vendas durante períodos específicos. '''

import pandas as pd


def gerar_campanhas():
    campanhas = [{
        "id_campanha": 1,
        "nome": "Volta às Aulas",
        "tipo": "Sazonal",
        "mes_inicio": 1,
        "dia_inicio": 15,
        "mes_fim": 2,
        "dia_fim": 15,
        "desconto_percentual": 15,
        "multiplicador_vendas": 1.10,
        "categoria": "Escritório",
        "prioridade": 2,
        "ativo": True,
        "descricao": "Campanha voltada para produtos escolares e escritório."
    },
    {
        "id_campanha": 2,
        "nome": "Dia das Mães",
        "tipo": "Data Comemorativa",
        "mes_inicio": 5,
        "dia_inicio": 1,
        "mes_fim": 5,
        "dia_fim": 14,
        "desconto_percentual": 10,
        "multiplicador_vendas": 1.10,
        "categoria": "Casa",
        "prioridade": 2,
        "ativo": True,
        "descricao": "Campanha especial para presentes do Dia das Mães."
    },
    {
        "id_campanha": 3,
        "nome": "Liquidação de Inverno",
        "tipo": "Liquidação",
        "mes_inicio": 7,
        "dia_inicio": 1,
        "mes_fim": 7,
        "dia_fim": 15,
        "desconto_percentual": 20,
        "multiplicador_vendas": 1.10,
        "categoria": "Todas",
        "prioridade": 1,
        "ativo": True,
        "descricao": "Liquidação nacional para renovação de estoque."
    },
    {
        "id_campanha": 4,
        "nome": "Dia das Crianças",
        "tipo": "Data Comemorativa",
        "mes_inicio": 10,
        "dia_inicio": 1,
        "mes_fim": 10,
        "dia_fim": 12,
        "desconto_percentual": 15,
        "multiplicador_vendas": 1.10,
        "categoria": "Tecnologia",
        "prioridade": 2,
        "ativo": True,
        "descricao": "Campanha para produtos infantis e eletrônicos."
    },
    {
        "id_campanha": 5,
        "nome": "Black Friday",
        "tipo": "Promoção",
        "mes_inicio": 11,
        "dia_inicio": 20,
        "mes_fim": 11,
        "dia_fim": 30,
        "desconto_percentual": 30,
        "multiplicador_vendas": 1.20,
        "categoria": "Todas",
        "prioridade": 5,
        "ativo": True,
        "descricao": "Maior campanha promocional do ano."
    },

    {
        "id_campanha": 6,
        "nome": "Natal",
        "tipo": "Data Comemorativa",
        "mes_inicio": 12,
        "dia_inicio": 1,
        "mes_fim": 12,
        "dia_fim": 24,
        "desconto_percentual": 20,
        "multiplicador_vendas": 1.20,
        "categoria": "Todas",
        "prioridade": 4,
        "ativo": True,
        "descricao": "Campanha de Natal."
    }]
    return pd.DataFrame(campanhas)

if __name__ == "__main__":
    campanhas = gerar_campanhas()
    print(campanhas)