#!/usr/bin/env python3
"""montar.py — template + conteudo -> index.html do Hyperframes.

Por que existe (medido no A#19, 12 reels): o agente escrevia o HTML a mao toda
vez. Isso custava ~14 chamadas por reel so de `lint -> corrige -> lint` e
render repetido (4,2 lint + 2,7 lint-timeline + 2,8 render por reel), e ainda
assim saia com erro — o reel a16-criadores tinha `top:1372px-1312px` no CSS,
que nao e CSS valido.

Aqui o HTML e GERADO. Template versionado nao tem erro de sintaxe para corrigir,
entao o loop some do contexto e o determinismo deixa de depender da disciplina
do agente: mesmo template + mesmo conteudo = mesmo HTML, byte a byte.

DIVISAO DE RESPONSABILIDADE (decidida em 2026-08-03):
  - o TEMPLATE (layout, faixas, cores, o que entra em cada banda) mora no
    PROJETO (ex.: promoavatar/templates/*.json) — e decisao editorial, e
    versionada em git, e vira snapshot por fluxo, e e revisavel no portao;
  - o MOTOR (este arquivo) mora na SKILL — e mecanica, e compartilhada, e nao
    deve ser duplicada em cada projeto.

FALHA ALTO de proposito: template inexistente ou conteudo incompleto sai com
exit != 0 e mensagem. O modo antigo era o agente improvisar um HTML quando algo
faltava, e improviso passa despercebido.

Uso:
  python3 montar.py --template <projeto>/templates/empilhado-capa.json \\
    --manifesto <ws>/manifesto.json --segmentos <ws>/segmentos.json \\
    --out <ws>/motion/index.html

`segmentos.json` = [{"inicio":0.0,"headline":"PARE DE PAGAR|FERRAMENTA CARA",
                     "hook":"5 apps. {1 video.} Ainda assim?"}, ...]
  - `|` na headline quebra a linha; o TRECHO APOS o `|` sai no acento.
  - `{...}` no hook marca a palavra-chave (sai no acento).
  - um segmento por imagem do manifesto, na ordem.
"""
import argparse, html, json, os, shutil, sys
from pathlib import Path


def erro(msg: str, code: int = 2):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(code)


def carregar(p: str, oque: str) -> dict:
    caminho = Path(os.path.expanduser(p))
    if not caminho.exists():
        erro(f"{oque} nao existe: {caminho}. Nao invente um: corrija o caminho "
             f"ou reporte — improvisar aqui foi o que a versao anterior fazia.")
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except Exception as e:
        erro(f"{oque} invalido ({caminho}): {e}")


def esc(s) -> str:
    return html.escape(str(s or ""), quote=False)


def headline_html(txt: str, maiusculas: bool) -> str:
    partes = [p.strip() for p in str(txt or "").split("|")]
    if maiusculas:
        partes = [p.upper() for p in partes]
    if len(partes) == 1:
        return esc(partes[0])
    corpo = "<br>".join(esc(p) for p in partes[:-1])
    return f'{corpo}<br><span class="em">{esc(partes[-1])}</span>'


def hook_html(txt: str) -> str:
    """`{palavra}` vira acento."""
    out, resto = "", str(txt or "")
    while "{" in resto and "}" in resto:
        a, _, r1 = resto.partition("{")
        kw, _, resto = r1.partition("}")
        out += esc(a) + f'<span class="kw">{esc(kw)}</span>'
    return out + esc(resto)


ALTURA_BASE_PADRAO = 608

def topo_do_hook(hk: dict) -> int:
    """Onde o texto da base COMECA, em px a partir do topo da faixa.

    Era centralizado na vertical (`top:50%`), e no reel pronto isso deixava a
    frase solta no meio de 608px, longe do avatar. O dono pediu "quase no topo
    do quadro inferior, com respiro de 2 linhas" — entao o respiro e medido em
    LINHAS do proprio texto, nao em pixels soltos: mudar o corpo da letra move o
    texto junto, sem ninguem ter que recalcular margem.

    Teto na metade da faixa: um `respiro_linhas` grande demais empurraria a
    frase para fora do quadro sem erro nenhum — so um reel com a base vazia.
    """
    tamanho = hk.get("tamanho", 56)
    entrelinha = hk.get("entrelinha", 1.16)
    linhas = hk.get("respiro_linhas", 2)
    return min(round(linhas * tamanho * entrelinha), ALTURA_BASE_PADRAO // 2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default=None,
                    help="opcional: se omitido, usa o que o preparar.py resolveu "
                         "e gravou no manifesto (campo `template`)")
    ap.add_argument("--manifesto", required=True)
    ap.add_argument("--segmentos", required=True)
    ap.add_argument("--legendas", default=None,
                    help="opcional: legendas.json (legendas.py). Sem ele, reel "
                         "sem legenda — ver docs/legenda.md")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    man = carregar(a.manifesto, "manifesto")
    # Quem escolhe o layout e o preparar.py (override > campo do alvo > mapa
    # por formato editorial > padrao), e ele grava a escolha E a regra que
    # venceu no manifesto. Aqui so obedecemos — e falhamos alto se ninguem
    # resolveu, em vez de eleger um por conta propria.
    escolhido = a.template or man.get("template")
    if not escolhido:
        erro("nenhum template resolvido: passe --template ou rode o preparar.py "
             "com --flow/--mapa para que ele grave a escolha no manifesto")
    if not str(escolhido).endswith(".json"):
        # o preparar.py grava tambem o caminho resolvido; o nome sozinho
        # nao diz onde o template mora (ele fica no PROJETO, nao no workspace)
        arq = man.get("template_arquivo")
        if not arq:
            erro(f"template '{escolhido}' veio como nome, sem caminho. Rode o "
                 f"preparar.py com --mapa/--flow (ele resolve o arquivo) ou passe "
                 f"--template com o caminho do .json.")
        escolhido = arq
    tpl = carregar(escolhido, "template")
    segs = carregar(a.segmentos, "segmentos")
    if not isinstance(segs, list) or not segs:
        erro("segmentos.json precisa ser uma lista nao vazia")

    cv = tpl.get("canvas", {})
    W, H = cv.get("largura", 1080), cv.get("altura", 1920)
    cor = tpl.get("cores", {})
    fx = tpl.get("faixas", {})
    topo, meio, base = fx.get("topo", {}), fx.get("meio", {}), fx.get("base", {})
    tr = tpl.get("transicao", {})

    dur = float((man.get("avatar") or {}).get("duracao") or 0)
    if dur <= 0:
        erro("manifesto sem duracao do avatar — rode preparar.py antes")
    avatar = (man.get("avatar") or {}).get("caminho")
    imgs = [i for i in man.get("imagens", []) if i.get("caminho")]
    if not imgs:
        erro("manifesto sem imagens. A secao `## IMAGENS` do texto do publico e "
             "quem as define (regra 11b) — nao gere prompts seus.")
    if len(segs) > len(imgs):
        erro(f"{len(segs)} segmentos para {len(imgs)} imagens — cada segmento "
             f"precisa da sua imagem")

    saida = Path(os.path.expanduser(a.out))
    saida.parent.mkdir(parents=True, exist_ok=True)

    def rel(p):
        """Caminho root-relativo, e RECUSA sair da raiz do projeto.

        O lint do Hyperframes rejeita `../` acima da raiz
        (`invalid_parent_traversal_in_asset_path`) e o render sai mudo ou sem
        imagem. Custou uma rodada para descobrir: `preparar.py` copia a midia
        para dentro de `motion/` justamente para isto valer.
        """
        r = os.path.relpath(os.path.expanduser(p), saida.parent)
        if r.startswith(".."):
            erro(f"asset fora da raiz da composicao: {p}\n"
                 f"       O Hyperframes so aceita caminho root-relativo. Rode "
                 f"preparar.py (ele copia a midia para motion/) em vez de "
                 f"apontar para o arquivo original.")
        return r

    hl, hk = topo.get("headline", {}), base.get("hook", {})
    # Faixa de base e OPCIONAL: `diptico` e `imagem-plena` nao tem terceira
    # faixa. Nesses, o vazio de 608px que a base costumava deixar some por
    # ESTRUTURA, e nao por regra de redacao.
    tem_base = "base" in fx
    base_video = tem_base and base.get("fonte") == "explicativo"
    base_texto = tem_base and not base_video
    # O avatar pode ser uma FAIXA ou um recorte flutuante (PiP) sobre a imagem.
    pip = meio.get("pip", {}) if meio.get("forma") == "pip" else None
    exp = (man.get("explicativo") or {}).get("caminho")
    if base_video and not exp:
        erro(f"o template '{tpl.get('nome')}' pede video explicativo na base, e o "
             f"manifesto nao tem um. Use outro template ou passe --explicativo "
             f"ao preparar.py.")

    # ---------- corpo ----------
    cards = "\n".join(
        f'        <img id="c{n}" class="card" src="{esc(rel(i["caminho"]))}" data-track-index="1" />'
        for n, i in enumerate(imgs[:len(segs)], 1))
    heads = "\n".join(
        f'        <div class="headline" id="h{n}">{headline_html(s.get("headline"), hl.get("maiusculas", True))}</div>'
        for n, s in enumerate(segs, 1))
    if base_video:
        corpo_base = (f'        <video id="expvid" class="clip" src="{esc(rel(exp))}" muted playsinline loop\n'
                      f'               data-start="0" data-duration="{dur}" data-track-index="1"></video>')
    elif base_texto:
        corpo_base = "\n".join(
            f'        <div class="hook" id="b{n}">{hook_html(s.get("hook"))}</div>'
            for n, s in enumerate(segs, 1))
    else:
        corpo_base = None

    if pip:
        # Avatar flutuando sobre a imagem: precisa de recorte, borda e sombra,
        # senao "cola" no fundo e some. z-index acima da headline e proposital.
        css_meio = f"""
      #meio{{position:absolute;
        {f"top:{pip.get('topo',120)}px" if pip.get('ancora_v','rodape')=='topo' else f"bottom:{pip.get('rodape',120)}px"};
        {f"right:{pip.get('direita',56)}px" if pip.get('ancora_h','esquerda')=='direita' else f"left:{pip.get('esquerda',56)}px"};
        width:{pip.get('largura',468)}px;
        height:{pip.get('altura',264)}px;overflow:hidden;z-index:4;
        border-radius:{pip.get('raio',28)}px;
        border:{pip.get('borda',3)}px solid rgba(255,255,255,.16);
        box-shadow:0 18px 48px rgba(0,0,0,.55)}}
      #meio video{{width:100%;height:100%;object-fit:cover}}
"""
    else:
        css_meio = f"""
      #meio{{position:absolute;top:{meio.get('y',704)}px;left:0;width:{W}px;
        height:{meio.get('altura',608)}px;overflow:hidden}}
      #meio video{{width:100%;height:100%;object-fit:cover}}
      #meio .edge{{position:absolute;inset:0;z-index:2;pointer-events:none;
        box-shadow:inset 0 8px 18px rgba(0,0,0,.35),inset 0 -8px 18px rgba(0,0,0,.35)}}
"""
    # ---------- legenda ----------
    # Uma palavra por vez, ancorada na BASE da faixa do avatar (o terco
    # inferior do quadro e o painel `#base`, nao sobra para legenda).
    # Cada palavra e um elemento proprio que acende e apaga: um elemento so,
    # trocando de texto por `tl.call`, nao sobrevive ao render por seek do
    # Hyperframes.
    lg = meio.get("legenda", {})
    legs = carregar(a.legendas, "legendas") if a.legendas else []
    if legs and not isinstance(legs, list):
        erro("legendas.json precisa ser uma lista — rode scripts/legendas.py")
    if legs and pip:
        # No PiP o avatar e um selo de 468x264 sobre a imagem; legenda ali
        # sairia ilegivel e taparia o proprio rosto.
        print("aviso: template com avatar em PiP — legenda ignorada")
        legs = []

    # A fonte da legenda precisa viajar junto: o renderer so resolve sozinho um
    # punhado de familias, e as demais caem calado numa generica
    # (`font_family_without_font_face` no lint). Copiar para dentro de motion/ e
    # declarar @font-face e o que faz o render sair com a tipografia aprovada.
    face_legenda = ""
    if legs and lg.get("fonte_arquivo"):
        orig = Path(os.path.expanduser(lg["fonte_arquivo"]))
        if not orig.exists():
            erro(f"fonte da legenda nao encontrada: {orig}\n"
                 f"       Ajuste `faixas.meio.legenda.fonte_arquivo` no template.")
        destino = saida.parent / "fonts" / orig.name
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(orig, destino)
        familia = lg.get("fonte", "").split(",")[0].strip()
        face_legenda = (f"""
      @font-face{{font-family:'{familia}';src:url('{esc(rel(destino))}');
        font-weight:{lg.get('peso',900)};font-style:normal}}
""")

    css_legenda = "" if not legs else face_legenda + f"""
      #captions{{position:absolute;left:0;right:0;bottom:{lg.get('respiro',28)}px;
        z-index:5;pointer-events:none;text-align:center}}
      #captions .w{{position:absolute;left:24px;right:24px;bottom:0;opacity:0;
        font-family:{lg.get('fonte','Inter,system-ui,sans-serif')};
        font-size:{lg.get('tamanho',86)}px;font-weight:{lg.get('peso',900)};
        line-height:1;color:var(--txt);
        -webkit-text-stroke:{lg.get('contorno_px',8)}px {lg.get('contorno','#000')};
        paint-order:stroke fill}}
      #captions .w.kw{{color:var(--ac)}}
"""
    corpo_legenda = "" if not legs else "\n" + "\n".join(
        f'        <div class="w{" kw" if p.get("kw") else ""}" id="cb{n}">{esc(p.get("palavra",""))}</div>'
        for n, p in enumerate(legs, 1))

    css_base = "" if not tem_base else f"""
      #base{{position:absolute;top:{base.get('y',1312)}px;left:0;width:{W}px;
        height:{base.get('altura',608)}px;overflow:hidden;background:{cor.get('base_fundo','#05070a')};
        display:flex;align-items:center;justify-content:center}}
      #base video{{width:100%;height:100%;object-fit:cover}}
      #base .hook{{position:absolute;left:{hk.get('margem_lateral',56)}px;
        right:{hk.get('margem_lateral',56)}px;top:{topo_do_hook(hk)}px;opacity:0;
        font-size:{hk.get('tamanho',56)}px;font-weight:{hk.get('peso',800)};
        line-height:{hk.get('entrelinha',1.16)};color:var(--txt);text-align:center}}
      #base .hook .kw{{color:var(--ac)}}
"""

    css = f"""
      *{{margin:0;padding:0;box-sizing:border-box}}
      html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{cor.get('fundo','#000')};
        font-family:Inter,system-ui,sans-serif}}
      :root{{--txt:{cor.get('texto','#fff')};--ac:{cor.get('acento','#F5A623')}}}
      #root{{position:relative;width:{W}px;height:{H}px}}
      #topo{{position:absolute;top:{topo.get('y',0)}px;left:0;width:{W}px;height:{topo.get('altura',704)}px;
        overflow:hidden;background:{cor.get('fundo','#000')}}}
      #topo .card{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;
        filter:brightness({topo.get('escurecer',0.62)}) saturate(1.15)}}
      #topo .shade{{position:absolute;inset:0;z-index:2;pointer-events:none;
        background:linear-gradient(180deg,rgba(0,0,0,.15) 0%,rgba(0,0,0,.72) 100%)}}
      #topo .headline{{position:absolute;left:{hl.get('margem_lateral',48)}px;
        right:{hl.get('margem_lateral',48)}px;
        {f"top:{hl.get('topo_em',280)}px" if hl.get('ancora')=='topo' else f"bottom:{hl.get('base_em',56)}px"};
        z-index:3;opacity:0;
        font-size:{hl.get('tamanho',76)}px;font-weight:{hl.get('peso',900)};
        line-height:{hl.get('entrelinha',1.04)};color:var(--txt);
        text-shadow:0 4px 24px rgba(0,0,0,.65)}}
      #topo .headline .em{{color:var(--ac)}}
{css_meio}{css_legenda}{css_base}
      #flash{{position:absolute;inset:0;background:#fff;opacity:0;z-index:20;pointer-events:none}}
"""

    bloco_base = ("" if corpo_base is None
                  else f'      <div id="base">\n{corpo_base}\n      </div>')

    # ---------- timeline ----------
    tl, D = [], float(tr.get("duracao", 0.42))
    tl.append('      tl.set("#c1",{opacity:1},0); tl.set("#h1",{opacity:1},0);')
    if base_texto:
        tl.append('      tl.set("#b1",{opacity:1},0);')
    tl.append(f'      tl.fromTo("#c1",{{scale:1.06}},{{scale:1,duration:0.6,ease:"power2.out"}},0);')
    for n, s in enumerate(segs[1:], start=2):
        t = float(s.get("inicio", 0))
        if tr.get("flash"):
            tl.append(f'      tl.set("#flash",{{opacity:0.9}},{t-0.03:.2f});')
            tl.append(f'      tl.to("#flash",{{opacity:0,duration:0.14,ease:"power2.out"}},{t:.2f});')
        tl.append(f'      tl.to("#c{n-1}",{{opacity:0,duration:0.22,ease:"power2.in"}},{t-0.05:.2f});')
        tl.append(f'      tl.fromTo("#c{n}",{{opacity:0,scale:{tr.get("escala_entrada",1.08)}}},'
                  f'{{opacity:1,scale:1,duration:{D},ease:"power3.out"}},{t:.2f});')
        tl.append(f'      tl.to("#h{n-1}",{{opacity:0,y:-16,duration:0.22,ease:"power2.in"}},{t-0.08:.2f});')
        tl.append(f'      tl.fromTo("#h{n}",{{opacity:0,y:18}},'
                  f'{{opacity:1,y:0,duration:0.40,ease:"back.out(1.6)"}},{t+0.26:.2f});')
        if base_texto:
            tl.append(f'      tl.to("#b{n-1}",{{opacity:0,y:-10,duration:0.22,ease:"power2.in"}},{t-0.08:.2f});')
            tl.append(f'      tl.fromTo("#b{n}",{{opacity:0,y:14}},'
                      f'{{opacity:1,y:0,duration:{D},ease:"power2.out"}},{t+0.25:.2f});')
    # legenda: acende no `start` da palavra, apaga quando a proxima comeca.
    # `set` (e nao `to`) de proposito: sem fade, a troca e seca e o render por
    # seek acerta o quadro exato.
    for n, p in enumerate(legs, 1):
        ini = float(p.get("start", 0))
        fim = ini + float(p.get("dur", 0))
        tl.append(f'      tl.set("#cb{n}",{{opacity:1}},{ini:.3f});')
        tl.append(f'      tl.set("#cb{n}",{{opacity:0}},{fim:.3f});')

    # pulsos: nenhum beat acima do teto (regra dos <=4s), calculado, nao chutado
    teto = float(tr.get("pulso_max_s", 3.6))
    marcos = [float(s.get("inicio", 0)) for s in segs] + [dur]
    for n in range(1, len(segs) + 1):
        ini, fim = marcos[n - 1], marcos[n]
        t = ini + teto
        while t < fim - 0.3:
            tl.append(f'      tl.fromTo("#c{n}",{{filter:"brightness({topo.get("escurecer",0.62)}) saturate(1.15)"}},'
                      f'{{filter:"brightness({round(topo.get("escurecer",0.62)+0.08,2)}) saturate(1.25)",'
                      f'duration:0.5,yoyo:true,repeat:1,ease:"sine.inOut"}},{t:.2f});')
            t += teto

    doc = f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <!-- GERADO por montar.py a partir de {esc(tpl.get('nome'))} — nao edite a mao:
         mexa no template (projeto) ou nos segmentos, e gere de novo. -->
    <style>{css}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}"
         data-width="{W}" data-height="{H}">
      <div id="topo">
{cards}
        <div class="shade"></div>
{heads}
      </div>
      <div id="meio">
        <video id="avatarvid" class="clip" src="{esc(rel(avatar))}" muted playsinline
               data-start="0" data-duration="{dur}" data-track-index="0"></video>
{'' if pip else '        <div class="edge"></div>'}
{'' if not legs else f'        <div id="captions">{corpo_legenda}{chr(10)}        </div>'}
      </div>
      <audio id="avataraudio" src="{esc(rel(avatar))}" data-start="0" data-duration="{dur}"
             data-track-index="2" data-volume="1"></audio>
{bloco_base}
      <div id="flash"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused:true}});
{chr(10).join(tl)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    saida.write_text(doc, encoding="utf-8")
    forma = ("base=video" if base_video else "base=texto" if base_texto else "sem base")
    print(f"template   {tpl.get('nome')}  ({forma}, avatar={'PiP' if pip else 'faixa'})")
    print(f"segmentos  {len(segs)} · imagens {len(imgs)} · duracao {dur}s")
    print(f"beats      maior lacuna <= {teto}s (pulsos inseridos automaticamente)")
    print(f"html       {saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
