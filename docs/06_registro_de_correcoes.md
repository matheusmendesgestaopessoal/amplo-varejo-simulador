# Registro de Correções · 12/10/2026

Revisão completa do projeto antes da nova versão do dashboard. Nenhum pedido novo foi gerado:
as vendas, clientes, lojas e produtos publicados continuam os mesmos. Este documento lista o que estava errado,
o que mudou e como reproduzir.

---

## 1. Escala das metas e do estoque

| Problema | Efeito | Correção |
|---|---|---|
| A meta era sorteada entre R$ 500 mil e R$ 900 mil por loja e mês, faixa pensada para o modo `producao`. No modo `desenvolvimento` (o dos dados publicados), cada loja vende cerca de R$ 33 mil por mês | Meta cerca de 20× acima da venda: atingimento de ~5% e "todas as lojas abaixo da meta" | Meta = venda média por loja da região no mês × fator de desafio de 0,95 a 1,15 |
| O estoque inicial era sorteado entre 20 e 500 unidades por loja e produto, enquanto cada loja vende ~6 unidades de cada produto no ano | Todo produto parecia parado; análise de giro sem sentido | Estoque inicial = unidades vendidas no ano + sobra de 0,5 a 6 meses de venda |

A correção é **determinística** e preserva a variação aleatória original de cada linha (o fator e a cobertura
são derivados do sorteio antigo). Arquivos alterados: `metas.csv`, `estoque.csv` e as linhas de entrada de
`movimentacao_estoque.csv`. Resultado: meta anual de R$ 22,67 Mi para R$ 21,66 Mi de receita válida (95,5%)
e estoque final de cerca de 4 meses de venda.

Script: [`codigo/correcoes/corrigir_escala_metas_estoque.py`](../codigo/correcoes/corrigir_escala_metas_estoque.py).

## 2. Simulador sem semente completa

A semente era aplicada ao Faker, mas não ao `random` nem ao `numpy` (usado por `DataFrame.sample()`).
Cada execução gerava dados diferentes, e os números do dashboard antigo vinham de uma execução diferente
da que está nos CSVs do repositório.

**Correção:** `random.seed` e `np.random.seed` no início de `executar_simulacao()`, e metas e estoque passaram a
ser gerados depois dos pedidos, na escala das vendas (`codigo/simulacao/metas.py`, `codigo/geradores/operacoes/estoque.py`).
Duas execuções seguidas agora produzem exatamente os mesmos dados.

> Atenção: rodar o pipeline completo de novo gera um conjunto **diferente** do publicado (reprodutível, mas outro).
> Os dados publicados foram mantidos e apenas corrigidos, para não trocar a base da análise.

## 3. Medidas DAX

| Medida | Erro | Correção |
|---|---|---|
| `Receita_Total`, `Custo_Total`, `Produtos_Vendidos` | Somavam pedidos cancelados | Filtram `sk_status <> 3` |
| `Taxa Cancelamento` | Dividia cancelados por pedidos **válidos** (9,8%) | Divide por **todos** os pedidos (8,9%) |
| `Receita Perdida` | Reaproveitava `Receita_Total`, que agora exclui cancelados | Soma `sub_total` dos cancelados diretamente |
| `Meta_Faturamento`, `Meta_Pedidos` | `fato_metas` não se relaciona com o calendário: por mês, aparecia a meta do ano | Aplicam o mês com `TREATAS` |
| `Valor_Estoque` | `MAX(custo)` sem transição de contexto pegava o maior custo de todos os produtos | `CALCULATE(MAX(custo))` por produto |

Também foram criadas 51 medidas novas (diagnóstico, textos dinâmicos e formatação). Ver o [dicionário de dados](04_dicionario_de_dados.md).

## 4. Premissa do problema

O documento de abertura partia de uma "queda de 12% no faturamento", mas os dados cobrem um único ano e não
permitem medir queda. A pergunta passou a ser: **onde a empresa perde faturamento em 2025, quanto isso vale e por
onde começar?** As causas foram testadas, e a hipótese anterior (cancelamento por falta de estoque) foi descartada.

## 5. Números antigos x atuais

| Indicador | Antes | Agora |
|---|---:|---:|
| Taxa de cancelamento | 9,8% | 8,9% |
| Impacto: cancelamentos | R$ 1,47 Mi | R$ 0,69 a 1,39 Mi recuperáveis (de R$ 2,10 Mi perdidos) |
| Impacto: estoque | R$ 357 mil | R$ 0,63 a 1,09 Mi em caixa (de R$ 1,56 Mi em excesso) |
| Impacto: lojas | R$ 273 mil | R$ 0,40 a 0,80 Mi (de R$ 1,64 Mi de gap) |

## Como reproduzir

Na raiz do projeto, com o MySQL configurado no `.env` (ver `.env.example`):

```bash
# só se partir dos CSVs originais (já aplicado no repositório; o script não roda duas vezes)
python -m codigo.correcoes.corrigir_escala_metas_estoque

# recarregar banco operacional e DW
python -c "from codigo.exportadores.exportar_mysql import exportar_mysql; exportar_mysql()"
python -c "from codigo.dw.atualizar_dw import executar_carga_dw; executar_carga_dw()"

# conferir todos os números da análise
python -m codigo.analises.diagnostico
```
