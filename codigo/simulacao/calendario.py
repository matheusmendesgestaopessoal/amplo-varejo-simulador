# CALENDARIO

import pandas as pd
from codigo.configuracoes.configuracao import ANO_INICIO, ANO_FIM

def gerar_calendario():
    calendario = pd.date_range(start=ANO_INICIO, end=ANO_FIM, freq="D")

    df_calendario = pd.DataFrame({
        "id_calendario": range(1, len(calendario) + 1),
        "data": calendario.date,
        "ano": calendario.year,
        "mes": calendario.month,
        "nome_mes": calendario.month_name(),
        "trimestre": calendario.quarter,
        "semestre": ( calendario.month - 1 ) // 6 + 1,
        "dia": calendario.day,
        "dia_semana": calendario.day_name(),
        "dia_util": calendario.dayofweek < 5,
        "final_de_semana": calendario.dayofweek >= 5
        })
    return df_calendario

if __name__ == "__main__":
    calendario = gerar_calendario()
    print(calendario.head())