from pathlib import Path
from sqlalchemy import text
from codigo.configuracoes.database import conectar_dw

def executar_carga_dw():

    engine = conectar_dw()
    caminho_sql = Path("sql/03_JOINS.sql")

    if not caminho_sql.exists():
        print("Arquivo 03_JOINS.sq não encontrado.")
        return

    with open(caminho_sql, "r", encoding="utf-8") as arquivo:
        script = arquivo.read()

    comandos = script.split(";")

    print("\n========================================")
    print("       CARGA DO DATA WAREHOUSE")
    print("========================================\n")

    with engine.begin() as conexao:
        for comando in comandos:
            comando = comando.strip()
            if not comando:
                continue

            conexao.execute(text(comando))

            print("Comando executado.")

    print("\nDW atualizada com sucesso!")

if __name__ == "__main__":
    executar_carga_dw()


    