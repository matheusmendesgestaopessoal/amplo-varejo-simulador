# MOTOR

''' Arquivo responsável por orquestrar toda a geração
dos dados da Amplo Varejo S.A. '''

# DADOS MESTRES

from codigo.geradores.mestres.estados import gerar_estados
from codigo.geradores.mestres.lojas import gerar_lojas
from codigo.geradores.mestres.vendedores import gerar_vendedores
from codigo.geradores.mestres.categorias import gerar_categorias
from codigo.geradores.mestres.produtos import gerar_produtos
from codigo.geradores.mestres.clientes import gerar_clientes

# SIMULAÇÕES

from codigo.geradores.apoio.dados_simulacao import DadosSimulacao
from codigo.simulacao.calendario import gerar_calendario
from codigo.simulacao.sazonalidade import gerar_sazonalidade
from codigo.simulacao.campanhas import gerar_campanhas
from codigo.simulacao.eventos import gerar_eventos
from codigo.simulacao.metas import gerar_metas

# OPERACOES

from codigo.geradores.operacoes.pedidos import gerar_pedidos
from codigo.geradores.operacoes.itens_pedido import gerar_itens_pedido
from codigo.geradores.operacoes.estoque import gerar_estoque
from codigo.geradores.operacoes.movimentacao_estoque import gerar_movimentacao_estoque
# from codigo.geradores.operacoes.estoque 
# from codigo.geradores.operacoes.estoque 
# EXPORTADOR
from codigo.exportadores.exportar_csv import exportar_csv

def executar_simulacao():

    dados = DadosSimulacao()

    print("=" * 60)
    print("INICIANDO SIMULAÇÃO")
    print("=" * 60)

    # TABELAS DE APOIO
    dados.calendario = gerar_calendario()
    dados.sazonalidade = gerar_sazonalidade()
    dados.campanhas = gerar_campanhas()
    dados.eventos = gerar_eventos()


    # TABELAS MESTRES
    dados.estados = gerar_estados()
    dados.lojas = gerar_lojas(dados.estados)
    dados.clientes = gerar_clientes(dados)
    dados.vendedores = gerar_vendedores(dados.lojas)

    dados.categorias = gerar_categorias()
    dados.produtos = gerar_produtos(dados)



    dados.metas = gerar_metas(dados)

    # TABELAS OPERACIONAIS
    dados.pedidos = gerar_pedidos(dados)
    dados.itens_pedido = gerar_itens_pedido(dados)
    dados.estoque = gerar_estoque(dados)
    dados.movimentacao_estoque = gerar_movimentacao_estoque(dados)

    return dados

if __name__ == "__main__":

    dados = executar_simulacao()
    dados.resumo()

