from codigo.geradores.apoio.motor_simulacao import executar_simulacao

from codigo.validacoes.validar_cobertura import validar_cobertura
from codigo.validacoes.validar_integridade import validar_integridade
from codigo.validacoes.validar_estoque import validar_estoque


dados = executar_simulacao()

validar_cobertura(dados)

validar_integridade(dados)

validar_estoque(dados)