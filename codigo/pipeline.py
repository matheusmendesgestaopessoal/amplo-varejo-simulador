from codigo.geradores.apoio.motor_simulacao import executar_simulacao
from codigo.exportadores.exportar_csv import exportar_csv
from codigo.exportadores.exportar_mysql import exportar_mysql
from codigo.dw.atualizar_dw import executar_carga_dw

from codigo.validacoes.validar_cobertura import validar_cobertura
from codigo.validacoes.validar_estoque import validar_estoque
from codigo.validacoes.validar_integridade import validar_integridade

def executar_pipeline():

    print("=" * 60)
    print("        AMPLО VAREJO - PIPELINE")
    print("=" * 60)

    # 1. GERAÇÃO
    print("\n[1/5] Gerando dados...\n")

    dados = executar_simulacao()

    # 2. VALIDAÇÕES
    print("\n[2/5] Validando dados...\n")

    cobertura_ok = validar_cobertura(dados)
    integridade_ok = validar_integridade(dados)
    estoque_ok = validar_estoque(dados)

    if not all([
        cobertura_ok,
        integridade_ok,
        estoque_ok
    ]):
        print("\nERRO: validações falharam.")
        print("Pipeline interrompida.")
        return

    print("\nTodas as validações passaram.")

    # 3. CSV
    print("\n[3/5] Exportando CSVs...\n")

    exportar_csv(dados)

    # 4. OLTP
    print("\n[4/5] Carregando banco OLTP...\n")

    exportar_mysql()

    # 5. DW
    print("\n[5/5] Atualizando Data Warehouse...\n")

    executar_carga_dw()

    print("\n" + "=" * 60)
    print("      PIPELINE CONCLUÍDA COM SUCESSO!")
    print("=" * 60)


if __name__ == "__main__":
    executar_pipeline()