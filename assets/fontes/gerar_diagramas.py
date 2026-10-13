"""Gera as imagens de modelo do README (assets/*.png) na identidade visual do dashboard.

- mer_oltp.png            banco operacional (lido de sql/01_modelo_fisico_bd.sql)
- modelo_dimensional.png  Data Warehouse em estrela (lido de sql/02_star_schema.sql)
- arquitetura.png         fluxo do pipeline (arquitetura.html, escrito à mão)

As tabelas, tipos, chaves e relacionamentos saem do próprio SQL; só a posição de cada card é definida aqui.
Uso (na raiz do projeto):  python assets/fontes/gerar_diagramas.py
"""
import html as html_lib
import json
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).parent
RAIZ = AQUI.parent.parent
CHROME = next((c for c in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"] if Path(c).exists()), None)


def ler_sql(caminho):
    """Devolve {tabela: {"colunas": [(nome, tipo)], "pk": set, "fk": {coluna: tabela}}}."""
    sql = caminho.read_text(encoding="utf-8")
    tabelas = {}
    for m in re.finditer(r"CREATE TABLE IF NOT EXISTS `?(?:\w+`?\.`?)?(\w+)`?\s*\((.*?)\)\s*ENGINE", sql, re.S):
        nome, corpo = m.group(1), m.group(2)
        cols = []
        for linha in corpo.split("\n"):
            linha = linha.strip().strip(",")
            if not linha or re.match(r"(PRIMARY|INDEX|UNIQUE|CONSTRAINT|FOREIGN|KEY|REFERENCES|ON )", linha):
                continue
            partes = linha.split()
            tipo = partes[1]
            if tipo.upper().startswith("ENUM"):
                tipo = "ENUM"
            cols.append((partes[0].strip("`"), tipo.upper()))
        pk = set(re.findall(r"`?(\w+)`?", re.search(r"PRIMARY KEY \(([^)]*)\)", corpo).group(1))) if "PRIMARY KEY" in corpo else set()
        fk = {c: t for c, t in re.findall(r"FOREIGN KEY \(`?(\w+)`?\)\s*REFERENCES `?(?:\w+`?\.`?)?(\w+)`?", corpo)}
        tabelas[nome] = {"colunas": cols, "pk": pk, "fk": fk}
    return tabelas


def card(nome, t, x, y, w, cab, cab_txt, subtitulo="", grao=""):
    linhas = []
    for c, tipo in t["colunas"]:
        if c in t["pk"]:
            chave, classe = '<span class="ch pk">PK</span>', "col pk"
        elif c in t["fk"] or (c.startswith("sk_") and c not in t["pk"]):
            chave, classe = '<span class="ch fk">FK</span>', "col"
        else:
            chave, classe = '<span class="ch"></span>', "col"
        linhas.append(f'<div class="{classe}" data-c="{c}">{chave}<span class="nome">{c}</span><span class="tipo">{tipo}</span></div>')
    sub = f"<small>{subtitulo}</small>" if subtitulo else ""
    g = f'<div class="grao">{grao}</div>' if grao else ""
    return (f'<div class="tabela card" id="{nome}" style="left:{x}px;top:{y}px;width:{w}px;--cab:{cab};--cab-txt:{cab_txt}">'
            f'<h4>{nome}{sub}</h4>{g}{"".join(linhas)}</div>')


def pagina(titulo, rotulo, texto, legenda, cards, relacoes, largura, altura, extras=""):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{titulo}</title>
<link rel="stylesheet" href="diagramas.css"><style>body{{width:{largura}px}}#tela{{height:{altura}px}}</style></head><body>
<div class="topo"><span class="lbl">{rotulo}</span><h1>{titulo}</h1><p>{texto}</p><div class="legenda">{legenda}</div></div>
<div id="tela"><svg class="ligacoes"></svg>{"".join(cards)}{extras}</div>
<script src="ligacoes.js"></script><script>desenharLigacoes({json.dumps(relacoes, ensure_ascii=False)});marcarAltura();</script>
</body></html>"""


# ------------------------------------------------------------------ banco operacional (OLTP)
GRUPOS = {  # cor do cabeçalho por grupo do MER
    "Cadastros mestres": ("#EEF4FF", "#0F4FD1", ["estados", "lojas", "vendedores", "clientes", "categorias", "produtos"]),
    "Operações comerciais": ("#1A6BF5", "#FFFFFF", ["pedidos", "itens_pedido"]),
    "Operações logísticas": ("#5AB0FF", "#0B2E66", ["estoque", "movimentacao_estoque"]),
    "Gestão e apoio": ("#F1F2F4", "#111111", ["calendario", "metas", "campanhas", "eventos", "sazonalidade"]),
}
POS_OLTP = {  # x, y de cada card (largura 270)
    "estados": (110, 40), "lojas": (110, 230), "vendedores": (110, 450), "clientes": (110, 690), "metas": (110, 930),
    "pedidos": (470, 230), "itens_pedido": (470, 500), "estoque": (470, 800),
    "calendario": (830, 40), "produtos": (830, 390), "movimentacao_estoque": (830, 690),
    "categorias": (1190, 390),
    "campanhas": (1550, 40), "eventos": (1550, 450), "sazonalidade": (1550, 860),
}
LACOS = {("vendedores", "lojas"): {"lado": "esq", "folga": 40}, ("clientes", "lojas"): {"lado": "esq", "folga": 70},
         ("metas", "lojas"): {"lado": "esq", "folga": 100},
         ("movimentacao_estoque", "calendario"): {"lado": "dir", "folga": 60},
         ("itens_pedido", "pedidos"): {"lado": "esq", "folga": 34}, ("lojas", "estados"): {"lado": "esq", "folga": 40}}


def oltp():
    t = ler_sql(RAIZ / "sql" / "01_modelo_fisico_bd.sql")
    cor = {tab: (c, ct) for _, (c, ct, tabs) in GRUPOS.items() for tab in tabs}
    cards = [card(n, t[n], *POS_OLTP[n], 270, *cor[n]) for n in POS_OLTP]
    rel = []
    for n, d in t.items():
        for c, alvo in d["fk"].items():
            pk = next(iter(t[alvo]["pk"]))
            rel.append([n, c, alvo, pk, LACOS.get((n, alvo), {})])
    legenda = "".join(f'<span><i class="leg-cor" style="background:{c}"></i>{g}</span>' for g, (c, _, _) in GRUPOS.items())
    legenda += '<span><b class="ch pk" style="width:24px;font-size:10px;padding:1px 0;border-radius:5px;text-align:center">PK</b>chave primária</span>'
    legenda += '<span><b class="ch fk" style="width:24px;font-size:10px;padding:1px 0;border-radius:5px;text-align:center">FK</b>chave estrangeira · linha azul = relacionamento 1 : N</span>'
    return pagina("Banco operacional (OLTP) · amplo_varejo", "Modelo físico · MySQL",
                  f"{len(t)} tabelas em 4 grupos. O banco é abastecido só pelo simulador em Python, depois das validações de cobertura, "
                  "integridade e estoque. Campanhas, eventos e sazonalidade alimentam a simulação e não têm chave estrangeira.",
                  legenda, cards, rel, 1880, 1180)


# ------------------------------------------------------------------ Data Warehouse (estrela)
POS_DW = {
    "dim_calendario": (520, 30), "fato_vendas": (520, 450), "dim_status_pedido": (520, 960),
    "dim_cliente": (90, 450), "dim_vendedor": (90, 710),
    "dim_produto": (960, 450), "dim_loja": (960, 730),
    "fato_movimentacao_estoque": (1400, 450), "fato_metas": (1400, 760),
}
GRAO = {"fato_vendas": "Grão: 1 linha por item de pedido", "fato_movimentacao_estoque": "Grão: 1 linha por movimentação",
        "fato_metas": "Grão: 1 linha por loja × mês"}


def dw():
    t = ler_sql(RAIZ / "sql" / "02_star_schema.sql")
    cards = []
    for n, (x, y) in POS_DW.items():
        fato = n.startswith("fato")
        cards.append(card(n, t[n], x, y, 330 if fato else 300, "#1A6BF5" if fato else "#EEF4FF",
                          "#FFFFFF" if fato else "#0F4FD1", "FATO" if fato else "DIMENSÃO", GRAO.get(n, "")))
    rel = []
    for n, d in t.items():
        if not n.startswith("fato"):
            continue
        for c, _ in d["colunas"]:
            if c.startswith("sk_") and c not in d["pk"]:
                alvo = {"sk_calendario": "dim_calendario", "sk_cliente": "dim_cliente", "sk_vendedor": "dim_vendedor",
                        "sk_loja": "dim_loja", "sk_produto": "dim_produto", "sk_status": "dim_status_pedido"}[c]
                op = {"vertical": True} if (n, alvo) in {("fato_vendas", "dim_calendario"), ("fato_vendas", "dim_status_pedido")} else {}
                rel.append([n, c, alvo, c, op])
    nota = ('<div class="nota" style="left:1400px;top:1010px;width:330px"><b>fato_metas</b> não tem data: o mês é ligado ao '
            'calendário no DAX com <code>TREATAS</code>, sem relacionamento físico.</div>')
    legenda = ('<span><i class="leg-cor" style="background:#1A6BF5"></i>Fato (eventos medidos)</span>'
               '<span><i class="leg-cor" style="background:#EEF4FF"></i>Dimensão (contexto da análise)</span>'
               '<span>Linha azul = relacionamento 1 : N, da dimensão para o fato</span>')
    return pagina("Data Warehouse em estrela · amplo_varejo_dw", "Modelo dimensional · Star Schema",
                  "3 fatos e 6 dimensões. As dimensões são desnormalizadas (ex.: loja já traz estado e região), "
                  "o que deixa as medidas DAX simples e permite cruzar venda, meta e estoque pela mesma loja e produto.",
                  legenda, cards, rel, 1820, 1120, nota)


# ------------------------------------------------------------------ render
def chrome(*args):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", *args],
                          capture_output=True, text=True, encoding="utf-8", timeout=180)


def fotografar(html, png):
    dom = chrome("--window-size=1900,1200", "--dump-dom", html.resolve().as_uri()).stdout
    m = re.search(r'<pre id="posicoes"[^>]*>(.*?)</pre>', dom, re.S)
    tam = json.loads(html_lib.unescape(m.group(1)))
    chrome(f"--window-size={tam['largura']},{tam['altura']}", "--force-device-scale-factor=2",
           f"--screenshot={png.resolve()}", html.resolve().as_uri())
    print(f"{png.name}: {tam['largura']}×{tam['altura']} (2x)")


if __name__ == "__main__":
    if not CHROME:
        sys.exit("Chrome ou Edge não encontrado.")
    (AQUI / "mer_oltp.html").write_text(oltp(), encoding="utf-8")
    (AQUI / "modelo_dimensional.html").write_text(dw(), encoding="utf-8")
    for nome in ["mer_oltp", "modelo_dimensional", "arquitetura"]:
        fotografar(AQUI / f"{nome}.html", AQUI.parent / f"{nome}.png")
