# Dashboard

- `amplo_varejo.pbip`: projeto do Power BI (abre no Power BI Desktop). O relatório fica em `amplo_varejo.Report/` e o modelo semântico em `amplo_varejo.SemanticModel/`.
- `tema_matheus.json`: tema da identidade visual (já aplicado no relatório; para outro arquivo: Exibir → Temas → Procurar temas).
- `prints/`: imagens das páginas, numeradas pela ordem (`01_diagnostico.png`, `02_detalhe_loja.png`).
- `prototipo/`: protótipos de layout em HTML aprovados antes da construção. Os números deles são ilustrativos.
- `gerador_pbir/`: gera as páginas do relatório a partir do layout aprovado (ver abaixo).

## Páginas

| Página | Tipo | O que responde |
|---|---|---|
| Diagnóstico | Rolagem (storytelling) | Onde a empresa perde faturamento, quanto vale e o plano de ação |
| Detalhe da loja | Drill-through (botão direito numa loja → Detalhar) | Por que uma loja ficou abaixo da meta e o que fazer |
| Dica da região | Dica de ferramenta | Resumo da região ao passar o mouse nas barras de região |

## Como o layout é gerado

O visual do relatório é o do protótipo, sem retrabalho manual no Power BI:

1. `gerador_pbir/fundos/*.html` descreve cada página com o mesmo CSS do protótipo. Tudo o que é estático
   (cards, sombras, ícones, rótulos, cartões de decisão, plano de ação) está no HTML.
2. Onde entra um dado, o HTML tem uma vaga vazia (`data-v="..."`).
3. `gerar_paginas.py` abre o HTML no Chrome sem janela, mede a posição de cada vaga e fotografa a página em 2x.
4. A foto vira a imagem de fundo da página, e cada visual (gráfico, número, título dinâmico, filtro, botão)
   é criado transparente exatamente em cima da sua vaga. Números, títulos e cores continuam vindo das medidas DAX.

Para mudar o layout: editar o HTML (abrir com `?debug` no navegador mostra as vagas) e rodar

```bash
python gerador_pbir/gerar_paginas.py amplo_varejo.Report gerador_pbir/modelos
```

Com o Power BI aberto, aparece "Apply external changes": basta aplicar e clicar em **Atualizar**.

**Link público:** LINK_PUBLICO_POWER_BI
