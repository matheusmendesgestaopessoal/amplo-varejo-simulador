# Roteiro do dashboard · Amplo Varejo

Página única de rolagem (1920 px de largura, tamanho real), contada como uma história:
**Pergunta → Contexto → Achados → Ação**, com a identidade visual do portfólio.

**Versão vigente: v2 · ferramenta de trabalho** (pasta [`v2/`](v2/))
- [`v2/pagina_1_historia.png`](v2/pagina_1_historia.png): página de história, com resposta na primeira tela, filtros globais, títulos dinâmicos e tooltip
- [`v2/pagina_2_detalhe_loja.png`](v2/pagina_2_detalhe_loja.png): detalhe por loja (drill-through)
- [`comparacao_v1_v2.png`](comparacao_v1_v2.png): v1 (vitrine) x v2 (ferramenta)

A v1 ([`prototipo_dashboard.png`](prototipo_dashboard.png)) fica como referência. Regras gerais no kit:
`kit-projetos-dados/_kit/padrao_dashboard.md`.

Abaixo, o roteiro de conteúdo (vale para a v2; na v2 o cabeçalho não tem menu e a seção 1 junta pergunta, resposta e KPIs).

| # | Seção | Pergunta que responde | Título-conclusão | Visuais |
|---|---|---|---|---|
| 0 | Cabeçalho | O que é este relatório? | Amplo Varejo · Diagnóstico de faturamento | Nome, período, autor, filtros (período, região, loja) |
| 1 | Pergunta (hero) | Onde a empresa perde faturamento? | "Três causas operacionais somam R$ 2,1 Mi; cancelamentos respondem por 70%." | 5 KPIs: receita (destaque azul), lucro, pedidos, taxa de cancelamento (vermelho vs meta), receita perdida |
| 2 | Contexto | Quando, onde e com o quê a Amplo fatura? | "Novembro e dezembro concentram 24% da receita." | Receita mensal x meta · receita por região (barras, no lugar do mapa) · receita por categoria · top 5 lojas · post-it "o que isso significa" |
| 3 | Achado 1 · Cancelamento 🔴 | Qual a maior perda? | "Cancelamentos 3,3× acima da meta custam R$ 1,47 Mi." | Taxa por mês com linha de meta · taxa por região · post-its hipótese / como validar / ação |
| 4 | Achado 2 · Estoque 🟠 | Onde há dinheiro parado? | "R$ 357 mil parados em produtos que quase não vendem." | Dispersão estoque x vendas (quadrante crítico em vermelho) · tabela dos produtos de menor giro |
| 5 | Achado 3 · Lojas 🟠 | Quais lojas puxam o resultado para baixo? | "Lojas abaixo da meta deixam R$ 273 mil na mesa." | Atingimento da meta por loja (vermelho < 100%) · tabela causa → ação |
| 6 | Ação | Por onde começar? | "Cancelamentos primeiro." | Barra de composição do impacto · plano de ação (problema, ação, responsável, impacto, prioridade, prazo) |
| 7 | Rodapé · método | Posso confiar nisso? | — | Dados, modelo, métricas, autor |

## Regras aplicadas
- Títulos dizem a conclusão, não o nome do gráfico.
- Azul só no que importa; azul-seleção no resto; vermelho só para problema; verde para meta atingida.
- Barras começam no zero; sem mapa colorido (barras ordenadas comparam melhor).
- Cada achado termina em hipótese → validação → ação.

## Pendências antes de construir no Power BI
1. **A queda de 12% não aparece nos dados.** O problema declarado é uma queda anual de ~12%, mas só há 2025 e as 3 causas somam R$ 2,1 Mi (~0,7% da receita). Decidir: simular 2024 para mostrar a queda, ou reformular o problema como "receita perdida".
2. **Validar números:** taxa de cancelamento de 9,8% x receita perdida de R$ 1,47 Mi; corrigir "R$ R$ 2.100.000" no documento de ações (impacto do problema 1 é R$ 1,47 Mi).
3. Gráficos marcados como "valores ilustrativos" no protótipo precisam dos dados reais do modelo.
4. No Power BI não há rolagem até uma seção pelo menu; o menu do cabeçalho vira um índice visual ou sai.
