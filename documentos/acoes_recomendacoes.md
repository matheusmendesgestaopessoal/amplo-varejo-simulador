# Plano de Ação Prescritivo — Amplo Varejo S.A.

**Baseado na análise do dashboard executivo · Período analisado: 01/01/2025 a 31/12/2025 · Elaborado por: Matheus Mendes**

---

## Sumário Executivo

A análise de dados identificou **3 problemas operacionais** que, juntos, representam um impacto financeiro estimado de **R$ 2.100.000**. Os problemas estão concentrados em três frentes distintas — estoque, giro de produto e desempenho de loja — e cada um tem uma ação recomendada, uma área responsável e uma prioridade definida.

| Problema | Impacto Estimado | Prioridade | Responsável |
|---|---:|:---:|---|
| Taxa de cancelamento acima da meta | R$ 1.470.000 | 🔴 Alta | Operações / Logística |
| Baixo giro de estoque | R$ 357.000 | 🟠 Média | Estoque / Comercial |
| Lojas abaixo da meta | R$ 273.000 | 🟠 Média | Gestão de Lojas / Comercial |
| **Total** | **R$ 2.100.000** | | |

---

## 1. Objetivo e Como Usar Este Documento

Este documento traduz os achados do dashboard executivo em **ações concretas, com responsável e prazo definidos**. Ele não substitui o dashboard — complementa. O dashboard mostra o quê; este documento explica o porquê e o que fazer a respeito.

**Para a liderança:** use este documento para decidir prioridade de investimento de tempo e recursos entre as áreas.

**Para as áreas de execução:** cada problema traz uma seção "Evidências no Dashboard", indicando exatamente qual página e quais filtros usar para validar o diagnóstico antes de agir — não execute a ação recomendada sem antes confirmar o recorte específico (loja, produto, região) que se aplica à sua realidade.

## 2. Metodologia e Fontes de Dados

Os três problemas foram identificados a partir do cruzamento de indicadores nas páginas **Overview**, **Produtos** e **Clientes** do dashboard, com aprofundamento na página **Insights**. Os valores de impacto financeiro foram estimados por meio de *[Receita Perdida = CALCULATE([Receita_Total], 'FATO Vendas'[sk_status] = 3)]*.
---

## 3. Problemas Identificados

### Problema 1 — Taxa de cancelamento acima da meta

**Diagnóstico**
A taxa de cancelamento de pedidos está acima da meta de **3%** estabelecida pela empresa. Cada pedido cancelado representa uma venda que já havia sido iniciada, mas não convertida — diferente de uma venda que nunca aconteceu, aqui já existia demanda real sendo perdida.

**Evidências no Dashboard**
Página **Insights** → card de Taxa de Cancelamento (comparar com a meta de 3%) → filtro por loja/categoria para identificar onde a taxa é mais alta.

**Causa provável**
A hipótese principal é **indisponibilidade de produto no momento do pedido** — quando o cliente pede algo que a loja não tem em estoque suficiente, a chance de cancelamento aumenta, especialmente em picos de demanda.

**Impacto financeiro estimado**
**R$ R$ 2.100.000** — valor associado à receita que teria sido concretizada se os pedidos cancelados por indisponibilidade tivessem sido atendidos.

**Ação recomendada**
1. Cruzar pedidos cancelados com nível de estoque no momento do pedido (mesma loja, mesmo produto, mesma data)
2. Identificar as lojas e produtos com maior concentração de cancelamento
3. Redistribuir estoque das lojas com sobra para as lojas com maior taxa de cancelamento
4. Reforçar reposição dos produtos mais envolvidos, priorizando os de maior ticket médio

**Resultado esperado após a ação**
Redução da taxa de cancelamento de 9,8% para próximo de 3% (meta), a confirmar em novo ciclo de medição.

**Área responsável:** Operações / Logística / Estoque
**Prioridade:** 🔴 Alta
**Prazo sugerido para reavaliação:** 30 dias após início da ação

---

### Problema 2 — Baixo giro de estoque

**Diagnóstico**
Um grupo de produtos apresenta volume de vendas desproporcionalmente baixo em relação à quantidade mantida em estoque. Isso significa capital parado — dinheiro investido em produto que não está gerando retorno, além de ocupar espaço que poderia ser usado por itens de maior demanda.

**Evidências no Dashboard**
Página **Produtos** → visual "Produtos com Baixa Saída", filtrado por categoria.

**Causa provável**
Uma combinação possível de: demanda abaixo da expectativa original de compra, preço pouco competitivo frente ao mercado, concentração do produto em lojas de baixo fluxo, ou ausência de campanha comercial para esses itens específicos.

**Impacto financeiro estimado**
**R$ 357.000** — valor de capital imobilizado nos produtos identificados com giro mais baixo.

**Ação recomendada**
1. Classificar todos os produtos por giro (ex: Curva ABC de estoque, não só de receita)
2. Para os produtos críticos (giro mais baixo), analisar o histórico de vendas dos últimos 3-6 meses
3. Avaliar transferência para lojas com maior demanda comprovada daquela categoria
4. Criar campanha promocional pontual para os itens parados
5. Suspender novas compras desses produtos até normalizar o estoque existente

**Resultado esperado após a ação**
Redução do capital imobilizado em produtos de baixo giro, com liberação de espaço em estoque para itens de maior rotatividade.

**Área responsável:** Estoque / Compras / Comercial
**Prioridade:** 🟠 Média
**Prazo sugerido para reavaliação:** 60 dias após início da ação

---

### Problema 3 — Lojas abaixo da meta de desempenho

**Diagnóstico**
Um subconjunto de lojas apresenta desempenho comercial consistentemente abaixo do esperado, puxando o resultado consolidado da empresa para baixo. Importante: cada loja abaixo da meta pode ter uma causa diferente — este não é um problema único, é uma categoria de problemas que exige diagnóstico individual.

**Evidências no Dashboard**
Página **Overview** → visual Meta x Realizado, filtrado por loja, e página **Clientes** → cruzamento de fluxo de clientes por loja.

**Causa provável**
Entre as causas possíveis: baixo fluxo de clientes na região, baixa taxa de conversão da equipe de vendas, mix de produto inadequado ao perfil da loja, estoque insuficiente, ou desempenho abaixo do esperado de vendedores específicos.

**Impacto financeiro estimado**
**R$ 273.000** — valor associado à diferença entre meta e realizado nas unidades identificadas.

**Ação recomendada**
1. Comparar, loja a loja, os indicadores: receita, quantidade de pedidos, ticket médio, quantidade de clientes ativos, produtos vendidos e desempenho de vendedores
2. Classificar a causa dominante de cada loja abaixo da meta (não tratar todas com a mesma solução)
3. Aplicar ação direcionada por causa:

| Causa identificada | Ação |
|---|---|
| Baixo fluxo de clientes | Campanha local de atração |
| Baixa conversão | Treinamento da equipe comercial |
| Estoque inadequado | Redistribuição de produtos |
| Baixo desempenho de vendedor | Acompanhamento individual e plano de metas |

**Resultado esperado após a ação**
Redução do gap entre meta e realizado nas lojas identificadas, mensurado individualmente por unidade.

**Área responsável:** Gestão de Lojas / Comercial
**Prioridade:** 🟠 Média
**Prazo sugerido para reavaliação:** 60 dias após início da ação

---

## 4. Comparativo de Prioridade

Uma pergunta natural da liderança é "por onde começar" — a resposta não é só o valor financeiro, é a relação entre esforço e retorno:

| Problema | Impacto | Complexidade de Execução | Por que essa prioridade |
|---|---|---|---|
| Cancelamento | R$ 1.470.000 | Média (redistribuição logística) | Maior impacto financeiro e causa mais direta de resolver |
| Baixo giro | R$ 357.000 | Baixa (decisão comercial) | Ação rápida, mas impacto menor |
| Lojas abaixo da meta | R$ 273.000 | Alta (diagnóstico individual por loja) | Exige mais tempo de análise antes de agir, resultado mais lento |

## 5. Plano Consolidado de Ações

| Problema | Causa | Ação | Responsável | Prioridade | Impacto | Prazo de Reavaliação |
|---|---|---|---|---|---:|---|
| Cancelamento acima da meta | Indisponibilidade de estoque | Redistribuir estoque e reforçar abastecimento | Operações / Logística | 🔴 Alta | R$ 1.470.000 | 30 dias |
| Baixo giro de estoque | Produtos com baixa saída | Campanhas, redistribuição e revisão de compras | Estoque / Comercial | 🟠 Média | R$ 357.000 | 60 dias |
| Lojas abaixo da meta | Baixo desempenho comercial | Diagnóstico individual e plano de recuperação | Gestão / Comercial | 🟠 Média | R$ 273.000 | 60 dias |

**Impacto financeiro total estimado: R$ 2.100.000**

## 6. Processo de Acompanhamento

Este plano só gera valor se for acompanhado até o resultado final — não termina na entrega deste documento.

```
Etapa 1 — Identificação
   O dashboard identifica o problema e sua magnitude
        ↓
Etapa 2 — Diagnóstico
   A área responsável valida a causa com dados operacionais próprios
        ↓
Etapa 3 — Execução
   A ação recomendada é implementada
        ↓
Etapa 4 — Monitoramento
   Os indicadores voltam a ser acompanhados no Power BI
        ↓
Etapa 5 — Avaliação
   Resultado é comparado com a situação anterior, no prazo definido
```

Esse ciclo resume a lógica de todo o documento: **Dados → Problema → Causa → Ação → Resultado → Reavaliação.**

## 7. Premissas e Limitações

Os valores de impacto financeiro apresentados neste documento (R$ 1.470.000, R$ 357.000 e R$ 273.000) são **estimativas gerenciais**, calculadas a partir de projeções sobre os dados disponíveis — não são perdas financeiras comprovadas ou auditadas. Eles devem ser tratados como **ordem de grandeza para priorização**, não como número definitivo de resultado financeiro.

Essa distinção é intencional: tratar estimativa como fato comprometeria a credibilidade da análise. Recomenda-se que, após a execução das ações, os valores reais de resultado sejam apurados e comparados com esta estimativa inicial — o que também serve para calibrar a precisão do modelo de estimativa para os próximos ciclos.

## 8. Próxima Revisão

Este documento deve ser revisado a cada ciclo de reavaliação definido por problema (30-60 dias). Uma nova versão consolidada deve ser publicada trimestralmente, incorporando os resultados reais medidos e eventuais novos problemas identificados pelo dashboard.