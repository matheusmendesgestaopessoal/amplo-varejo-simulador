import random

from codigo.configuracoes.configuracao import PEDIDOS_MINIMOS_DIA, PEDIDOS_MAXIMOS_DIA

def calcular_demanda_dia(dados, data):

    # Demanda base 
    demanda = random.randint(PEDIDOS_MINIMOS_DIA, PEDIDOS_MAXIMOS_DIA)
    # Sazonalidade 
    mes = data.month
    sazonalidade = dados.sazonalidade.iloc[dados.sazonalidade["mes"]==mes].iloc[0]
    demanda *= sazonalidade["indice_vendas"]

    campanhas = dados.campanhas
    campanhas_ativas = campanhas[((campanhas["mes_inicio"] < mes) | 
                                  ((campanhas["mes_inicio"] == mes) & 
                                   (campanhas["dia_inicio"] <= data.day))) & 
                                   ((campanhas["mes_fim"] > mes) | 
                                    ((campanhas["mes_fim"] == mes) & 
                                     (campanhas["dia_fim"] >= data.day)))]

    for i, campanha in campanhas_ativas.iterrows():
        demanda *= campanha["multiplicador_vendas"]

    for i, evento in dados.eventos.iterrows():
        if random.random() <= evento["probabilidade"]:
            demanda *= (1 + evento["impacto_vendas"])

    return max(1, int(demanda))

    

