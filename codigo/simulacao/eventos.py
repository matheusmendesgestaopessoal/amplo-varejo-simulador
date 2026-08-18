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
            "mes_inicio": 7, "dia_inicio": 1,
            "mes_fim": 9, "dia_fim": 30,
            "impacto_vendas": 0,
            "prioridade": 3,
            "ativo": True,
            "descricao": "Novo concorrente reduz as vendas do Sudeste (Jul-Set)."
        },
        {
            "id_evento": 2,
            "nome_evento": "Campanha Nacional",
            "tipo": "Marketing",
            "categoria": "Todas",
            "regiao": "Todas",
            "mes_inicio": 6, "dia_inicio": 1,
            "mes_fim": 6, "dia_fim": 15,
            "impacto_vendas": 0.25,
            "prioridade": 2,
            "ativo": True,
            "descricao": "Campanha nacional aumenta vendas em Junho (fora do período de queda)."
        },
        {
            "id_evento": 3,
            "nome_evento": "Problema Logístico",
            "tipo": "Operacional",
            "categoria": "Todas",
            "regiao": "Sul",
            "mes_inicio": 10, "dia_inicio": 1,
            "mes_fim": 10, "dia_fim": 20,
            "impacto_vendas": -0.15,
            "prioridade": 4,
            "ativo": True,
            "descricao": "Atrasos reduzem pedidos no Sul em Outubro."
        },
        {
            "id_evento": 4,
            "nome_evento": "Produto Viral",
            "tipo": "Mercado",
            "categoria": "Tecnologia",
            "regiao": "Todas",
            "mes_inicio": 4, "dia_inicio": 1,
            "mes_fim": 4, "dia_fim": 15,
            "impacto_vendas": 0.15,
            "prioridade": 5,
            "ativo": True,
            "descricao": "Produto viraliza em Tecnologia, em Abril (fora do período de queda)."
        },
        {
            "id_evento": 5,
            "nome_evento": "Ruptura de Estoque",
            "tipo": "Operacional",
            "categoria": "Eletro",
            "regiao": "Nordeste",
            "mes_inicio": 9, "dia_inicio": 1,
            "mes_fim": 9, "dia_fim": 15,
            "impacto_vendas": 0,
            "prioridade": 5,
            "ativo": True,
            "descricao": "Falta de estoque reduz vendas de Eletro no Nordeste em Setembro."
        },
        {
            "id_evento": 6,
            "nome_evento": "Crise Econômica Regional",
            "tipo": "Econômico",
            "categoria": "Todas",
            "regiao": "Centro-Oeste",
            "mes_inicio": 8, "dia_inicio": 1,
            "mes_fim": 11, "dia_fim": 30,
            "impacto_vendas": -0.10,
            "prioridade": 5,
            "ativo": True,
            "descricao": "Redução de consumo no Centro-Oeste (Ago-Nov)."
        },
    ]
    return pd.DataFrame(eventos)

if __name__ == "__main__":
    eventos = gerar_eventos()
    print(eventos)