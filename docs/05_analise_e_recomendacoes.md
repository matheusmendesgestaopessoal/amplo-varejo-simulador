# Análise e Recomendações · Amplo Varejo S.A.

**Período analisado:** 01/01/2025 a 31/12/2025 · **Fonte:** Data Warehouse `amplo_varejo_dw` e dashboard (página Diagnóstico) · **Autor:** Matheus Mendes

Todos os números deste documento podem ser recalculados com `python -m codigo.analises.diagnostico`.
Cada recomendação segue o cartão de decisão: Fato → Interpretação → Causas → Validação → Ação → Resultado → Acompanhamento.

---

## Recomendação

> **Recomendo começar pelos cancelamentos: é a maior perda (R$ 2,10 Mi), a primeira ação custa pouco (registrar o motivo de cada cancelamento) e o retorno começa em 30 dias.**

As três frentes juntas podem recuperar de **R$ 1,7 a 3,3 Mi** em receita e caixa em até 90 dias.

| Ordem | Frente | Decisão | Dono | Prazo | Indicador (hoje → meta) | Valor recuperável | Esforço | Confiança |
|:---:|---|---|---|---|---|---:|---|---|
| 1 | Cancelamentos | Registrar o motivo, auditar o fluxo do pedido e corrigir a causa nº 1 | Operações + TI | 30 a 90 dias | Taxa 8,9% → 5,0% | R$ 0,69 a 1,39 Mi | Médio | Média |
| 2 | Estoque excedente | Redistribuir entre lojas, pausar compras e promover os 10 itens com mais excesso | Estoque + Compras | 60 dias | Excesso R$ 1,56 Mi → R$ 0,6 Mi | R$ 0,63 a 1,09 Mi em caixa | Baixo | Alta |
| 3 | Lojas abaixo da meta | Diagnóstico individual das 19 lojas abaixo de 90% da meta | Gestão de lojas | 60 a 90 dias | Atingimento 95,5% → 100% | R$ 0,40 a 0,80 Mi | Alto | Média |

### Decisões pedidas à diretoria
1. Aprovar o campo obrigatório de motivo de cancelamento (custo baixo).
2. Autorizar a amostragem de 200 cancelamentos com a operação.
3. Pausar as compras dos 10 produtos com mais excesso de estoque.
4. Autorizar o diagnóstico individual das 19 lojas abaixo de 90% da meta.

### Por que essa ordem
Cancelamento é a maior perda e a primeira ação é barata e rápida. Estoque tem a maior confiança e o menor esforço,
mas libera caixa, não receita. Lojas exigem diagnóstico individual, o que leva mais tempo.

---

## Visão geral de 2025

| Indicador | Valor |
|---|---:|
| Pedidos | 10.708 (9.751 válidos, 957 cancelados) |
| Receita válida | R$ 21,66 Mi |
| Lucro · margem | R$ 7,43 Mi · 34,3% |
| Ticket médio | R$ 2.221 |
| Meta de faturamento · atingimento | R$ 22,67 Mi · 95,5% |

Definições: receita válida = pedidos não cancelados; taxa de cancelamento = cancelados ÷ total de pedidos.

---

## Cartão 1 · Cancelamentos acima da meta
**Prioridade:** Alta · **Esforço:** Médio · **Confiança na causa:** Média · **Dono:** Operações + TI

**1. Fato**
957 dos 10.708 pedidos de 2025 foram cancelados: **8,9%**, contra a meta de 3,0% (3,0×). A receita desses pedidos soma **R$ 2,10 Mi**.
A taxa vai de 7,1% a 9,3% entre as regiões, de 7,2% a 10,9% entre os meses e de 3,0% a 13,0% entre as lojas.
*Fonte:* medidas `Taxa Cancelamento` e `Receita Perdida`; seção "Cancelamentos" da página Diagnóstico.

**2. Interpretação**
É a maior perda do ano. Diferente de uma venda que não aconteceu, aqui o cliente já tinha decidido comprar.
Os testes qui-quadrado **não mostram diferença significativa** entre regiões (p = 0,12), meses (p = 0,38), lojas (p = 0,64)
e categorias (p = 0,94): as variações são compatíveis com o acaso. O cancelamento é igual em todo lugar, o que aponta para o
**processo do pedido**, e não para uma loja, região ou produto.
*O que ainda não sabemos:* o motivo de cada cancelamento, que não é registrado no sistema.

**3. Causas prováveis**
| Hipótese | Evidência | Confiança |
|---|---|---|
| Falha no pagamento ou na aprovação do pedido | Taxa uniforme em todo lugar, típica de uma etapa comum a todos os pedidos | Média |
| Prazo de entrega longo | Sem diferença entre regiões (o Norte não difere das demais) | Baixa |
| Desistência do cliente | Sem dado de motivo para confirmar | Baixa |
| ~~Falta de estoque~~ | Descartada: havia saldo de estoque em todas as lojas e produtos | — |

**4. Validação**
Classificar a causa de uma amostra de 200 cancelamentos junto com a operação (2 semanas).
Critério: a causa que somar 40% ou mais da amostra vira a prioridade.

**5. Ação**
| Passo | Responsável | Prazo |
|---|---|---|
| Tornar obrigatório o motivo do cancelamento no sistema | TI | 30 dias |
| Classificar a amostra de 200 cancelamentos | Operações + Dados | 2 semanas |
| Corrigir a causa nº 1 e medir a taxa toda semana | Operações + TI | 90 dias |

**6. Resultado esperado**
| Cenário | Taxa alvo | Receita recuperável |
|---|---:|---:|
| Conservador | 6% | R$ 0,69 Mi |
| Provável | 5% | R$ 0,92 Mi |
| Meta | 3% | R$ 1,39 Mi |

Cálculo: receita dos cancelados × (taxa atual − taxa alvo) ÷ taxa atual.

**7. Acompanhamento**
- **KPI:** taxa de cancelamento semanal.
- **Revisão:** 30 e 90 dias.
- **Gatilho:** se em 60 dias a taxa não ficar abaixo de 8%, rever a causa priorizada.

---

## Cartão 2 · Lojas abaixo da meta
**Prioridade:** Média · **Esforço:** Alto · **Confiança na causa:** Média · **Dono:** Gestão de lojas

**1. Fato**
A rede atingiu **95,5%** da meta (R$ 21,66 Mi de R$ 22,67 Mi). **35 de 54 lojas** ficaram abaixo, com gap de **R$ 1,64 Mi**.
As **19 lojas abaixo de 90%** concentram R$ 1,34 Mi (82% do gap). Menor atingimento: PA 051, com 72%.
*Fonte:* medidas `Meta x Realizado %`, `Lojas Abaixo Meta`, `Gap Lojas Abaixo Meta`, `Lojas Abaixo 90%`.

**2. Interpretação**
O gap está concentrado: tratar 19 lojas resolve a maior parte do problema. Cada loja pode ter uma causa diferente
(poucos pedidos, ticket baixo ou cancelamento alto), por isso o diagnóstico é individual.
*O que ainda não sabemos:* o fluxo de clientes nas lojas (visitas), que separaria atração de conversão.

**3. Causas prováveis**
Variam por loja. A página **Detalhe da loja** (drill-through) compara pedidos, ticket médio e cancelamento
de cada loja com a média da rede e indica a causa dominante.

**4. Validação**
Abrir o detalhe de cada uma das 19 lojas e confirmar a causa com o gerente regional.

**5. Ação**
| Causa dominante | Ação | Responsável | Prazo |
|---|---|---|---|
| Poucos pedidos (abaixo da média da rede) | Campanha local de atração | Marketing + loja | 60 dias |
| Ticket baixo | Treino de venda de maior valor e revisão do mix | Comercial | 60 dias |
| Pedidos e ticket na média | Revisar a meta com a gestão regional | Gestão de lojas | 30 dias |

**6. Resultado esperado**
Fechar de 30% a 60% do gap das 19 lojas em 60 a 90 dias: **R$ 0,40 a 0,80 Mi**.

**7. Acompanhamento**
- **KPI:** atingimento mensal por loja.
- **Gatilho:** loja que não subir 5 p.p. de atingimento em 60 dias tem a causa revista.

---

## Cartão 3 · Estoque acima de 3 meses de cobertura
**Prioridade:** Média · **Esforço:** Baixo · **Confiança:** Alta · **Dono:** Estoque + Compras

**1. Fato**
O estoque final vale **R$ 4,56 Mi** a custo, cerca de **4 meses de venda**. **R$ 1,56 Mi (34%)** está acima de 3 meses de cobertura.
**10 dos 80 produtos** concentram metade do excesso: MacBook Air, Desktop Gamer, Smart TV 65", Notebook Lenovo IdeaPad,
Lava e Seca, Geladeira Frost Free, Notebook Dell Inspiron, Notebook Acer Aspire, Secadora de Roupas e Smart TV 50".
**273 combinações de loja e produto** não venderam nada no ano (R$ 282 mil).
*Fonte:* medidas `Valor Estoque Final`, `Cobertura Estoque (meses)`, `Excesso Estoque`, `Combinações Sem Venda`.

**2. Interpretação**
É capital parado em itens caros, que ocupa espaço e perde valor com o tempo. Como o excesso está concentrado em poucos
produtos, a ação é dirigida e pode começar já.

**3. Causas prováveis**
| Hipótese | Evidência | Confiança |
|---|---|---|
| Compra acima da demanda em itens de alto valor | Excesso concentrado em produtos de ticket alto | Alta |
| Reposição não ajustada à venda de cada loja | O mesmo produto tem cobertura muito diferente entre lojas | Média |

**4. Validação**
Conferir com Compras os lotes e prazos de pedido dos 10 produtos.

**5. Ação**
| Passo | Responsável | Prazo |
|---|---|---|
| Transferir excedentes entre lojas da mesma região | Estoque | 30 dias |
| Pausar compras dos 10 itens até a cobertura voltar a 3 meses | Compras | Imediato |
| Promoção dirigida para os itens sem venda | Comercial | 60 dias |

**6. Resultado esperado**
Liberar de 40% a 70% do excesso em 60 dias: **R$ 0,63 a 1,09 Mi em caixa**.

**7. Acompanhamento**
- **KPI:** cobertura de estoque por produto e loja.
- **Gatilho:** item acima de 4 meses de cobertura entra na lista de promoção.

---

## Premissas e limitações
- Os dados são **sintéticos**, gerados pelo simulador com regras de negócio definidas. Os resultados ilustram o método.
- Os valores de impacto são **estimativas gerenciais para priorização**, não perdas auditadas. Devem ser apurados após a execução.
- O status dos pedidos é sorteado no simulador com probabilidade fixa, o que explica a uniformidade dos cancelamentos.
  Numa empresa real, o mesmo teste (a taxa varia entre grupos?) é o primeiro passo para separar problema de processo
  de problema local.
- Metas e estoque inicial foram recalibrados para a escala das vendas simuladas. Ver o [registro de correções](06_registro_de_correcoes.md).
