# Dashboard

- `amplo_varejo.pbip`: projeto do Power BI (abre no Power BI Desktop). O relatório fica em `amplo_varejo.Report/` e o modelo semântico em `amplo_varejo.SemanticModel/`.
- `tema_matheus.json`: tema da identidade visual (já aplicado no relatório; para outro arquivo: Exibir → Temas → Procurar temas).
- `prints/`: imagens das páginas, numeradas pela ordem (`01_diagnostico.png`, `02_detalhe_loja.png`).
- `gerador_pbir/`: script que gera as páginas do relatório a partir de modelos de visual (`python gerar_paginas.py <pasta .Report> <pasta modelos>`).
- `prototipo/`: protótipos de layout em HTML aprovados antes da construção. Os números deles são ilustrativos.

## Páginas

| Página | Tipo | O que responde |
|---|---|---|
| Diagnóstico | Rolagem (storytelling) | Onde a empresa perde faturamento, quanto vale e o plano de ação |
| Detalhe da loja | Drill-through (botão direito numa loja → Detalhar) | Por que uma loja ficou abaixo da meta e o que fazer |
| Dica da região | Tooltip | Resumo da região ao passar o mouse |

**Link público:** LINK_PUBLICO_POWER_BI
