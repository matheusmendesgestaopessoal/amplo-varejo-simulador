# DADOS DA SIMULAÇÃO

''' Classe responsável por armazenar todos os DataFrames
gerados durante a simulação.'''

class DadosSimulacao:

    def __init__(self):

        # TABELAS DE APOIO
        self.calendario = None
        self.sazonalidade = None
        self.campanhas = None
        self.eventos = None
        self.metas = None

        # DADOS MESTRES
        self.estados = None
        self.lojas = None
        self.vendedores = None
        self.categorias = None
        self.produtos = None
        self.clientes = None

        # DADOS TRANSICIONAIS
        self.pedidos = None
        self.itens_pedido = None
        self.estoque = None
        self.movimentacao_estoque = None


    def resumo(self):
        print("\n" + "-" * 60)
        print("RESUMO DA GERAÇÃO:")
        print("-" * 60)     

        tabelas = {
            "Calendário": self.calendario,
            "Sazonalidade": self.sazonalidade,
            "Campanhas": self.campanhas,
            "Eventos": self.eventos,
            "Metas": self.metas,

            "Estados": self.estados,
            "Lojas": self.lojas,
            "Vendedores": self.vendedores,
            "Categorias": self.categorias,
            "Produtos": self.produtos,
            "Clientes": self.clientes,

            "Pedidos": self.pedidos,
            "Itens Pedido": self.itens_pedido,
            "Estoque": self.estoque,
            "Movimentação do Estoque": self.movimentacao_estoque
            }

        for nome, tabela in tabelas.items():

            quantidade = 0 if tabela is None else len(tabela)
            print(f"{nome:<20}{quantidade:>10} registros")

        print("-" * 60)