import random

from codigo.configuracoes.configuracao import PEDIDOS_MINIMOS_DIA, PEDIDOS_MAXIMOS_DIA
from codigo.utilitarios.regioes import pesos
from codigo.utilitarios.catalogo_produtos import PESO_CATEGORIA


def _ativos_no_dia(tabela, mes, dia):
    """Função genérica: filtra campanhas OU eventos ativos numa data,
    usando mes_inicio/dia_inicio/mes_fim/dia_fim (mesma lógica pros dois)."""
    inicio_ok = (tabela["mes_inicio"] < mes) | (
        (tabela["mes_inicio"] == mes) & (tabela["dia_inicio"] <= dia)
    )
    fim_ok = (tabela["mes_fim"] > mes) | (
        (tabela["mes_fim"] == mes) & (tabela["dia_fim"] >= dia)
    )
    return tabela[inicio_ok & fim_ok]


def calcular_demanda_dia(dados, data, regiao):
    """Calcula quantos pedidos uma REGIÃO específica gera em um dia,
    já considerando sazonalidade, campanhas gerais e eventos daquela região."""

    demanda_total_dia = random.randint(PEDIDOS_MINIMOS_DIA, PEDIDOS_MAXIMOS_DIA)
    demanda = demanda_total_dia * (pesos[regiao] / 100)

    mes = data.month
    sazonalidade = dados.sazonalidade[dados.sazonalidade["mes"] == mes].iloc[0]
    demanda *= sazonalidade["indice_vendas"]

    campanhas_ativas = _ativos_no_dia(dados.campanhas, mes, data.day)
    for _, campanha in campanhas_ativas[campanhas_ativas["categoria"] == "Todas"].iterrows():
        demanda *= campanha["multiplicador_vendas"]

    eventos_ativos = _ativos_no_dia(dados.eventos, mes, data.day)
    eventos_regiao = eventos_ativos[
        (eventos_ativos["regiao"] == regiao) | (eventos_ativos["regiao"] == "Todas")
    ]
    for _, evento in eventos_regiao.iterrows():
        demanda *= (1 + evento["impacto_vendas"])

    return max(1, int(round(demanda)))


def calcular_peso_categorias_dia(dados, data):
    """Retorna os pesos de categoria ajustados para o dia, considerando
    campanhas/eventos de categoria específica. Usado em itens_pedido.py
    para enviesar o MIX de produto vendido (não o volume de pedido)."""

    pesos_ajustados = PESO_CATEGORIA.copy()
    mes, dia = data.month, data.day

    campanhas_ativas = _ativos_no_dia(dados.campanhas, mes, dia)
    for _, campanha in campanhas_ativas[campanhas_ativas["categoria"] != "Todas"].iterrows():
        cat = campanha["categoria"]
        if cat in pesos_ajustados:
            pesos_ajustados[cat] *= campanha["multiplicador_vendas"]

    eventos_ativos = _ativos_no_dia(dados.eventos, mes, dia)
    for _, evento in eventos_ativos[eventos_ativos["categoria"] != "Todas"].iterrows():
        cat = evento["categoria"]
        if cat in pesos_ajustados:
            pesos_ajustados[cat] *= (1 + evento["impacto_vendas"])

    return pesos_ajustados


if __name__ == "__main__":
    print("Módulo de demanda carregado com sucesso.")