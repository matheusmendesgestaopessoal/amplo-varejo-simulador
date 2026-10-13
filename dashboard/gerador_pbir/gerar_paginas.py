"""Gera as páginas do dashboard (Power BI Project, formato PBIR) fiéis ao protótipo v2.

Como funciona
  1. O layout de cada página é um HTML em fundos/ (mesmo CSS do protótipo). Tudo o que é
     estático (cards, sombras, ícones, rótulos, cartões de decisão, plano) fica no HTML.
  2. Onde entra um dado, o HTML tem uma "vaga" vazia (atributo data-v).
  3. O Chrome sem janela mede a posição de cada vaga e fotografa a página (2x, para ficar nítida).
  4. A foto vira a imagem de fundo da página no Power BI, e cada visual (gráfico, número,
     título dinâmico, filtro) é criado transparente exatamente em cima da sua vaga.
  Resultado: o relatório fica igual ao protótipo e os números continuam vivos (filtros,
  drill-through, dica de ferramenta).

Os visuais são clonados de modelos que o próprio Power BI gravou (pasta modelos/), trocando só
posição, campos e formatação, para o visual.json continuar válido.

Uso:  python gerar_paginas.py <pasta .Report> <pasta modelos>
"""
import copy
import html as html_lib
import json
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

REPORT = Path(sys.argv[1])
DEF = REPORT / "definition"
MODELOS = Path(sys.argv[2])
FUNDOS = Path(__file__).parent / "fundos"
RECURSOS = REPORT / "StaticResources" / "RegisteredResources"
ESCALA = 2  # resolução da imagem de fundo (2x = nítida em telas de alta densidade)

CHROME = next((c for c in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"] if Path(c).exists()), None)

# ------------------------------------------------------------------ identidade
AZUL, AZUL_TINTA, AZUL_PASTA, AZUL_SEL, AZUL_FUNDO = "#1A6BF5", "#0F4FD1", "#5AB0FF", "#CFE0FF", "#EEF4FF"
VERMELHO, VERM_ESC, VERDE_ESC = "#FF3B3B", "#C41F1F", "#00995A"
GRAFITE, GRAFITE2, TEXTO, DIVISOR, FUNDO = "#111111", "#5E5E5E", "#3F3F3F", "#EFEFED", "#F7F8FA"
FONTES = {
    400: "'''Segoe UI'', wf_segoe-ui_normal, helvetica, arial, sans-serif'",
    600: "'''Segoe UI Semibold'', wf_segoe-ui_semibold, helvetica, arial, sans-serif'",
    700: "'''Segoe UI Bold'', wf_segoe-ui_bold, helvetica, arial, sans-serif'",
    900: "'''Segoe UI Black'', ''Segoe UI Bold'', helvetica, arial, sans-serif'",
}

def pt(px):
    """Tamanho do CSS (px) para o Power BI (pt)."""
    return round(px * 0.75, 1)

# ------------------------------------------------------------------ utilitários JSON
def lit(v):
    return {"expr": {"Literal": {"Value": v}}}

def cor(hexa):
    return {"solid": {"color": lit(f"'{hexa}'")}}

def medida(nome, entidade="_Metas"):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": entidade}}, "Property": nome}}

def cor_medida(nome):
    return {"solid": {"color": {"expr": medida(nome)}}}

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

T = {n: json.loads((MODELOS / f"{n}.json").read_text(encoding="utf-8"))
     for n in ["card", "bar", "slicer", "table", "combo", "button"]}

def filtro_topn(campo, nome_medida, n, direcao):
    """Filtro de visual 'N primeiros' (direcao: 2 = maiores, 1 = menores)."""
    entidade = campo["Column"]["Expression"]["SourceRef"]["Entity"]
    prop = campo["Column"]["Property"]
    return {"name": novo_id(), "field": campo, "type": "TopN", "filter": {"Version": 2, "From": [
        {"Name": "subquery", "Expression": {"Subquery": {"Query": {
            "Version": 2,
            "From": [{"Name": "d", "Entity": entidade, "Type": 0}, {"Name": "_", "Entity": "_Metas", "Type": 0}],
            "Select": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": prop}, "Name": "field"}],
            "OrderBy": [{"Direction": direcao, "Expression": {"Measure": {"Expression": {"SourceRef": {"Source": "_"}}, "Property": nome_medida}}}],
            "Top": n}}}, "Type": 2},
        {"Name": "d", "Entity": entidade, "Type": 0}],
        "Where": [{"Condition": {"In": {
            "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": prop}}],
            "Table": {"SourceRef": {"Source": "subquery"}}}}}]}}


# ------------------------------------------------------------------ fundo: medir e fotografar o HTML
def chrome(*args):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", *args],
                          capture_output=True, text=True, encoding="utf-8", timeout=180)

def medir(html):
    saida = chrome("--window-size=1920,1080", "--dump-dom", html.resolve().as_uri()).stdout
    m = re.search(r'<pre id="posicoes"[^>]*>(.*?)</pre>', saida, re.S)
    if not m:
        sys.exit(f"não consegui medir {html.name}")
    return json.loads(html_lib.unescape(m.group(1)))

def fotografar(html, largura, altura, png):
    chrome(f"--window-size={largura},{altura}", f"--force-device-scale-factor={ESCALA}",
           f"--screenshot={png.resolve()}", html.resolve().as_uri())
    if not png.exists():
        sys.exit(f"não consegui fotografar {html.name}")


class Pagina:
    def __init__(self, nome, titulo, html, largura, tipo=None, oculta=False, binding=None, filtros=None):
        self.id, self.visuais, self.z = nome, [], 0
        pos = medir(FUNDOS / html)
        self.vagas = pos["vagas"]
        altura = pos["altura"] if largura == 1920 and pos["altura"] > 1080 else {1920: 1080, 320: 240}[largura]
        self.imagem = f"fundo_{Path(html).stem}.png"
        RECURSOS.mkdir(parents=True, exist_ok=True)
        fotografar(FUNDOS / html, largura, altura, RECURSOS / self.imagem)
        self.pagina = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
            "name": nome, "displayName": titulo,
            "displayOption": "FitToWidth" if altura > 1080 else "FitToPage",
            "height": altura, "width": largura,
            "objects": {
                "background": [{"properties": {"image": {"image": {
                    "name": lit(f"'{self.imagem}'"),
                    "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1,
                                                              "ItemName": self.imagem}}},
                    "scaling": lit("'Fit'")}}, "transparency": lit("0D")}}],
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

    def _base(self, modelo, vaga):
        x, y, w, h = self.vagas[vaga]
        v = copy.deepcopy(T[modelo])
        v["name"] = novo_id()
        self.z += 1
        v["position"] = {"x": x, "y": y, "z": self.z * 100, "height": h, "width": w, "tabOrder": self.z * 100}
        for k in ("parentGroupName", "howCreated", "filterConfig"):
            v.pop(k, None)
        self.visuais.append(v)
        return v

    @staticmethod
    def _limpo(vis, dica=None):
        """Container transparente: sem título, fundo, borda, sombra ou cabeçalho (o fundo é a imagem)."""
        vis["visualContainerObjects"] = {
            "title": [{"properties": {"show": lit("false")}}],
            "subTitle": [{"properties": {"show": lit("false")}}],
            "background": [{"properties": {"show": lit("false")}}],
            "border": [{"properties": {"show": lit("false")}}],
            "dropShadow": [{"properties": {"show": lit("false")}}],
            "visualHeader": [{"properties": {"show": lit("false")}}],
            "padding": [{"properties": {"top": lit("0D"), "bottom": lit("0D"), "left": lit("0D"), "right": lit("0D")}}],
            "visualTooltip": [{"properties": {"show": lit("true")}}],
        }
        if dica:
            vis["visualContainerObjects"]["visualTooltip"] = [
                {"properties": {"show": lit("true"), "type": lit("'Canvas'"), "section": lit(f"'{dica}'")}}]

    # ---------------- texto vivo (medida de texto ou número num card sem moldura)
    def texto(self, vaga, nome_medida, px=14, c=TEXTO, peso=400, alinhar="left", quebra=False, vertical="top", c_medida=None):
        v = self._base("card", vaga)
        vis = v["visual"]
        vis["query"] = {"queryState": {"Data": {"projections": [proj(medida(nome_medida))]}}}
        o = vis["objects"]
        o["layout"][0]["properties"]["alignment"] = lit(f"'{vertical}'")
        o["value"] = [
            {"properties": {"show": lit("true")}},
            {"properties": {"fontSize": lit(f"{pt(px)}D"), "bold": lit("false"), "fontFamily": lit(FONTES[peso]),
                            "horizontalAlignment": lit(f"'{alinhar}'"), "textWrap": lit("true" if quebra else "false"),
                            "fontColor": cor_medida(c_medida) if c_medida else cor(c)},
             "selector": {"id": "default"}},
        ]
        o["padding"] = [{"properties": {"paddingUniform": lit("0L"), "paddingIndividual": lit("true"), "leftMargin": lit("0L"),
                                        "bottomMargin": lit("0L"), "rightMargin": lit("0L"), "topMargin": lit("0L")},
                         "selector": {"id": "default"}}]
        self._limpo(vis)
        vis["visualContainerObjects"]["visualTooltip"] = [{"properties": {"show": lit("false")}}]  # texto não tem dica
        return v

    def _eixos(self, o, rotulos_px=13):
        o["legend"] = [{"properties": {"show": lit("false")}}]
        o["categoryAxis"] = [{"properties": {"show": lit("true"), "fontFamily": lit(FONTES[400]), "fontSize": lit(f"{pt(rotulos_px)}D"),
                                             "labelColor": cor(GRAFITE2), "showAxisTitle": lit("false"),
                                             "concatenateLabels": lit("false")}}]
        o["valueAxis"] = [{"properties": {"show": lit("false"), "showAxisTitle": lit("false"), "gridlineShow": lit("false"),
                                          "secShow": lit("false"), "secShowAxisTitle": lit("false"), "logAxisScale": lit("false")}}]
        o["zoom"] = [{"properties": {"show": lit("false")}}]

    @staticmethod
    def _rotulos(extra=None, casas=None):
        p = {"show": lit("true"), "color": cor(GRAFITE), "fontSize": lit(f"{pt(13)}D"), "fontFamily": lit(FONTES[600]),
             "enableBackground": lit("false"), "labelDisplayUnits": lit("1D")}  # número cheio, sem "Mil"/"Mi" automático
        if casas is not None:
            p["labelPrecision"] = lit(f"{casas}L")
        r = [{"properties": p}]
        if extra:
            r += extra
        return r

    # ---------------- barras horizontais (ou colunas)
    def barras(self, vaga, categoria, nome_medida, ordem="Descending", c=AZUL, c_medida=None, topn=None, dica=None,
               espaco=30, colunas=False, casas=None):
        v = self._base("bar", vaga)
        vis = v["visual"]
        vis["visualType"] = "clusteredColumnChart" if colunas else "clusteredBarChart"
        m = medida(nome_medida)
        vis["query"] = {
            "queryState": {"Category": {"projections": [proj(categoria, ativo=True)]}, "Y": {"projections": [proj(m)]}},
            "sortDefinition": {"sort": [{"field": categoria if colunas else m, "direction": "Ascending" if colunas else ordem}]},
        }
        o = vis["objects"]
        self._eixos(o)
        o["categoryAxis"][0]["properties"]["innerPadding"] = lit(f"{espaco}L")
        dp = [{"properties": {"fill": cor(c)}}]
        if c_medida:
            dp.append({"properties": {"fill": cor_medida(c_medida)},
                       "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}})
        o["dataPoint"] = dp
        o["labels"] = self._rotulos(casas=casas)
        self._limpo(vis, dica)
        if topn:
            v["filterConfig"] = {"filters": [filtro_topn(categoria, topn[2] if len(topn) > 2 else nome_medida, topn[0], topn[1])]}
        return v

    # ---------------- composição (uma barra 100% empilhada, uma série por medida)
    def composicao(self, vaga, series, espessura=5):
        v = self._base("bar", vaga)
        # o Power BI desenha a barra única com ~1/5 da altura do visual: o visual (transparente) cresce
        # em volta do centro da vaga para a barra ficar com a altura da vaga
        pos = v["position"]
        centro = pos["y"] + pos["height"] / 2
        pos["height"] = round(pos["height"] * espessura)
        pos["y"] = round(centro - pos["height"] / 2)
        vis = v["visual"]
        vis["visualType"] = "hundredPercentStackedBarChart"
        vis["query"] = {"queryState": {"Y": {"projections": [proj(medida(n)) for n, _ in series]}}}
        o = vis["objects"]
        self._eixos(o)
        # eixo ligado (sem campo de categoria ele não mostra nada): desligado, o Power BI ignora os espaçamentos
        o["categoryAxis"][0]["properties"]["innerPadding"] = lit("0L")
        o["categoryAxis"][0]["properties"]["maxMarginFactor"] = lit("0L")
        o["dataPoint"] = [{"properties": {"fill": cor(c)}, "selector": {"metadata": f"_Metas.{n}"}} for n, c in series]
        o["labels"] = [{"properties": {"show": lit("false")}}]
        self._limpo(vis)
        return v

    # ---------------- colunas + linha tracejada (realizado x meta)
    def combo(self, vaga, categoria, medida_col, medida_linha, c_col=AZUL_SEL, c_medida=None, casas=None):
        v = self._base("combo", vaga)
        vis = v["visual"]
        mc, ml = medida(medida_col), medida(medida_linha)
        vis["query"] = {
            "queryState": {"Category": {"projections": [proj(categoria, ativo=True)]},
                           "Y": {"projections": [proj(mc)]}, "Y2": {"projections": [proj(ml)]}},
            "sortDefinition": {"sort": [{"field": categoria, "direction": "Ascending"}]},
        }
        o = vis["objects"]
        # colunas: cor padrão sem seletor (o seletor por série só funciona para a linha neste visual)
        dp = [{"properties": {"fill": cor(c_col)}},
              {"properties": {"fill": cor(VERMELHO)}, "selector": {"metadata": f"_Metas.{medida_linha}"}}]
        if c_medida:
            dp.append({"properties": {"fill": cor_medida(c_medida)},
                       "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}})
        o["dataPoint"] = dp
        o["lineStyles"] = [{"properties": {"strokeShow": lit("true"), "strokeWidth": lit("2D"), "lineStyle": lit("'dashed'"),
                                           "showMarker": lit("false")}}]
        self._eixos(o)
        o["valueAxis"][0]["properties"]["alignZeros"] = lit("true")
        o["labels"] = self._rotulos([{"properties": {"show": lit("false")}, "selector": {"metadata": f"_Metas.{medida_linha}"}}], casas)
        self._limpo(vis)
        return v

    # ---------------- tabela (cabeçalho em maiúsculas, linhas finas, sem moldura)
    def tabela(self, vaga, campos, ordenar=None, direcao="Descending", topn=None, linha=8):
        v = self._base("table", vaga)
        vis = v["visual"]
        vis["query"] = {"queryState": {"Values": {"projections": [proj(c, nome=n) for c, n in campos]}}}
        if ordenar:
            vis["query"]["sortDefinition"] = {"sort": [{"field": ordenar, "direction": direcao}]}
        vis["objects"] = {
            "columnHeaders": [{"properties": {"fontFamily": lit(FONTES[600]), "fontSize": lit(f"{pt(12)}D"), "fontColor": cor(GRAFITE2),
                                              "backColor": cor(FUNDO), "alignment": lit("'Left'"), "wordWrap": lit("true"),
                                              "outlineStyle": lit("0D")}}],
            "values": [{"properties": {"fontFamily": lit(FONTES[400]), "fontSize": lit(f"{pt(15)}D"), "fontColorPrimary": cor(TEXTO),
                                       "fontColorSecondary": cor(TEXTO), "backColorPrimary": cor("#FFFFFF"),
                                       "backColorSecondary": cor("#FFFFFF"), "wordWrap": lit("false"), "outlineStyle": lit("0D")}}],
            "grid": [{"properties": {"gridHorizontal": lit("true"), "gridHorizontalColor": cor(DIVISOR), "gridHorizontalWeight": lit("1D"),
                                     "gridVertical": lit("false"), "outlineColor": cor("#FFFFFF"), "outlineWeight": lit("0D"),
                                     "rowPadding": lit(f"{linha}D")}}],
            "total": [{"properties": {"totals": lit("false")}}],
        }
        self._limpo(vis)
        if topn:
            v["filterConfig"] = {"filters": [filtro_topn(*topn)]}
        return v

    # ---------------- filtro (lista suspensa sem cabeçalho; o rótulo está no fundo)
    def filtro(self, vaga, campo):
        v = self._base("slicer", vaga)
        vis = v["visual"]
        vis["query"] = {"queryState": {"Values": {"projections": [proj(campo, ativo=True)]}}}
        o = vis["objects"]
        o["header"] = [{"properties": {"show": lit("false")}}]
        o["items"] = [{"properties": {"fontFamily": lit(FONTES[600]), "textSize": lit(f"{pt(15)}D"), "fontColor": cor(GRAFITE),
                                      "outlineStyle": lit("0D"), "padding": lit("0D")}}]
        o["selectionIcon"] = [{"properties": {"color": cor(AZUL)}}]
        self._limpo(vis)
        return v

    # ---------------- botão invisível sobre o botão desenhado no fundo
    def botao(self, vaga, acao):
        v = self._base("button", vaga)
        vis = v["visual"]
        o = vis["objects"]
        o["icon"] = [{"properties": {"show": lit("false")}}]
        o["text"] = [{"properties": {"show": lit("false")}}]
        o["outline"] = [{"properties": {"show": lit("false")}}]
        o["fill"] = [{"properties": {"show": lit("true"), "fillColor": cor(AZUL_FUNDO), "transparency": lit("100D")},
                      "selector": {"id": "default"}}]
        o["shape"] = [{"properties": {"tileShape": lit("'rectangle'")}, "selector": {"id": "default"}}]
        vis["visualContainerObjects"] = {
            "visualLink": [{"properties": {"show": lit("true"), "type": lit(f"'{acao}'")}}],
            "title": [{"properties": {"show": lit("false")}}],
            "background": [{"properties": {"show": lit("false")}}],
            "border": [{"properties": {"show": lit("false")}}],
            "visualHeader": [{"properties": {"show": lit("false")}}],
        }
        return v

    def gravar(self):
        pasta = DEF / "pages" / self.id
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
LOJA = coluna("DIM Lojas", "Loja")  # nome curto (ex.: PA 051), também usado no drill-through
REGIAO = coluna("DIM Lojas", "regiao")
MES = coluna("DIM Calendario", "Mes_Abrev")
CATEGORIA = coluna("DIM Produtos", "nome_categoria")
PRODUTO = coluna("DIM Produtos", "nome_produto")
VENDEDOR = coluna("DIM Vendedor", "nome_vendedor")

ID_HIST, ID_LOJA, ID_DICA = "a1d1a9n0o0s1t1i1c0o1", "d2e2t2a2l2h2e2l2o2j2", "d3i3c3a3r3e3g3i3a3o3"


# ====================================================================== PÁGINA 1 · DIAGNÓSTICO
def pagina_diagnostico():
    p = Pagina(ID_HIST, "Diagnóstico", "diagnostico.html", 1920)

    # cabeçalho: filtros e limpar
    for vaga, campo in [("f_mes", MES), ("f_regiao", REGIAO), ("f_loja", LOJA), ("f_categoria", CATEGORIA)]:
        p.filtro(vaga, campo)
    p.botao("b_limpar", "ClearAllSlicers")

    # pergunta + resposta + dinheiro em jogo
    p.texto("t_resposta", "Txt Resposta", px=19, c=TEXTO, quebra=True)
    p.composicao("g_composicao", [("Receita Perdida", AZUL), ("Excesso Estoque", AZUL_PASTA), ("Gap Lojas Abaixo Meta", AZUL_SEL)])
    p.texto("v_comp_cancel", "Txt Receita Perdida", px=15, c=GRAFITE, peso=700, alinhar="right")
    p.texto("v_comp_estoque", "Txt Excesso Estoque", px=15, c=GRAFITE, peso=700, alinhar="right")
    p.texto("v_comp_lojas", "Txt Gap Lojas", px=15, c=GRAFITE, peso=700, alinhar="right")

    # KPIs
    for chave, val, ctx, c_val, c_ctx in [
        ("receita", "Txt KPI Receita", "Txt Meta Receita", "#FFFFFF", "#DCE8FF"),
        ("lucro", "Txt KPI Lucro", "Txt Ctx Margem", GRAFITE, GRAFITE2),
        ("pedidos", "Txt KPI Pedidos", "Txt Ctx Ticket", GRAFITE, GRAFITE2),
        ("cancel", "Txt KPI Cancelamento", "Txt Ctx Cancel Meta", VERMELHO, GRAFITE2),
        ("lojas", "Txt KPI Lojas Meta", "Txt Ctx Lojas Abaixo", GRAFITE, GRAFITE2),
    ]:
        p.texto(f"k_{chave}", val, px=38, c=c_val, peso=900)
        p.texto(f"c_{chave}", ctx, px=14, c=c_ctx, vertical="middle")
    p.texto("p_receita", "Txt Pill Receita", px=13, c="#FFFFFF", peso=700, alinhar="center", vertical="middle")
    p.texto("p_cancel", "Txt Pill Cancelamento", px=13, c=VERM_ESC, peso=700, alinhar="center", vertical="middle")
    p.texto("p_lojas", "Txt Pill Lojas", px=13, c=VERM_ESC, peso=700, alinhar="center", vertical="middle")

    # 01 · contexto
    p.texto("h_contexto", "Txt Titulo Contexto", px=34, c=GRAFITE, peso=700)
    p.combo("g_receita_mes", MES, "Receita Mi", "Meta Mi", c_medida="Cor Receita Mes", casas=1)
    p.barras("g_receita_regiao", REGIAO, "Receita Mi", dica=ID_DICA, espaco=45, casas=1)
    p.barras("g_receita_categoria", CATEGORIA, "Receita Mi", c_medida="Cor Receita Categoria", espaco=45, casas=1)

    # 02 · cancelamentos
    p.texto("h_cancel", "Txt Titulo Cancelamento", px=34, c=GRAFITE, peso=700)
    p.texto("s_cancel", "Txt Badge Cancelamento", px=14, c=VERM_ESC, peso=700, alinhar="center", vertical="middle")
    p.combo("g_cancel_mes", MES, "Taxa Cancelamento", "Meta % Cancelamento", casas=1)
    p.barras("g_cancel_regiao", REGIAO, "Taxa Cancelamento", c_medida="Cor Cancelamento", espaco=45, casas=1)

    # 03 · estoque
    p.texto("h_estoque", "Txt Titulo Estoque", px=34, c=GRAFITE, peso=700)
    p.texto("s_estoque", "Txt Badge Estoque", px=14, c="#8A6400", peso=700, alinhar="center", vertical="middle")
    p.barras("g_excesso_produto", PRODUTO, "Excesso mil", topn=(10, 2, "Excesso Estoque"), espaco=35, casas=0)
    p.tabela("t_excesso", [(PRODUTO, "PRODUTO"), (medida("Estoque mil"), "EM ESTOQUE (R$ MIL)"),
                           (medida("Excesso mil"), "EXCESSO (R$ MIL)"), (medida("Cobertura Estoque (meses)"), "COBERTURA (MESES)")],
             ordenar=medida("Excesso mil"), topn=(PRODUTO, "Excesso Estoque", 10, 2), linha=5)

    # 04 · lojas
    p.texto("h_lojas", "Txt Titulo Lojas", px=34, c=GRAFITE, peso=700)
    p.texto("s_lojas", "Txt Badge Lojas", px=14, c="#8A6400", peso=700, alinhar="center", vertical="middle")
    p.barras("g_lojas", LOJA, "Meta x Realizado %", ordem="Ascending", c_medida="Cor Atingimento",
             topn=(20, 1, "Meta x Realizado %"), espaco=30, casas=1)
    return p


# ====================================================================== PÁGINA 2 · DETALHE DA LOJA
def pagina_loja():
    filtro_nome = novo_id()
    p = Pagina(ID_LOJA, "Detalhe da loja", "detalhe_loja.html", 1920, tipo="Drillthrough", oculta=True,
               binding={"name": novo_id(), "type": "Drillthrough",
                        "parameters": [{"name": novo_id(), "boundFilter": filtro_nome, "fieldExpr": LOJA}]},
               filtros=[{"name": filtro_nome, "field": LOJA, "type": "Categorical", "howCreated": "Drillthrough"}])
    p.botao("b_voltar", "Back")
    p.texto("h_loja", "Txt Titulo Loja", px=19, c=GRAFITE, peso=700)
    for chave, val, ctx, pill, c_val in [
        ("receita", "Txt KPI Loja Receita", "Txt Ctx Loja Meta", "Receita", GRAFITE),
        ("pedidos", "Txt KPI Pedidos", "Txt Ctx Loja Pedidos", "Pedidos", GRAFITE),
        ("ticket", "Txt KPI Ticket", "Txt Ctx Loja Ticket", "Ticket", GRAFITE),
        ("cancel", "Txt KPI Cancelamento", "Txt Ctx Loja Cancelamento", "Cancelamento", VERMELHO),
    ]:
        p.texto(f"k_{chave}", val, px=34, c=c_val, peso=900)
        p.texto(f"c_{chave}", ctx, px=14, c=GRAFITE2, vertical="middle")
        p.texto(f"p_{chave}", f"Txt Pill Loja {pill}", px=13, peso=700, alinhar="center", vertical="middle",
                c_medida=f"Cor Pill Loja {pill}")
    p.texto("k_excesso", "Txt KPI Loja Excesso", px=34, c=GRAFITE, peso=900)

    p.combo("g_loja_mes", MES, "Receita mil", "Meta mil", c_medida="Cor Receita Mes", casas=0)
    p.texto("t_causa", "Txt Causa Loja", px=15, c=TEXTO, quebra=True)
    p.texto("t_agravante", "Txt Agravante Loja", px=15, c=TEXTO, quebra=True)
    p.texto("t_acao", "Txt Acao Loja", px=15, c=TEXTO, quebra=True)

    p.barras("g_loja_categoria", CATEGORIA, "Receita mil", c_medida="Cor Receita Categoria", espaco=45, casas=0)
    p.barras("g_loja_cancel", CATEGORIA, "Taxa Cancelamento", c_medida="Cor Cancelamento", espaco=45, casas=1)
    p.tabela("t_vendedores", [(VENDEDOR, "VENDEDOR"), (medida("Receita mil"), "RECEITA (R$ MIL)"),
                              (medida("Quantidade_Pedidos"), "PEDIDOS"), (medida("Taxa Cancelamento"), "CANCELAMENTO")],
             ordenar=medida("Receita mil"))
    return p


# ====================================================================== PÁGINA 3 · DICA DA REGIÃO
def pagina_dica():
    p = Pagina(ID_DICA, "Dica da região", "dica_regiao.html", 320, tipo="Tooltip", oculta=True,
               binding={"name": novo_id(), "type": "Tooltip", "parameters": []})
    p.texto("h_regiao", "Txt Tooltip Regiao", px=16, c=GRAFITE, peso=700)
    p.texto("t_sub", "Txt Tooltip Sub", px=12, c=GRAFITE2)
    p.barras("g_categorias", CATEGORIA, "Receita Mi", c_medida="Cor Receita Categoria", espaco=35, casas=1)
    p.texto("t_cancel", "Txt Tooltip Cancel", px=13, c=VERMELHO, peso=700, vertical="middle")
    return p


# ====================================================================== gravação e limpeza
def registrar_imagens(paginas):
    """Registra as imagens de fundo em report.json e apaga fundos antigos que ninguém usa."""
    caminho = DEF / "report.json"
    rel = json.loads(caminho.read_text(encoding="utf-8-sig"))
    pacotes = rel.setdefault("resourcePackages", [])
    pacote = next((p for p in pacotes if p["name"] == "RegisteredResources"), None)
    if not pacote:
        pacote = {"name": "RegisteredResources", "type": "RegisteredResources", "items": []}
        pacotes.append(pacote)
    imagens = {p.imagem for p in paginas}
    pacote["items"] = [i for i in pacote["items"] if i.get("type") != "Image"] + \
                      [{"name": n, "path": n, "type": "Image"} for n in sorted(imagens)]
    caminho.write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
    for f in RECURSOS.glob("*.png"):
        if f.name not in imagens:
            f.unlink()


if __name__ == "__main__":
    if not CHROME:
        sys.exit("Chrome ou Edge não encontrado: é usado para medir e fotografar os fundos.")
    paginas = [pagina_diagnostico(), pagina_loja(), pagina_dica()]

    for pasta in (DEF / "pages").iterdir():
        if pasta.is_dir() and pasta.name not in {p.id for p in paginas}:
            shutil.rmtree(pasta)
    if (DEF / "bookmarks").exists():
        shutil.rmtree(DEF / "bookmarks")

    total = sum(p.gravar() for p in paginas)
    registrar_imagens(paginas)
    (DEF / "pages" / "pages.json").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": [p.id for p in paginas], "activePageName": paginas[0].id}, ensure_ascii=False, indent=2), encoding="utf-8")
    for p in paginas:
        tam = (RECURSOS / p.imagem).stat().st_size / 1e6
        print(f"{p.pagina['displayName']:<16} {p.pagina['width']}×{p.pagina['height']:<5} {len(p.visuais):>3} visuais · fundo {tam:.1f} MB")
    print(f"total: {total} visuais")
