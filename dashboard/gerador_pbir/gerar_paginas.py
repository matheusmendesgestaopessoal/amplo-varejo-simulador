"""Gera as páginas do dashboard (formato PBIR do Power BI Project) no padrão do kit.

Estratégia: clona visuais que o próprio Power BI já gravou neste relatório (modelos)
e troca só posição, campos, textos e cores. Assim a estrutura de cada visual.json
continua válida para o Power BI.

Páginas geradas:
  1. Diagnóstico      · história em rolagem (1920 px de largura)
  2. Detalhe da loja  · drill-through por loja (1920 × 1080, oculta)
  3. Dica da região   · tooltip (320 × 240, oculta)

Uso:  python gerar_paginas.py <pasta .Report do projeto> <pasta com os modelos>
"""
import copy
import json
import shutil
import sys
import uuid
from pathlib import Path

REPORT = Path(sys.argv[1]) / "definition"
MODELOS = Path(sys.argv[2])

# ------------------------------------------------------------------ identidade
AZUL, AZUL_TINTA, AZUL_PASTA, AZUL_SEL, AZUL_FUNDO = "#1A6BF5", "#0F4FD1", "#5AB0FF", "#CFE0FF", "#EEF4FF"
AMARELO, VERMELHO, VERDE, VERDE_ESC = "#FFD93D", "#FF3B3B", "#00D980", "#00995A"
GRAFITE, GRAFITE2, TEXTO, BORDA, DIVISOR, FUNDO = "#111111", "#5E5E5E", "#3F3F3F", "#ECECEA", "#EFEFED", "#F7F8FA"
FONTE = "'''Segoe UI'', wf_segoe-ui_normal, helvetica, arial, sans-serif'"
FONTE_SEMI = "'''Segoe UI Semibold'', wf_segoe-ui_semibold, helvetica, arial, sans-serif'"
FONTE_BOLD = "'''Segoe UI Bold'', wf_segoe-ui_bold, helvetica, arial, sans-serif'"

# ------------------------------------------------------------------ utilitários JSON
def lit(v):
    return {"expr": {"Literal": {"Value": v}}}

def cor(hexa):
    return {"solid": {"color": lit(f"'{hexa}'")}}

def medida(nome, entidade="_Metas"):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": entidade}}, "Property": nome}}

def coluna(entidade, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entidade}}, "Property": prop}}

def proj(campo, ativo=False, nome=None):
    ent = campo[next(iter(campo))]["Expression"]["SourceRef"]["Entity"]
    prop = campo[next(iter(campo))]["Property"]
    p = {"field": campo, "queryRef": f"{ent}.{prop}", "nativeQueryRef": prop}
    if ativo:
        p["active"] = True
    if nome:
        p["displayName"] = nome
    return p

def novo_id():
    return uuid.uuid4().hex[:20]

def carregar(caminho):
    return json.loads((MODELOS / caminho).read_text(encoding="utf-8"))

T = {
    "card": carregar("card.json"), "bar": carregar("bar.json"), "text": carregar("text.json"),
    "shape": carregar("shape.json"), "slicer": carregar("slicer.json"), "table": carregar("table.json"),
    "combo": carregar("combo.json"), "button": carregar("button.json"),
}

class Pagina:
    def __init__(self, nome, titulo, largura, altura, tipo=None, oculta=False, binding=None, filtros=None):
        self.id = nome
        self.visuais = []
        self.z = 0
        self.pagina = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
            "name": nome, "displayName": titulo,
            "displayOption": "FitToWidth" if altura > 1080 else "FitToPage",
            "height": altura, "width": largura,
            "objects": {
                "background": [{"properties": {"color": cor(FUNDO), "transparency": lit("0D")}}],
                "outspace": [{"properties": {"color": cor(FUNDO)}}],
            },
        }
        if tipo:
            self.pagina["type"] = tipo
        if oculta:
            self.pagina["visibility"] = "HiddenInViewMode"
        if binding:
            self.pagina["pageBinding"] = binding
        if filtros:
            self.pagina["filterConfig"] = {"filters": filtros}

    def _base(self, modelo, x, y, w, h):
        v = copy.deepcopy(T[modelo])
        v["name"] = novo_id()
        self.z += 1
        v["position"] = {"x": x, "y": y, "z": self.z * 100, "height": h, "width": w, "tabOrder": self.z * 100}
        v.pop("parentGroupName", None)
        v.pop("howCreated", None)
        v.pop("filterConfig", None)
        self.visuais.append(v)
        return v

    # ---------------- forma (fundos de card, faixas coloridas, blocos)
    def forma(self, x, y, w, h, fundo="#FFFFFF", raio=16, borda=BORDA):
        v = self._base("shape", x, y, w, h)
        o = v["visual"]["objects"]
        o["shape"] = [{"properties": {"tileShape": lit("'rectangle'"), "roundEdge": lit(f"{raio}L")}}]
        o["fill"] = [{"properties": {"transparency": lit("0D"), "fillColor": cor(fundo)}, "selector": {"id": "default"}}]
        o["outline"] = ([{"properties": {"show": lit("true"), "lineColor": cor(borda), "weight": lit("1D")}}]
                        if borda else [{"properties": {"show": lit("false")}}])
        o["shadow"] = [{"properties": {"show": lit("false")}}]
        return v

    # ---------------- texto estático
    def texto(self, x, y, w, h, paragrafos, alinhamento="left"):
        """paragrafos: lista de parágrafos; cada um é lista de (texto, tamanho_pt, cor, peso)."""
        v = self._base("text", x, y, w, h)
        pars = []
        for par in paragrafos:
            runs = []
            for t, tam, c, peso in par:
                estilo = {"fontSize": f"{tam}pt", "color": c, "fontFamily": "Segoe UI"}
                if peso:
                    estilo["fontWeight"] = peso
                runs.append({"value": t, "textStyle": estilo})
            pars.append({"textRuns": runs, "horizontalTextAlignment": alinhamento})
        v["visual"]["objects"]["general"] = [{"properties": {"paragraphs": pars}}]
        v["visual"]["visualContainerObjects"] = {"background": [{"properties": {"show": lit("false")}}]}
        return v

    def rotulo(self, x, y, w, texto, c=GRAFITE2):
        return self.texto(x, y, w, 24, [[(texto.upper(), 9, c, "bold")]])

    # ---------------- cartão (valor de uma medida, inclusive textos dinâmicos)
    def cartao(self, x, y, w, h, nome_medida, tam=20, c=GRAFITE, negrito=True, quebra=False, titulo=None):
        v = self._base("card", x, y, w, h)
        vis = v["visual"]
        vis["query"] = {"queryState": {"Data": {"projections": [proj(medida(nome_medida))]}}}
        o = vis["objects"]
        o["value"] = [
            {"properties": {"show": lit("true")}},
            {"properties": {"fontSize": lit(f"{tam}D"), "bold": lit("true" if negrito else "false"),
                            "fontFamily": lit(FONTE_BOLD if negrito else FONTE), "horizontalAlignment": lit("'left'"),
                            "textWrap": lit("true" if quebra else "false"), "fontColor": cor(c)},
             "selector": {"id": "default"}},
        ]
        o["label"] = [{"properties": {"show": lit("false")}, "selector": {"id": "default"}}]
        o["padding"] = [{"properties": {"paddingUniform": lit("0L"), "paddingIndividual": lit("true"), "leftMargin": lit("0L"),
                                        "bottomMargin": lit("0L"), "rightMargin": lit("0L"), "topMargin": lit("0L")},
                         "selector": {"id": "default"}}]
        vco = {
            "border": [{"properties": {"show": lit("false")}}],
            "background": [{"properties": {"show": lit("false")}}],
            "padding": [{"properties": {"top": lit("0D"), "bottom": lit("0D"), "left": lit("0D"), "right": lit("0D")}}],
            "dropShadow": [{"properties": {"show": lit("false")}}],
            "visualHeader": [{"properties": {"show": lit("false")}}],
            "title": [{"properties": {"show": lit("false")}}],
        }
        if titulo:
            vco["title"] = [{"properties": {"show": lit("true"), "text": lit(f"'{titulo}'"), "fontColor": cor(GRAFITE2),
                                            "fontSize": lit("10D"), "fontFamily": lit(FONTE_SEMI), "alignment": lit("'left'")}}]
        vis["visualContainerObjects"] = vco
        return v

    # ---------------- container padrão dos gráficos (card branco, título à esquerda)
    def _container(self, vis, titulo, subtitulo=None, dica=None):
        vco = {
            "title": [{"properties": {"show": lit("true"), "text": lit(f"'{titulo}'"), "fontColor": cor(GRAFITE),
                                      "fontSize": lit("13D"), "fontFamily": lit(FONTE_SEMI), "alignment": lit("'left'"),
                                      "titleWrap": lit("true"), "bold": lit("false")}}],
            "background": [{"properties": {"show": lit("true"), "color": cor("#FFFFFF"), "transparency": lit("0D")}}],
            "border": [{"properties": {"show": lit("true"), "color": cor(BORDA), "radius": lit("16D"), "width": lit("1D")}}],
            "padding": [{"properties": {"top": lit("16D"), "bottom": lit("16D"), "left": lit("20D"), "right": lit("20D")}}],
            "dropShadow": [{"properties": {"show": lit("false")}}],
            "visualHeader": [{"properties": {"show": lit("false")}}],
            "visualTooltip": [{"properties": {"show": lit("true")}}],
        }
        if subtitulo:
            vco["subTitle"] = [{"properties": {"show": lit("true"), "text": lit(f"'{subtitulo}'"), "fontColor": cor(GRAFITE2),
                                               "fontSize": lit("10D"), "fontFamily": lit(FONTE), "alignment": lit("'left'")}}]
        if dica:
            vco["visualTooltip"] = [{"properties": {"show": lit("true"), "type": lit("'ReportPage'"), "section": lit(f"'{dica}'")}}]
        vis["visualContainerObjects"] = vco

    def _rotulos(self, unidades=None, precisao=None, c=GRAFITE):
        props = {"show": lit("true"), "color": cor(c), "fontSize": lit("10D"), "fontFamily": lit(FONTE_SEMI),
                 "enableBackground": lit("false")}
        if unidades:
            props["labelDisplayUnits"] = lit(f"{unidades}D")
        if precisao is not None:
            props["labelPrecision"] = lit(f"{precisao}L")
        return [{"properties": props}]

    # ---------------- barras horizontais / colunas
    def barras(self, x, y, w, h, categoria, nome_medida, titulo, subtitulo=None, ordem="Descending",
               cor_fixa=AZUL, cor_medida=None, unidades=None, precisao=None, topn=None, colunas=False, dica=None):
        v = self._base("bar", x, y, w, h)
        vis = v["visual"]
        vis["visualType"] = "clusteredColumnChart" if colunas else "clusteredBarChart"
        m = medida(nome_medida)
        vis["query"] = {
            "queryState": {"Category": {"projections": [proj(categoria, ativo=True)]}, "Y": {"projections": [proj(m)]}},
            "sortDefinition": {"sort": [{"field": m, "direction": ordem}]},
        }
        if colunas:  # colunas mantêm a ordem natural da categoria (ex.: meses)
            vis["query"]["sortDefinition"] = {"sort": [{"field": categoria, "direction": "Ascending"}]}
        o = vis["objects"]
        o["legend"] = [{"properties": {"show": lit("false")}}]
        o["categoryAxis"] = [{"properties": {"show": lit("true"), "fontFamily": lit(FONTE), "fontSize": lit("10D"),
                                             "labelColor": cor(GRAFITE2), "showAxisTitle": lit("false"),
                                             "concatenateLabels": lit("false"), "innerPadding": lit("25L")}}]
        o["valueAxis"] = [{"properties": {"show": lit("false"), "logAxisScale": lit("false"), "gridlineShow": lit("false"),
                                          "showAxisTitle": lit("false")}}]
        dp = [{"properties": {"fill": cor(cor_fixa)}}]
        if cor_medida:
            dp.append({"properties": {"fill": {"solid": {"color": {"expr": medida(cor_medida)}}}},
                       "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}})
        o["dataPoint"] = dp
        o["labels"] = self._rotulos(unidades, precisao)
        o["zoom"] = [{"properties": {"show": lit("false")}}]
        self._container(vis, titulo, subtitulo, dica)
        if topn:
            entidade = categoria["Column"]["Expression"]["SourceRef"]["Entity"]
            prop = categoria["Column"]["Property"]
            n, direcao = topn  # direcao: 2 = maiores, 1 = menores
            v["filterConfig"] = {"filters": [{
                "name": novo_id(), "field": categoria, "type": "TopN",
                "filter": {"Version": 2, "From": [
                    {"Name": "subquery", "Expression": {"Subquery": {"Query": {
                        "Version": 2,
                        "From": [{"Name": "d", "Entity": entidade, "Type": 0}, {"Name": "_", "Entity": "_Metas", "Type": 0}],
                        "Select": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": prop}, "Name": "field"}],
                        "OrderBy": [{"Direction": direcao, "Expression": {"Measure": {"Expression": {"SourceRef": {"Source": "_"}}, "Property": nome_medida}}}],
                        "Top": n}}}, "Type": 2},
                    {"Name": "d", "Entity": entidade, "Type": 0}],
                    "Where": [{"Condition": {"In": {
                        "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": prop}}],
                        "Table": {"SourceRef": {"Source": "subquery"}}}}}]}}]}
        return v

    # ---------------- colunas + linha (realizado x meta)
    def combo(self, x, y, w, h, categoria, medida_col, medida_linha, titulo, subtitulo=None, unidades=None, precisao=None):
        v = self._base("combo", x, y, w, h)
        vis = v["visual"]
        mc, ml = medida(medida_col), medida(medida_linha)
        vis["query"] = {
            "queryState": {"Category": {"projections": [proj(categoria, ativo=True)]},
                           "Y": {"projections": [proj(mc)]}, "Y2": {"projections": [proj(ml)]}},
            "sortDefinition": {"sort": [{"field": categoria, "direction": "Ascending"}]},
        }
        o = vis["objects"]
        o["dataPoint"] = [{"properties": {"fill": cor(AZUL_SEL)}},
                          {"properties": {"fill": cor(AZUL)}, "selector": {"metadata": f"_Metas.{medida_col}"}},
                          {"properties": {"fill": cor(VERMELHO)}, "selector": {"metadata": f"_Metas.{medida_linha}"}}]
        o["lineStyles"] = [{"properties": {"strokeShow": lit("true"), "strokeWidth": lit("2D"), "lineStyle": lit("'dashed'"),
                                           "showMarker": lit("false")}}]
        o["valueAxis"] = [{"properties": {"show": lit("false"), "secShow": lit("false"), "alignZeros": lit("true"),
                                          "logAxisScale": lit("false"), "gridlineShow": lit("false")}}]
        o["categoryAxis"] = [{"properties": {"show": lit("true"), "fontFamily": lit(FONTE), "fontSize": lit("10D"),
                                             "labelColor": cor(GRAFITE2), "showAxisTitle": lit("false")}}]
        o["labels"] = self._rotulos(unidades, precisao)
        o["legend"] = [{"properties": {"show": lit("true"), "position": lit("'TopLeft'"), "fontSize": lit("9D"),
                                       "labelColor": cor(GRAFITE2), "showTitle": lit("false")}}]
        self._container(vis, titulo, subtitulo)
        return v

    # ---------------- tabela
    def tabela(self, x, y, w, h, campos, titulo, subtitulo=None, ordenar=None, direcao="Ascending", fonte=11):
        v = self._base("table", x, y, w, h)
        vis = v["visual"]
        vis["query"] = {"queryState": {"Values": {"projections": [proj(c, nome=n) for c, n in campos]}}}
        if ordenar:
            vis["query"]["sortDefinition"] = {"sort": [{"field": ordenar, "direction": direcao}]}
        vis["objects"] = {
            "columnHeaders": [{"properties": {"fontFamily": lit(FONTE_SEMI), "fontSize": lit(f"{fonte - 1}D"), "fontColor": cor(GRAFITE2),
                                              "backColor": cor(FUNDO), "alignment": lit("'Left'"), "wordWrap": lit("true")}}],
            "values": [{"properties": {"fontFamily": lit(FONTE), "fontSize": lit(f"{fonte}D"), "fontColorPrimary": cor(GRAFITE),
                                       "fontColorSecondary": cor(GRAFITE), "backColorPrimary": cor("#FFFFFF"),
                                       "backColorSecondary": cor("#FFFFFF"), "wordWrap": lit("true")}}],
            "grid": [{"properties": {"gridHorizontal": lit("true"), "gridHorizontalColor": cor(DIVISOR), "gridVertical": lit("false"),
                                     "outlineStyle": lit("0D"), "rowPadding": lit("6D")}}],
            "total": [{"properties": {"totals": lit("false")}}],
        }
        self._container(vis, titulo, subtitulo)
        return v

    # ---------------- filtro (segmentação em lista suspensa)
    def filtro(self, x, y, w, h, campo, cabecalho):
        v = self._base("slicer", x, y, w, h)
        vis = v["visual"]
        vis["query"] = {"queryState": {"Values": {"projections": [proj(campo, ativo=True)]}}}
        o = vis["objects"]
        o["header"] = [{"properties": {"fontFamily": lit(FONTE_SEMI), "textSize": lit("8D"), "fontColor": cor(GRAFITE2),
                                       "outlineStyle": lit("0D"), "text": lit(f"'{cabecalho}'")}}]
        o["items"] = [{"properties": {"fontFamily": lit(FONTE), "textSize": lit("10D"), "fontColor": cor(GRAFITE),
                                      "outlineStyle": lit("0D")}}]
        vis["visualContainerObjects"] = {
            "background": [{"properties": {"show": lit("true"), "color": cor("#FFFFFF"), "transparency": lit("0D")}}],
            "border": [{"properties": {"show": lit("true"), "color": cor(BORDA), "radius": lit("10D"), "width": lit("1D")}}],
            "padding": [{"properties": {"top": lit("6D"), "bottom": lit("4D"), "left": lit("12D"), "right": lit("8D")}}],
            "visualHeader": [{"properties": {"show": lit("false")}}],
        }
        return v

    # ---------------- botão voltar (drill-through)
    def voltar(self, x, y, w, h):
        v = self._base("button", x, y, w, h)
        vis = v["visual"]
        o = vis["objects"]
        o["text"] = [{"properties": {"show": lit("true")}},
                     {"properties": {"text": lit("'←  Voltar ao diagnóstico'"), "fontSize": lit("11D"), "fontColor": cor(AZUL_TINTA),
                                     "fontFamily": lit(FONTE_SEMI), "bold": lit("true")}, "selector": {"id": "default"}}]
        o["fill"] = [{"properties": {"show": lit("true"), "fillColor": cor(AZUL_FUNDO), "transparency": lit("0D")}, "selector": {"id": "default"}}]
        o["shape"] = [{"properties": {"tileShape": lit("'pill'")}, "selector": {"id": "default"}}]
        vis["visualContainerObjects"] = {"visualLink": [{"properties": {"show": lit("true"), "type": lit("'Back'")}}],
                                         "title": [{"properties": {"show": lit("false")}}]}
        return v

    # ---------------- gravação
    def gravar(self):
        pasta = REPORT / "pages" / self.id
        if pasta.exists():
            shutil.rmtree(pasta)
        (pasta / "visuals").mkdir(parents=True)
        (pasta / "page.json").write_text(json.dumps(self.pagina, ensure_ascii=False, indent=2), encoding="utf-8")
        for v in self.visuais:
            d = pasta / "visuals" / v["name"]
            d.mkdir()
            (d / "visual.json").write_text(json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")
        return len(self.visuais)


# ====================================================================== campos usados
LOJA = coluna("DIM Lojas", "nome_loja")
REGIAO = coluna("DIM Lojas", "regiao")
MES = coluna("DIM Calendario", "Mes_Abrev")
CATEGORIA = coluna("DIM Produtos", "nome_categoria")
PRODUTO = coluna("DIM Produtos", "nome_produto")
VENDEDOR = coluna("DIM Vendedor", "nome_vendedor")
PLANO = lambda c: coluna("Plano_Prescritivo", c)

X0, W, G = 104, 1712, 24

ID_HIST, ID_LOJA, ID_DICA = "a1d1a9n0o0s1t1i1c0o1", "d2e2t2a2l2h2e2l2o2j2", "d3i3c3a3r3e3g3i3a3o3"


def secao(p, y, numero, nome, medida_titulo, frase, prioridade=None):
    """Cabeçalho de seção: rótulo, título-conclusão dinâmico, frase de apoio e selo de prioridade."""
    p.rotulo(X0, y, 600, f"{numero} · {nome}")
    p.cartao(X0, y + 24, 1400, 46, medida_titulo, tam=22, quebra=False)
    p.texto(X0, y + 72, 1400, 26, [[(frase, 11, GRAFITE2, None)]])
    if prioridade:
        texto, fundo, c = prioridade
        p.forma(X0 + W - 300, y + 30, 300, 34, fundo=fundo, raio=17, borda=None)
        p.texto(X0 + W - 300, y + 35, 300, 26, [[(texto, 10, c, "bold")]], alinhamento="center")
    return y + 112


def cartao_decisao(p, y, titulo, etiquetas, fato, interp, acao, rodape, altura=430):
    """Cartão de decisão: Fato · Interpretação · Ação + faixa inferior (causas, resultado, acompanhamento)."""
    p.forma(X0, y, W, altura)
    p.texto(X0 + 28, y + 18, 760, 30, [[(titulo, 13, GRAFITE, "bold")]])
    p.texto(X0 + 800, y + 20, W - 830, 28, [[(etiquetas, 10, GRAFITE2, None)]], alinhamento="right")
    p.forma(X0, y + 58, W, 1, fundo=DIVISOR, raio=0, borda=None)
    col_w = (W - 4 * 28) // 3
    for i, (rot, c, paragrafos) in enumerate([("1  FATO", AZUL_TINTA, fato), ("2  INTERPRETAÇÃO", "#8A6400", interp),
                                              ("3  AÇÃO", VERDE_ESC, acao)]):
        x = X0 + 28 + i * (col_w + 28)
        p.texto(x, y + 74, col_w, 24, [[(rot, 10, c, "bold")]])
        p.texto(x, y + 102, col_w, altura - 102 - 128, [[(t, 11, TEXTO, None)] for t in paragrafos])
    p.forma(X0 + 1, y + altura - 120, W - 2, 119, fundo=FUNDO, raio=16, borda=None)
    rod_w = (W - 4 * 28) // 3
    for i, (rot, txt) in enumerate(rodape):
        x = X0 + 28 + i * (rod_w + 28)
        p.texto(x, y + altura - 108, rod_w, 22, [[(rot.upper(), 9, GRAFITE2, "bold")]])
        p.texto(x, y + altura - 84, rod_w, 76, [[(txt, 10, TEXTO, None)]])
    return y + altura + 48


# ====================================================================== PÁGINA 1 · DIAGNÓSTICO
def pagina_historia():
    p = Pagina(ID_HIST, "Diagnóstico", 1920, 5000)

    # cabeçalho
    p.forma(0, 0, 1920, 84, fundo="#FFFFFF", raio=0, borda=None)
    p.forma(0, 83, 1920, 1, fundo=DIVISOR, raio=0, borda=None)
    p.forma(X0, 22, 40, 40, fundo=AZUL, raio=10, borda=None)
    p.texto(X0, 29, 40, 26, [[("AV", 11, "#FFFFFF", "bold")]], alinhamento="center")
    p.texto(X0 + 54, 16, 760, 30, [[("Amplo Varejo · Diagnóstico de faturamento", 15, GRAFITE, "bold")]])
    p.texto(X0 + 54, 46, 760, 24, [[("Dados sintéticos · jan–dez/2025 · análise de Matheus Mendes", 10, GRAFITE2, None)]])
    p.filtro(1192, 14, 200, 56, REGIAO, "Região")
    p.filtro(1404, 14, 200, 56, LOJA, "Loja")
    p.filtro(1616, 14, 200, 56, MES, "Mês")

    # 1 · pergunta + resposta
    y = 112
    p.forma(X0, y, 1000, 320)
    p.rotulo(X0 + 36, y + 30, 400, "Pergunta central")
    p.texto(X0 + 36, y + 56, 940, 104, [[("Onde a Amplo Varejo está ", 28, GRAFITE, "bold"), ("perdendo", 28, AZUL, "bold"),
                                         (" faturamento?", 28, GRAFITE, "bold")]])
    p.cartao(X0 + 36, y + 178, 930, 124, "Txt Resposta", tam=13, c=TEXTO, negrito=False, quebra=True)
    xr = X0 + 1024
    p.forma(xr, y, W - 1024, 320)
    p.texto(xr + 32, y + 28, 600, 28, [[("Dinheiro em jogo", 13, GRAFITE, "bold")]])
    p.texto(xr + 32, y + 56, 600, 24, [[("Estimativa gerencial para priorização", 10, GRAFITE2, None)]])
    for i, (med, txt, c) in enumerate([("Txt Receita Perdida", "em pedidos cancelados · prioridade alta", VERMELHO),
                                       ("Txt Gap Lojas", "de gap nas lojas abaixo da meta · prioridade média", AZUL_PASTA),
                                       ("Txt Excesso Estoque", "em estoque acima de 3 meses de cobertura · prioridade média", AMARELO)]):
        yy = y + 96 + i * 72
        p.forma(xr + 32, yy, W - 1024 - 64, 60, fundo=FUNDO, raio=12, borda=None)
        p.forma(xr + 32, yy, 6, 60, fundo=c, raio=3, borda=None)
        p.cartao(xr + 56, yy + 14, 190, 34, med, tam=17)
        p.texto(xr + 250, yy + 18, W - 1024 - 300, 28, [[(txt, 11, TEXTO, None)]])

    # KPIs
    y = 456
    kw = (W - 4 * G) // 5
    kpis = [("Receita válida", "Txt KPI Receita", "Txt Ctx Receita", True, GRAFITE),
            ("Lucro", "Txt KPI Lucro", "Txt Ctx Lucro", False, GRAFITE),
            ("Pedidos válidos", "Txt KPI Pedidos", "Txt Ctx Pedidos", False, GRAFITE),
            ("Taxa de cancelamento", "Txt KPI Cancelamento", "Txt Ctx Cancelamento", False, VERMELHO),
            ("Lojas abaixo da meta", "Txt KPI Lojas", "Txt Ctx Lojas", False, GRAFITE)]
    for i, (rot, val, ctx, destaque, c) in enumerate(kpis):
        x = X0 + i * (kw + G)
        p.forma(x, y, kw, 132, fundo=AZUL if destaque else "#FFFFFF", borda=None if destaque else BORDA)
        p.texto(x + 22, y + 16, kw - 44, 24, [[(rot, 10, "#DCE8FF" if destaque else GRAFITE2, "bold")]])
        p.cartao(x + 22, y + 44, kw - 44, 46, val, tam=24, c="#FFFFFF" if destaque else c)
        p.cartao(x + 22, y + 96, kw - 44, 24, ctx, tam=10, c="#DCE8FF" if destaque else GRAFITE2, negrito=False)
    p.texto(X0, y + 142, W, 24, [[("Receita válida = pedidos não cancelados. Ticket médio = receita válida ÷ pedidos válidos. "
                                   "Taxa de cancelamento = cancelados ÷ total de pedidos.", 9, GRAFITE2, None)]])

    # 2 · contexto
    y = secao(p, 652, "01", "Contexto", "Txt Titulo Contexto",
              "Onde, quando e com o quê a Amplo fatura: perdas nesses pontos pesam mais no resultado.")
    p.combo(X0, y, 832, 380, MES, "Receita_Total", "Meta_Faturamento", "Receita válida x meta por mês",
            "R$ · linha tracejada = meta", unidades=1000000, precisao=2)
    p.barras(X0 + 856, y, 416, 380, REGIAO, "Receita_Total", "Receita por região", "R$ · passe o mouse para detalhar",
             unidades=1000000, precisao=2, dica=ID_DICA)
    p.barras(X0 + 1296, y, 416, 380, CATEGORIA, "Receita_Total", "Receita por categoria", "R$", unidades=1000000, precisao=2)

    # 3 · cancelamentos
    y = secao(p, y + 380 + 56, "02", "Cancelamentos", "Txt Titulo Cancelamento",
              "A taxa é parecida em todas as regiões, meses e categorias: o problema é de processo, não de local.",
              ("Prioridade alta · R$ 2,10 Mi", "#FFEDED", "#C41F1F"))
    p.barras(X0, y, 1056, 320, MES, "Taxa Cancelamento", "Taxa de cancelamento por mês", "% dos pedidos · meta de 3%",
             cor_fixa=AZUL_SEL, colunas=True, precisao=1)
    p.barras(X0 + 1080, y, W - 1080, 320, REGIAO, "Taxa Cancelamento", "Taxa de cancelamento por região",
             "% · vermelho = acima da média da rede", cor_medida="Cor Cancelamento", precisao=1)
    y = cartao_decisao(
        p, y + 344, "Cartão de decisão · Cancelamentos acima da meta",
        "Prioridade Alta  ·  Esforço Médio  ·  Confiança na causa Média  ·  Dono Operações + TI",
        ["957 dos 10.708 pedidos de 2025 foram cancelados: 8,9%, contra a meta de 3,0% (3,0×).",
         "A receita desses pedidos soma R$ 2,10 Mi. A taxa vai de 7,1% (Centro-Oeste) a 9,3% (Sul e Sudeste).",
         "Fonte: medidas Taxa Cancelamento e Receita Perdida."],
        ["É a maior perda do ano. Testes qui-quadrado não mostram diferença significativa entre regiões (p = 0,12), "
         "meses (p = 0,38), lojas (p = 0,64) e categorias (p = 0,94).",
         "O cancelamento é igual em todo lugar: aponta para o processo do pedido, não para uma loja ou região.",
         "O que ainda não sabemos: o motivo de cada cancelamento não é registrado."],
        ["1. Tornar obrigatório o motivo do cancelamento. TI · 30 dias",
         "2. Classificar a causa de uma amostra de 200 cancelamentos com a operação. Operações · 2 semanas",
         "3. Corrigir a causa nº 1 e medir a taxa toda semana. Operações + TI · 90 dias"],
        [("Causas prováveis", "Falha no pagamento ou na aprovação (média) · prazo de entrega (baixa) · desistência (baixa). "
                              "Falta de estoque descartada: havia estoque em todas as lojas."),
         ("Resultado esperado em 90 dias", "Taxa de 8,9% para 5,0%. Receita recuperável: R$ 0,69 Mi (6%) · R$ 0,92 Mi (5%) · "
                                           "R$ 1,39 Mi (meta de 3%)."),
         ("Acompanhamento", "KPI: taxa semanal. Revisão em 30 e 90 dias. Gatilho: se em 60 dias a taxa não ficar abaixo de 8%, "
                            "rever a causa priorizada.")])

    # 4 · lojas
    y = secao(p, y, "03", "Lojas", "Txt Titulo Lojas",
              "Clique com o botão direito numa loja e escolha Detalhar para ver o diagnóstico individual.",
              ("Prioridade média · R$ 1,64 Mi", "#FFF4CC", "#8A6400"))
    p.barras(X0, y, 1000, 560, LOJA, "Meta x Realizado %", "As 20 lojas com menor atingimento da meta",
             "% da meta de faturamento · vermelho = abaixo de 100%", ordem="Ascending", cor_medida="Cor Atingimento",
             precisao=1, topn=(20, 1))
    p.tabela(X0 + 1024, y, W - 1024, 560,
             [(LOJA, "Loja"), (medida("Receita_Total"), "Receita"), (medida("Meta_Faturamento"), "Meta"),
              (medida("Meta x Realizado %"), "Atingimento")],
             "Receita x meta por loja", "Ordenado pelo menor atingimento", ordenar=medida("Meta x Realizado %"))
    y = cartao_decisao(
        p, y + 584, "Cartão de decisão · Lojas abaixo da meta",
        "Prioridade Média  ·  Esforço Alto  ·  Confiança na causa Média  ·  Dono Gestão de lojas",
        ["A rede atingiu 95,5% da meta: R$ 21,66 Mi de R$ 22,67 Mi.",
         "35 de 54 lojas ficaram abaixo. As 19 abaixo de 90% concentram R$ 1,34 Mi dos R$ 1,64 Mi de gap (82%).",
         "Menor atingimento: PA 051, com 72%."],
        ["O gap está concentrado: tratar 19 lojas resolve a maior parte do problema.",
         "Cada loja tem uma causa diferente (fluxo, ticket ou cancelamento). Por isso o diagnóstico é individual, "
         "na página de detalhe da loja."],
        ["1. Abrir o detalhe das 19 lojas e classificar a causa dominante. Gestão de lojas · 2 semanas",
         "2. Aplicar a ação de cada causa: campanha local (fluxo), treino de venda (ticket) ou revisão da meta.",
         "3. Acompanhar o atingimento mensal de cada loja."],
        [("Causas prováveis", "Varia por loja; a página de detalhe calcula a causa dominante a partir de pedidos, "
                              "ticket e cancelamento comparados com a rede."),
         ("Resultado esperado em 60 a 90 dias", "Fechar de 30% a 60% do gap das 19 lojas: R$ 0,40 a 0,80 Mi."),
         ("Acompanhamento", "KPI: atingimento mensal por loja. Gatilho: loja que não subir 5 p.p. em 60 dias "
                            "tem a causa revista.")],
        altura=380)

    # 5 · estoque
    y = secao(p, y, "04", "Estoque", "Txt Titulo Estoque",
              "Poucos produtos de ticket alto concentram o excesso: a ação é dirigida e rápida.",
              ("Prioridade média · R$ 1,56 Mi", "#FFF4CC", "#8A6400"))
    p.barras(X0, y, 1000, 400, PRODUTO, "Excesso Estoque", "Os 10 produtos com mais excesso de estoque",
             "R$ a custo acima de 3 meses de cobertura", cor_fixa=AMARELO, unidades=1000, precisao=0, topn=(10, 2))
    p.barras(X0 + 1024, y, W - 1024, 400, CATEGORIA, "Excesso Estoque", "Excesso por categoria", "R$ a custo",
             cor_fixa=AMARELO, unidades=1000, precisao=0)
    y = cartao_decisao(
        p, y + 424, "Cartão de decisão · Estoque acima de 3 meses de cobertura",
        "Prioridade Média  ·  Esforço Baixo  ·  Confiança Alta  ·  Dono Estoque + Compras",
        ["O estoque final vale R$ 4,56 Mi a custo, cerca de 4 meses de venda.",
         "R$ 1,56 Mi (34%) está acima de 3 meses de cobertura. 10 dos 80 produtos concentram metade do excesso.",
         "273 combinações de loja e produto não venderam nada no ano (R$ 282 mil)."],
        ["É capital parado em itens caros (MacBook, Desktop Gamer, TVs, notebooks), que ocupa espaço e perde valor.",
         "Como o excesso está concentrado em poucos produtos, a ação é dirigida e pode começar já."],
        ["1. Transferir excedentes entre lojas da mesma região. Estoque · 30 dias",
         "2. Pausar compras dos 10 itens até a cobertura voltar a 3 meses. Compras · imediato",
         "3. Promoção dirigida para os itens sem venda. Comercial · 60 dias"],
        [("Causas prováveis", "Compra acima da demanda em itens de alto valor; sem reposição ajustada à venda de cada loja."),
         ("Resultado esperado em 60 dias", "Liberar de 40% a 70% do excesso: R$ 0,63 a 1,09 Mi em caixa."),
         ("Acompanhamento", "KPI: cobertura por produto e loja. Gatilho: item acima de 4 meses de cobertura entra "
                            "na lista de promoção.")],
        altura=380)

    # 6 · recomendação (o único bloco azul)
    p.forma(X0, y, W, 640, fundo=AZUL, borda=None)
    p.rotulo(X0 + 40, y + 34, 600, "05 · Recomendação", c="#CFE0FF")
    p.texto(X0 + 40, y + 62, W - 80, 90, [[("Recomendo começar pelos cancelamentos: é a maior perda, a primeira ação custa pouco "
                                             "(registrar o motivo) e o retorno começa em 30 dias.", 22, "#FFFFFF", "bold")]])
    p.texto(X0 + 40, y + 156, W - 80, 30, [[("As três frentes podem recuperar de R$ 1,7 a 3,3 Mi em receita e caixa em até 90 dias "
                                              "(estimativa gerencial para priorização).", 12, "#E6EEFF", None)]])
    p.tabela(X0 + 40, y + 206, W - 80, 220,
             [(PLANO("Frente"), "Frente"), (PLANO("Decisão"), "Decisão"), (PLANO("Dono"), "Dono"), (PLANO("Prazo"), "Prazo"),
              (PLANO("Indicador"), "Indicador"), (PLANO("Valor recuperável"), "Valor recuperável"),
              (PLANO("Esforço"), "Esforço"), (PLANO("Confiança"), "Confiança")],
             "Plano de ação", "Ordem sugerida", ordenar=PLANO("Ordem"))
    p.forma(X0 + 40, y + 446, W - 80, 160, fundo="#FFFFFF", borda=None)
    p.texto(X0 + 68, y + 462, 700, 26, [[("Decisões pedidas à diretoria", 13, GRAFITE, "bold")]])
    p.texto(X0 + 68, y + 494, W - 136, 104, [
        [("1. Aprovar o campo obrigatório de motivo de cancelamento (custo baixo).", 11, TEXTO, None)],
        [("2. Autorizar a amostragem de 200 cancelamentos com a operação.", 11, TEXTO, None)],
        [("3. Pausar as compras dos 10 produtos com mais excesso de estoque.", 11, TEXTO, None)],
        [("4. Autorizar o diagnóstico individual das 19 lojas abaixo de 90% da meta.", 11, TEXTO, None)]])
    y += 640 + 28

    # rodapé de método
    p.texto(X0, y, W, 48, [[("Dados: sintéticos, gerados em Python com regras de negócio (jan–dez/2025)  ·  Modelo: MySQL → ETL → "
                              "Star Schema (6 dimensões, 3 fatos)  ·  Métricas: DAX documentadas no repositório  ·  "
                              "Matheus Mendes, Analista de Dados", 9, GRAFITE2, None)]])
    p.pagina["height"] = y + 72
    return p


# ====================================================================== PÁGINA 2 · DETALHE DA LOJA
def pagina_loja():
    filtro_nome = novo_id()
    p = Pagina(ID_LOJA, "Detalhe da loja", 1920, 1080, tipo="Drillthrough", oculta=True,
               binding={"name": novo_id(), "type": "Drillthrough",
                        "parameters": [{"name": novo_id(), "boundFilter": filtro_nome, "fieldExpr": LOJA}]},
               filtros=[{"name": filtro_nome, "field": LOJA, "type": "Categorical", "howCreated": "Drillthrough"}])
    p.forma(0, 0, 1920, 84, fundo="#FFFFFF", raio=0, borda=None)
    p.forma(0, 83, 1920, 1, fundo=DIVISOR, raio=0, borda=None)
    p.voltar(X0, 20, 250, 44)
    p.texto(X0 + 280, 12, 900, 24, [[("Diagnóstico de faturamento / Detalhe da loja", 10, GRAFITE2, None)]])
    p.cartao(X0 + 280, 36, 1300, 36, "Txt Titulo Loja", tam=17)

    y = 108
    kw = (W - 4 * G) // 5
    kpis = [("Receita válida", "Txt KPI Loja Receita", "Txt Ctx Loja Receita", GRAFITE),
            ("Pedidos válidos", "Txt KPI Pedidos", "Txt Ctx Loja Pedidos", GRAFITE),
            ("Ticket médio", "Txt KPI Ticket", "Txt Ctx Loja Ticket", GRAFITE),
            ("Taxa de cancelamento", "Txt KPI Cancelamento", "Txt Ctx Loja Cancelamento", VERMELHO)]
    for i, (rot, val, ctx, c) in enumerate(kpis):
        x = X0 + i * (kw + G)
        p.forma(x, y, kw, 132)
        p.texto(x + 22, y + 16, kw - 44, 24, [[(rot, 10, GRAFITE2, "bold")]])
        p.cartao(x + 22, y + 44, kw - 44, 46, val, tam=24, c=c)
        p.cartao(x + 22, y + 96, kw - 44, 24, ctx, tam=10, c=GRAFITE2, negrito=False)
    x = X0 + 4 * (kw + G)
    p.forma(x, y, kw, 132)
    p.texto(x + 22, y + 16, kw - 44, 24, [[("Cobertura de estoque (meses)", 10, GRAFITE2, "bold")]])
    p.cartao(x + 22, y + 44, kw - 44, 46, "Cobertura Estoque (meses)", tam=24)
    p.texto(x + 22, y + 96, kw - 44, 24, [[("Saudável: até 3 meses", 10, GRAFITE2, None)]])

    y = 264
    p.combo(X0, y, 1000, 400, MES, "Receita_Total", "Meta_Faturamento", "Receita válida x meta da loja",
            "R$ · linha tracejada = meta", unidades=1000, precisao=0)
    xr = X0 + 1024
    p.forma(xr, y, W - 1024, 400)
    p.texto(xr + 28, y + 22, 600, 28, [[("Diagnóstico da loja", 13, GRAFITE, "bold")]])
    p.texto(xr + 28, y + 50, 620, 22, [[("Causa dominante calculada a partir de pedidos, ticket e cancelamento x rede", 10, GRAFITE2, None)]])
    p.forma(xr + 28, y + 88, W - 1024 - 56, 150, fundo=FUNDO, raio=12, borda=None)
    p.forma(xr + 28, y + 88, 5, 150, fundo=VERMELHO, raio=2, borda=None)
    p.texto(xr + 48, y + 100, 400, 22, [[("FATO E CAUSA", 9, "#C41F1F", "bold")]])
    p.cartao(xr + 48, y + 124, W - 1024 - 96, 104, "Txt Diagnostico Loja", tam=12, c=TEXTO, negrito=False, quebra=True)
    p.forma(xr + 28, y + 254, W - 1024 - 56, 120, fundo=FUNDO, raio=12, borda=None)
    p.forma(xr + 28, y + 254, 5, 120, fundo=VERDE, raio=2, borda=None)
    p.texto(xr + 48, y + 266, 400, 22, [[("AÇÃO RECOMENDADA", 9, VERDE_ESC, "bold")]])
    p.cartao(xr + 48, y + 290, W - 1024 - 96, 74, "Txt Acao Loja", tam=12, c=TEXTO, negrito=False, quebra=True)

    y = 688
    cw = (W - 2 * G) // 3
    p.barras(X0, y, cw, 360, CATEGORIA, "Receita_Total", "Receita por categoria", "R$", unidades=1000, precisao=0)
    p.barras(X0 + cw + G, y, cw, 360, CATEGORIA, "Taxa Cancelamento", "Cancelamento por categoria",
             "% · vermelho = acima da rede", cor_medida="Cor Cancelamento", precisao=1)
    p.tabela(X0 + 2 * (cw + G), y, cw, 360, [(VENDEDOR, "Vendedor"), (medida("Receita_Total"), "Receita"),
                                             (medida("Quantidade_Pedidos"), "Pedidos"), (medida("Taxa Cancelamento"), "Cancelamento")],
             "Vendedores", "Ordenado pela receita", ordenar=medida("Receita_Total"), direcao="Descending")
    return p


# ====================================================================== PÁGINA 3 · DICA DA REGIÃO
def pagina_dica():
    p = Pagina(ID_DICA, "Dica da região", 320, 240, tipo="Tooltip", oculta=True,
               binding={"name": novo_id(), "type": "Tooltip", "parameters": []})
    p.pagina["objects"]["background"] = [{"properties": {"color": cor("#FFFFFF"), "transparency": lit("0D")}}]
    p.cartao(14, 10, 292, 44, "Txt Tooltip Regiao", tam=10, quebra=True)
    v = p.barras(6, 56, 308, 178, CATEGORIA, "Receita_Total", "Receita por categoria", unidades=1000000, precisao=2)
    v["visual"]["visualContainerObjects"]["border"] = [{"properties": {"show": lit("false")}}]
    return p


# ====================================================================== gravação e limpeza
if __name__ == "__main__":
    paginas = [pagina_historia(), pagina_loja(), pagina_dica()]

    # remove as páginas e os marcadores antigos (há backup completo do projeto)
    for pasta in (REPORT / "pages").iterdir():
        if pasta.is_dir() and pasta.name not in {p.id for p in paginas}:
            shutil.rmtree(pasta)
    if (REPORT / "bookmarks").exists():
        shutil.rmtree(REPORT / "bookmarks")

    total = sum(p.gravar() for p in paginas)
    (REPORT / "pages" / "pages.json").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": [p.id for p in paginas], "activePageName": paginas[0].id}, ensure_ascii=False, indent=2), encoding="utf-8")
    for p in paginas:
        print(f"{p.pagina['displayName']:<18} {p.pagina['width']}×{p.pagina['height']:<5} {len(p.visuais)} visuais")
    print(f"total: {total} visuais")
