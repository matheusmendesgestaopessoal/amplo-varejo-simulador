<!-- Banner: adicionar assets/banner.png (modelo do kit-projetos-dados) e descomentar a linha abaixo -->
<!-- ![Amplo Varejo S.A.](assets/banner.png) -->

# Amplo Varejo S.A. · Onde a empresa perde faturamento

> Simulei a operação de uma rede varejista nacional, do banco de dados ao dashboard, para responder **onde a empresa perde faturamento, quanto isso vale e por onde começar a recuperar**.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?logo=mysql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-DAX-F2C811?logo=powerbi&logoColor=black)
![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-1A6BF5)

**[📊 Ver o dashboard](#-o-dashboard)** · **[📥 Abrir no Power BI](#como-abrir-o-dashboard)** · **[📄 Análise e recomendações](docs/05_analise_e_recomendacoes.md)** · **[🌐 Portfólio](https://portfolio-phi-lilac-19.vercel.app/)**

---

## Em 30 segundos

| | |
|---|---|
| **Problema** | A diretoria não sabe onde a operação deixa faturamento na mesa: pedidos cancelados, lojas abaixo da meta e capital parado em estoque. |
| **Pergunta** | Onde a Amplo Varejo está perdendo faturamento em 2025, quanto isso vale e por onde começar a recuperar? |
| **O que fiz** | Gerei os dados com regras de negócio em Python, modelei um banco operacional e um Data Warehouse em MySQL, construí o dashboard em Power BI e testei as causas com estatística. |
| **Resultado** | 3 frentes de perda com **R$ 1,7 a 3,3 Mi recuperáveis**. A maior é o cancelamento (8,9% contra meta de 3%, R$ 2,10 Mi), que é igual em todas as regiões e lojas: o problema está no processo do pedido. |
| **Recomendação** | Começar pelos cancelamentos: a primeira ação custa pouco (registrar o motivo de cada cancelamento) e o retorno começa em 30 dias. |

![Primeira tela do dashboard](dashboard/prints/01_diagnostico.png)

<sub>Primeira tela da página Diagnóstico: a pergunta, a resposta e o dinheiro em jogo antes de qualquer rolagem. Todos os números e títulos são medidas DAX e mudam com os filtros.</sub>

---

## 📊 O dashboard

Uma página de diagnóstico em rolagem (contada como história: contexto → achados → decisão), uma página de detalhe por loja e uma dica de ferramenta por região. O layout segue a mesma identidade visual do meu portfólio, em versão de ferramenta de trabalho.

**01 · Contexto.** Onde, quando e com o quê a Amplo fatura. Os 2 meses de maior receita ficam em azul; a linha tracejada é a meta.

![Contexto: receita por mês, região e categoria](dashboard/prints/02_contexto.png)

**02 · Cancelamentos, com o cartão de decisão.** Cada achado termina num cartão com fato, interpretação, ação, causas prováveis, resultado esperado e gatilho de acompanhamento.

![Cancelamentos e cartão de decisão](dashboard/prints/03_cancelamentos.png)

<table>
<tr>
<td width="50%"><b>03 · Estoque.</b> Os 10 produtos com mais excesso e a cobertura de cada um.<br><br><img src="dashboard/prints/04_estoque.png" alt="Estoque acima de 3 meses de cobertura"></td>
<td width="50%"><b>04 · Lojas.</b> As 20 lojas com menor atingimento e a ação para cada causa.<br><br><img src="dashboard/prints/05_lojas.png" alt="Lojas abaixo da meta"></td>
</tr>
</table>

**05 · Recomendação.** O fechamento: por que essa ordem, as decisões pedidas à diretoria e o plano com dono, prazo e valor.

![Recomendação e plano de ação](dashboard/prints/06_recomendacao.png)

<table>
<tr>
<td width="62%"><b>Detalhe da loja (drill-through).</b> Botão direito numa loja → Detalhar. A página compara a loja com a rede e calcula a causa dominante (aqui, PA 051: 64% menos pedidos que a média).<br><br><img src="dashboard/prints/07_detalhe_loja.png" alt="Detalhe da loja PA 051"></td>
<td width="38%"><b>Dica da região.</b> Ao passar o mouse numa região: receita por categoria e taxa de cancelamento.<br><br><img src="dashboard/prints/08_dica_regiao.png" alt="Dica de ferramenta da região"></td>
</tr>
</table>

📄 [Página Diagnóstico inteira](dashboard/prints/00_diagnostico_completo.png) · [Como o layout foi construído](dashboard/README.md)

### Como abrir o dashboard

O relatório vem com os dados, então não precisa instalar banco nenhum:

1. Baixe o repositório: botão verde **Code → Download ZIP** (ou `git clone`) e extraia.
2. Instale o [Power BI Desktop](https://www.microsoft.com/pt-br/power-platform/products/power-bi/desktop) (gratuito, Windows).
3. Abra `dashboard/amplo_varejo.pbip`.
4. Use os filtros do topo, passe o mouse nas barras de região e clique com o botão direito numa loja → **Detalhar**. No Power BI Desktop, os botões (Limpar filtros, Voltar) funcionam com **Ctrl + clique**.

---

## 1. Pergunta

**Contexto:** a Amplo Varejo S.A. é uma rede varejista **fictícia** com 54 lojas nos 27 estados. Todos os dados são sintéticos, gerados por um simulador com regras de negócio reais (sazonalidade, campanhas, eventos, metas e estoque).

**Problema de negócio:** a empresa fechou 2025 a 95,5% da meta, com quase 1 em cada 11 pedidos cancelado e estoque acima do necessário, sem saber qual dessas perdas atacar primeiro.

**Pergunta central:**
> *"Onde a Amplo Varejo está perdendo faturamento em 2025, quanto isso vale e por onde começar a recuperar?"*

**Perguntas de apoio:**
- O cancelamento está concentrado em alguma região, loja, mês ou categoria?
- Quantas lojas ficaram abaixo da meta e quanto do gap elas concentram?
- Quanto capital está parado em estoque acima da cobertura saudável, e em quais produtos?

📄 [Documento de abertura](docs/01_abertura.md)

## 2. Dados

| Fonte | Tipo | Volume | Período | Licença |
|---|---|---|---|---|
| Simulador próprio (Python + Faker) | Sintético | 10.708 pedidos · 21.339 itens · 7.500 clientes · 54 lojas · 100 vendedores · 80 produtos | 2025 | Dados fictícios, sem restrição de uso |

**Qualidade:** antes da exportação, validações automáticas conferem cobertura (27 estados com lojas, vendedores e pedidos), integridade referencial e estoque sem saldo negativo. Na revisão de outubro de 2026 corrigi a escala de metas e estoque, a semente do simulador e cinco medidas DAX. Ver o [registro de correções](docs/06_registro_de_correcoes.md).

📄 [Regras de negócio](docs/02_regras_de_negocio.md) · [Dicionário de dados](docs/04_dicionario_de_dados.md)

## 3. Modelo

**Arquitetura.** Oito etapas, do parâmetro de simulação à recomendação. Se alguma validação falha, o pipeline para e nada é exportado.

![Arquitetura do pipeline](assets/arquitetura.png)

**Banco operacional (OLTP).** 15 tabelas em 4 grupos: cadastros mestres, operações comerciais, operações logísticas e gestão e apoio. O banco é abastecido só pelo simulador, nunca à mão.

![Modelo físico do banco operacional](assets/mer_oltp.png)

**Data Warehouse em estrela.** 3 fatos (`fato_vendas` por item de pedido, `fato_movimentacao_estoque` por movimentação, `fato_metas` por loja e mês) e 6 dimensões desnormalizadas. Esse desenho deixa as medidas DAX simples e permite cruzar venda, meta e estoque pela mesma loja e produto.

![Modelo dimensional](assets/modelo_dimensional.png)

<sub>Os diagramas são gerados a partir do próprio SQL (`assets/fontes/gerar_diagramas.py`): tabelas, tipos, chaves e relacionamentos não são desenhados à mão.</sub>

📄 [Requisitos](docs/03_requisitos.md) · [SQL](sql/) · [Código](codigo/)

## 4. Insights

1. **Cancelamento de 8,9%, três vezes a meta, com R$ 2,10 Mi em pedidos perdidos.** O teste qui-quadrado não mostra diferença entre regiões (p = 0,12), meses (p = 0,38), lojas (p = 0,64) nem categorias (p = 0,94): a causa é o processo do pedido, não um lugar.
2. **35 de 54 lojas abaixo da meta, com gap de R$ 1,64 Mi.** As 19 lojas abaixo de 90% concentram 82% do gap, então o diagnóstico pode ser dirigido.
3. **R$ 1,56 Mi em estoque acima de 3 meses de cobertura (34% do estoque).** Dez produtos de alto valor concentram metade do excesso, e 273 combinações de loja e produto não venderam nada no ano.

Todos os números podem ser recalculados com `python -m codigo.analises.diagnostico`.

## 5. Ação

> **Recomendo começar pelos cancelamentos:** é a maior perda, a primeira ação custa pouco (registrar o motivo de cada cancelamento) e o retorno começa em 30 dias.

| Ordem | Frente | Decisão | Dono | Valor recuperável | Prioridade |
|:---:|---|---|---|---:|:---:|
| 1 | Cancelamentos | Registrar o motivo, auditar o fluxo do pedido e corrigir a causa nº 1 | Operações + TI | R$ 0,69 a 1,39 Mi | 🔴 Alta |
| 2 | Estoque excedente | Redistribuir, pausar compras e promover os 10 itens com mais excesso | Estoque + Compras | R$ 0,63 a 1,09 Mi em caixa | 🟠 Média |
| 3 | Lojas abaixo da meta | Diagnóstico individual das 19 lojas abaixo de 90% | Gestão de lojas | R$ 0,40 a 0,80 Mi | 🟠 Média |

Cada frente tem um cartão de decisão com fato, interpretação, causas, validação, ação, resultado esperado e acompanhamento.

📄 [Análise e recomendações completas](docs/05_analise_e_recomendacoes.md)

---

## Stack

| Etapa | Ferramentas |
|---|---|
| Dados | Python, Pandas, NumPy, Faker |
| Modelo | MySQL (OLTP e Data Warehouse), SQL, SQLAlchemy |
| Análise | Python (teste qui-quadrado, diagnóstico reprodutível) |
| Visualização | Power BI (PBIP), DAX, layout em HTML/CSS gerado por script |

## Como executar o projeto

```bash
git clone https://github.com/matheusmendesgestaopessoal/amplo-varejo-simulador.git
cd amplo-varejo-simulador
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # depois preencha o .env com os dados do seu MySQL
```

Antes da primeira carga, crie os bancos com [`sql/01_modelo_fisico_bd.sql`](sql/01_modelo_fisico_bd.sql) e [`sql/02_star_schema.sql`](sql/02_star_schema.sql).

Para usar **os dados publicados** (os da análise), carregue os CSVs no banco e no DW:

```bash
python -c "from codigo.exportadores.exportar_mysql import exportar_mysql; exportar_mysql()"
python -c "from codigo.dw.atualizar_dw import executar_carga_dw; executar_carga_dw()"
python -m codigo.analises.diagnostico      # confere todos os números da análise
```

Para gerar **uma simulação nova** (reprodutível com `SEMENTE_ALEATORIA`, mas diferente da publicada):

```bash
python -m codigo.pipeline
```

Volume, período e semente ficam em `codigo/configuracoes/configuracao.py`. Depois de recarregar o banco, clique em **Atualizar** no Power BI.

## Estrutura

```
amplo-varejo-simulador/
├── codigo/
│   ├── analises/          # diagnostico.py: recalcula os números da análise
│   ├── configuracoes/     # parâmetros da simulação e conexão com o banco
│   ├── correcoes/         # correção de escala de metas e estoque (out/2026)
│   ├── dw/                # ETL do OLTP para o Data Warehouse
│   ├── exportadores/      # CSV e MySQL
│   ├── geradores/         # dados mestres, operações e motor da simulação
│   ├── simulacao/         # calendário, sazonalidade, campanhas, eventos, metas
│   ├── utilitarios/
│   ├── validacoes/        # cobertura, integridade e estoque
│   └── pipeline.py
├── dados/brutos_csv/      # dados publicados (15 tabelas)
├── dashboard/
│   ├── amplo_varejo.pbip  # projeto Power BI (relatório + modelo semântico + dados)
│   ├── gerador_pbir/      # gera as páginas do relatório a partir do layout em HTML
│   ├── prints/            # imagens das páginas, tiradas do Power BI
│   └── prototipo/         # protótipo de layout aprovado antes do Power BI
├── docs/                  # 01 abertura · 02 regras · 03 requisitos · 04 dicionário · 05 análise · 06 correções
├── sql/                   # modelo físico, star schema, joins e views
├── assets/                # diagramas do README (fontes/ gera as imagens a partir do SQL)
├── .env.example
└── requirements.txt
```

## Limitações e próximos passos

- Dados **sintéticos** de um único ano: o projeto mede perdas dentro de 2025, não compara anos.
- Os valores de impacto são **estimativas gerenciais para priorização**, não perdas auditadas.
- O status dos pedidos é sorteado com probabilidade fixa, por isso o cancelamento é uniforme. Numa empresa real, o mesmo teste separa problema de processo de problema local.
- Próximos passos: registrar o motivo do cancelamento na simulação, simular fluxo de clientes nas lojas (para separar atração de conversão) e gerar mais de um ano para análise de tendência.

---

## Autor

<table>
<tr>
<td width="170" valign="top"><img src="assets/autor.png" width="150" alt="Foto de Matheus Mendes"></td>
<td valign="top">

### Matheus Mendes
**Analista de Dados** · SQL · Python · Power BI

Antes dos dados, passei mais de três anos na operação: programação, medição e faturamento em empresas de engenharia e manutenção, acompanhando cerca de 3 mil ordens de serviço por mês e transformando planilhas em relatórios de indicadores. Foi digitalizando a emissão de ordens de serviço, que antes era em papel, que vi o impacto de dados bem organizados.

Hoje curso Análise e Desenvolvimento de Sistemas e uso cada projeto para praticar o ciclo completo, da pergunta de negócio à recomendação. Neste, fiz tudo de ponta a ponta: regras de negócio, simulação, modelagem, ETL, DAX, design do dashboard e análise.

**Busco minha primeira vaga como analista de dados.** Se este projeto fez sentido para você, vamos conversar.

[![Portfólio](https://img.shields.io/badge/Portf%C3%B3lio-1A6BF5?style=for-the-badge&logo=googlechrome&logoColor=white)](https://portfolio-phi-lilac-19.vercel.app/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/matheusmendes-dados)
[![GitHub](https://img.shields.io/badge/GitHub-111111?style=for-the-badge&logo=github&logoColor=white)](https://github.com/matheusmendesgestaopessoal)
[![E-mail](https://img.shields.io/badge/E--mail-5E5E5E?style=for-the-badge&logo=gmail&logoColor=white)](mailto:matheus.mendesgestao@gmail.com)

</td>
</tr>
</table>
