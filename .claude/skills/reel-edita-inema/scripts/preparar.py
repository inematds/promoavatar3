#!/usr/bin/env python3
"""preparar.py — UMA chamada faz todo o preparo do reel e escreve o manifesto.

Por que existe (medido no A#19, 12 reels, 2026-08-03): o reel gastava 38
comandos de shell por video, e cada comando e uma ida ao modelo que rele o
contexto inteiro. So ffmpeg + ffprobe + whisper + gen-imagem eram ~14 dessas
chamadas, e nenhuma precisa de decisao do modelo no meio — sao mecanicas e
independentes. Aqui elas viram UMA.

O que faz, nesta ordem:
  1. cria o workspace (edicion/, motion/, motion/img/);
  2. le duracao/resolucao/fps das midias (ffprobe);
  3. extrai o audio do avatar e transcreve (transcribe-groq.sh), pulando se ja
     existir — retentativa nao paga de novo;
  4. roda detect-repeats.py sobre o transcript (informativo, nao derruba);
  5. GERA AS IMAGENS DA SECAO `## IMAGENS` do arquivo de texto do publico —
     uma por segmento, com --seed-key "<alvo>#<N>" e 1088x704 (a faixa do topo);
  6. escreve `manifesto.json` com tudo, para o agente NAO precisar sair
     procurando arquivo com ls/grep (isso era outro cluster grande de chamadas).

O passo 5 e o que fecha a Etapa 3: a fase de texto decide as imagens, e aqui
elas sao geradas MECANICAMENTE. Medido no A#19: o agente do reel ignorou a
secao `IMAGENS` e inventou os proprios prompts — instrucao nao e portao.

Uso:
  python3 preparar.py --avatar edicion/avatar.mp4 --ws ~/projetos/output/reels/x \\
      --alvo jovens --textos ~/projetos/promoavatar/textos/A19/jovens.md
  [--explicativo edicion/exp.mp4] [--sem-imagens] [--sem-transcricao]
"""
import argparse, json, os, re, subprocess, sys, shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LARGURA_TOPO, ALTURA_TOPO = 1088, 704   # faixa do topo e 1080x704 (stack-9x16.sh)


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def sonda(caminho: str) -> dict:
    """Duracao/resolucao/fps numa so chamada de ffprobe."""
    r = sh(["ffprobe", "-v", "error", "-of", "json",
            "-show_entries", "format=duration:stream=width,height,r_frame_rate,codec_type",
            caminho])
    if r.returncode != 0:
        return {"erro": r.stderr.strip()[:200]}
    d = json.loads(r.stdout or "{}")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    tem_audio = any(s.get("codec_type") == "audio" for s in d.get("streams", []))
    fps = v.get("r_frame_rate", "0/1")
    try:
        n, m = fps.split("/"); fps = round(int(n) / int(m), 2)
    except Exception:
        pass
    return {"duracao": round(float(d.get("format", {}).get("duration", 0)), 2),
            "largura": v.get("width"), "altura": v.get("height"),
            "fps": fps, "tem_audio": tem_audio}


def dimensoes_png(p) -> tuple:
    """Largura/altura lendo so o cabecalho IHDR — sem dependencia externa."""
    try:
        import struct
        with open(p, "rb") as f:
            return struct.unpack(">II", f.read(24)[16:24])
    except Exception:
        return (0, 0)


def _limpa(p: str) -> str:
    import unicodedata, re as _re
    p = unicodedata.normalize("NFD", str(p).lower())
    p = "".join(c for c in p if unicodedata.category(c) != "Mn")
    return _re.sub(r"[^a-z0-9]", "", p)


def tempos_dos_segmentos(transcript: dict, imagens: list) -> list:
    """Em que segundo a fala chega ao trecho citado por cada imagem.

    Isto NAO e trabalho de LLM. Medido em 2026-08-04, na mesma tarefa: um
    modelo local errou 0,24s em media (pior caso 0,92s, uma troca de imagem
    visivelmente fora da fala) e o Claude acertou na unha, gastando raciocinio
    para fazer busca de string. Aqui e exato, de graca e sempre igual.

    Casa o PREFIXO mais longo que existir: a citacao vem do .md e o transcript
    tokeniza diferente ("I.A." vs "IA"), entao exigir a frase inteira falha em
    ~3 de 8 casos. Sem casar, interpola entre os vizinhos e DIZ que interpolou.
    """
    ws = transcript.get("words") or [w for s in transcript.get("segments", [])
                                     for w in (s.get("words") or [])]
    palavras = [_limpa(w.get("word", "")) for w in ws]
    def achar(frase: str):
        alvo = [_limpa(p) for p in str(frase).split()]
        alvo = [p for p in alvo if p]
        for tam in range(len(alvo), 1, -1):
            pref = alvo[:tam]
            for i in range(len(palavras) - tam + 1):
                if palavras[i:i + tam] == pref:
                    return float(ws[i].get("start", 0)), ("transcrição"
                                                          if tam == len(alvo) else f"prefixo {tam}p")
        # Ultimo recurso antes de interpolar: a palavra mais DISTINTIVA da frase
        # (longa e que aparece uma vez so). Recua pela posicao dela na citacao,
        # ~0,3s por palavra, que e o ritmo tipico de fala. Cobre o caso em que o
        # transcript tokeniza diferente do .md ("I.A." vs "IA") e nem o prefixo
        # de duas palavras casa.
        for cand in sorted({p for p in alvo if len(p) >= 4}, key=len, reverse=True):
            if palavras.count(cand) == 1:
                i = palavras.index(cand)
                recuo = 0.3 * alvo.index(cand)
                return max(0.0, float(ws[i].get("start", 0)) - recuo), f"âncora \"{cand}\""
        return None, None

    achados = [achar(i.get("segmento", "")) for i in imagens]
    # O primeiro card entra no frame 0 — regra dura do cold-open.
    if achados:
        achados[0] = (0.0, achados[0][1] or "frame 0")
    # Interpola o que nao casou, e forca ordem crescente: imagem que "volta no
    # tempo" faria a timeline do montar.py sair embaralhada.
    ultimo = 0.0
    for k, (t, origem) in enumerate(achados):
        if t is None:
            prox = next((achados[j][0] for j in range(k + 1, len(achados))
                         if achados[j][0] is not None), None)
            t = round((ultimo + prox) / 2, 2) if prox is not None else ultimo + 2.0
            origem = "interpolado"
        t = max(t, ultimo + 0.05) if k else t
        achados[k] = (round(t, 2), origem)
        ultimo = achados[k][0]
    return achados


def ler_imagens(md: Path) -> list:
    """Le a secao `## IMAGENS` do arquivo do publico.

    Formato que a fase de texto escreve (regra 11b do fase1-texto.md):
        IMAGEM 3 — "primeiras palavras do segmento" [GATILHO]
        <prompt visual em ingles>
    """
    if not md or not md.exists():
        return []
    txt = md.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^##\s*IMAGENS\s*$(.*?)(?=^##\s|\Z)", txt, re.M | re.S)
    if not m:
        return []
    itens, atual = [], None
    for linha in m.group(1).splitlines():
        cab = re.match(r"^\s*IMAGEM\s+(\d+)\s*[—-]\s*(.*)$", linha)
        if cab:
            if atual and atual["prompt"]:
                itens.append(atual)
            rot = cab.group(2)
            seg = re.search(r'"([^"]*)"', rot)
            gat = re.search(r"\[([^\]]*)\]", rot)
            atual = {"n": int(cab.group(1)), "segmento": seg.group(1) if seg else "",
                     "gatilho": gat.group(1) if gat else "", "prompt": "",
                     "headline": "", "hook": ""}
        elif atual is not None:
            s = linha.strip()
            if s.lower().startswith("arquivo:"):          # imagem propria do usuario
                atual["arquivo"] = s.split(":", 1)[1].strip()
            elif s.lower().startswith("modo:"):           # contain (default) | cover
                atual["modo"] = s.split(":", 1)[1].strip()
            elif s.lower().startswith("headline:"):       # texto na tela do segmento
                atual["headline"] = s.split(":", 1)[1].strip()
            elif s.lower().startswith("hook:"):           # texto da faixa de base
                atual["hook"] = s.split(":", 1)[1].strip()
            elif s:
                atual["prompt"] = (atual["prompt"] + " " + s).strip()
    if atual and (atual["prompt"] or atual.get("arquivo")):
        itens.append(atual)
    return sorted(itens, key=lambda i: i["n"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--avatar", required=True)
    ap.add_argument("--ws", required=True, help="workspace do reel")
    ap.add_argument("--alvo", default="reel", help="publico — vira o seed-key")
    ap.add_argument("--textos", default=None, help="o .md do publico (secao IMAGENS)")
    ap.add_argument("--explicativo", default=None)
    ap.add_argument("--sem-imagens", action="store_true")
    ap.add_argument("--sem-transcricao", action="store_true")
    ap.add_argument("--flow", default=None,
                    help="flow.json do projeto — de onde saem o template do alvo e o padrao")
    ap.add_argument("--mapa", default=None,
                    help="templates/mapa.json — formato editorial -> layout")
    ap.add_argument("--template", default=None, help="override do operador")
    a = ap.parse_args()

    ws = Path(os.path.expanduser(a.ws))
    edicion, motion, imgdir = ws / "edicion", ws / "motion", ws / "motion" / "img"
    for d in (edicion, motion, imgdir):
        d.mkdir(parents=True, exist_ok=True)

    avatar = os.path.expanduser(a.avatar)
    if not os.path.exists(avatar):
        print(f"ERRO: avatar nao existe: {avatar}", file=sys.stderr)
        return 2

    # O Hyperframes exige asset DENTRO do projeto: caminho com `../` acima da
    # raiz e recusado pelo lint (invalid_parent_traversal_in_asset_path) e o
    # render sai mudo/sem imagem. Entao a midia e COPIADA para motion/ e o
    # manifesto guarda o caminho de la.
    def trazer(origem: str, nome: str) -> str:
        destino = motion / nome
        if not destino.exists() or os.path.getsize(destino) != os.path.getsize(origem):
            shutil.copy(origem, destino)
        return str(destino)

    man = {"workspace": str(ws), "alvo": a.alvo,
           "avatar": {"caminho": trazer(avatar, "avatar.mp4"),
                      "origem": avatar, **sonda(avatar)}}
    if a.explicativo:
        exp = os.path.expanduser(a.explicativo)
        if os.path.exists(exp):
            man["explicativo"] = {"caminho": trazer(exp, "explicativo.mp4"),
                                  "origem": exp, **sonda(exp)}
        else:
            man["explicativo"] = {"erro": f"nao existe: {exp}"}

    # ---- transcricao (pula se ja existe: retentativa nao repaga) ----
    transcript = edicion / "transcript.json"
    if a.sem_transcricao:
        man["transcript"] = {"pulado": True}
    elif transcript.exists() and transcript.stat().st_size > 0:
        man["transcript"] = {"caminho": str(transcript), "reaproveitado": True}
    else:
        audio = edicion / "audio.m4a"
        r = sh(["ffmpeg", "-y", "-loglevel", "error", "-i", avatar,
                "-vn", "-c:a", "aac", "-b:a", "128k", str(audio)])
        if r.returncode != 0:
            man["transcript"] = {"erro": r.stderr.strip()[:200]}
        else:
            tg = AQUI / "transcribe-groq.sh"
            r = sh(["bash", str(tg), str(audio), str(transcript)])
            man["transcript"] = ({"caminho": str(transcript)} if transcript.exists()
                                 else {"erro": (r.stderr or r.stdout).strip()[:300]})

    # ---- repeticoes (informativo) ----
    if transcript.exists():
        r = sh([sys.executable, str(AQUI / "detect-repeats.py"), str(transcript), "--json"])
        try:
            man["repeticoes"] = json.loads(r.stdout).get("total", 0)
        except Exception:
            man["repeticoes"] = None

    # ---- qual LAYOUT este publico usa, e POR QUE ----
    #
    # A escolha nao e do agente. Ela decorre, nesta ordem:
    #   1. --template            override do operador (teste)
    #   2. alvos.<alvo>.template voce cravou este publico  (regra "B")
    #   3. mapa[formato]         deriva do formato editorial que voce aprovou no
    #                            portao ("Formato escolhido:" do .md)  (regra "A")
    #   4. template da raiz      o padrao do pipeline
    # Guardamos TAMBEM qual regra venceu: sem isso ninguem consegue responder
    # depois "por que esse publico saiu nesse layout".
    formato = None
    if a.textos:
        md = Path(os.path.expanduser(a.textos))
        if md.exists():
            m = re.search(r"^\s*Formato escolhido:\s*(.+?)\s*$",
                          md.read_text(encoding="utf-8", errors="replace"), re.M)
            if m:
                formato = m.group(1).strip()
    man["formato"] = formato

    def ler_json(p):
        try:
            return json.loads(Path(os.path.expanduser(p)).read_text(encoding="utf-8"))
        except Exception:
            return {}

    flow = ler_json(a.flow) if a.flow else {}
    mapa = (ler_json(a.mapa) if a.mapa else {}).get("mapa", {})
    do_alvo = ((flow.get("alvos") or {}).get(a.alvo) or {}).get("template")
    escolha, origem = None, None
    if a.template:
        escolha, origem = a.template, "override (--template)"
    elif do_alvo:
        escolha, origem = do_alvo, f"campo `template` do alvo {a.alvo}"
    elif formato and mapa.get(formato):
        escolha, origem = mapa[formato], f"mapa: formato \"{formato}\""
    elif flow.get("template"):
        escolha, origem = flow["template"], "padrao do flow.json"
    man["template"] = escolha
    man["template_origem"] = origem
    # nome -> arquivo. Os templates moram no PROJETO: procuramos ao lado do
    # mapa.json e no `templates_dir` do flow.json, nunca no workspace.
    if escolha and not str(escolha).endswith(".json"):
        cands = []
        if a.mapa:
            cands.append(Path(os.path.expanduser(a.mapa)).parent / f"{escolha}.json")
        if a.flow:
            raiz = Path(os.path.expanduser(a.flow)).parent
            cands.append(raiz / (flow.get("templates_dir") or "templates") / f"{escolha}.json")
        achado = next((c for c in cands if c.exists()), None)
        man["template_arquivo"] = str(achado) if achado else None
        if not achado:
            man["template_aviso"] = (f"template '{escolha}' nao foi encontrado em "
                                     f"{[str(c) for c in cands]} — o montar.py vai falhar")
    else:
        man["template_arquivo"] = escolha
    if formato and not mapa.get(formato) and mapa and not do_alvo and not a.template:
        man["template_aviso"] = (f'formato "{formato}" nao esta no mapa — caiu no padrao. '
                                 f"Se ele merece layout proprio, acrescente ao mapa.json.")


    # Em que PROPORCAO gerar as imagens: quem manda e o template.
    # O `imagem-plena` usa a imagem em quadro inteiro (9:16); assumir a faixa
    # do topo (1088x704) esticava a imagem e deformava a cena — visto no
    # primeiro render de teste, e o lint nao pega isso.
    def _mult16(v: int) -> int:
        """O klein aceita 128-2048 em passos de 16."""
        return max(128, min(2048, int(round(v / 16)) * 16))
    img_w, img_h = LARGURA_TOPO, ALTURA_TOPO
    if man.get("template_arquivo"):
        _t = ler_json(man["template_arquivo"])
        _topo = (_t.get("faixas") or {}).get("topo") or {}
        # Sem `imagem` declarada, o tamanho SAI DA FAIXA — nao de um default
        # fixo. O diptico tem faixa de 960px e recebia imagem de 704: 256px
        # esticados em todo reel, e nenhum lint pega isso.
        img_w = _mult16((_t.get("canvas") or {}).get("largura", LARGURA_TOPO))
        img_h = _mult16(_topo.get("altura", ALTURA_TOPO))
        _i = _topo.get("imagem") or {}
        img_w = _mult16(_i.get("largura", img_w)); img_h = _mult16(_i.get("altura", img_h))
    man["imagem_tamanho"] = f"{img_w}x{img_h}"

    # ---- imagens da secao IMAGENS ----
    man["imagens"] = []
    if not a.sem_imagens:
        itens = ler_imagens(Path(os.path.expanduser(a.textos)) if a.textos else None)
        if not itens:
            man["imagens_aviso"] = ("nenhuma secao `## IMAGENS` encontrada — o texto "
                                    "do publico deveria traze-la (regra 11b)")
        for it in itens:
            destino = imgdir / f"topo-{it['n']:02d}.png"
            if it.get("arquivo"):                       # imagem propria do usuario
                origem = os.path.expanduser(it["arquivo"])
                if not os.path.exists(origem):
                    it.update(erro=f"arquivo nao existe: {origem}")
                    man["imagens"].append(it); continue
                # NUNCA corta imagem enviada. A gerada nasce no tamanho exato,
                # entao cortar nao tira nada; a enviada ja vem composta — se ela
                # traz texto ou um rosto enquadrado, cortar destroi o trabalho.
                # Entao: cabe INTEIRA (contain) e o resto e preenchido com uma
                # copia borrada dela mesma, que some no fundo escuro da marca.
                # `modo: cover` na linha do .md pede o comportamento oposto.
                modo = str(it.get("modo", "contain")).lower()
                if modo == "cover":
                    vf = (f"scale={img_w}:{img_h}:force_original_aspect_ratio=increase,"
                          f"crop={img_w}:{img_h}")
                else:
                    vf = (f"[0:v]scale={img_w}:{img_h}:force_original_aspect_ratio=increase,"
                          f"crop={img_w}:{img_h},gblur=sigma=32[bg];"
                          f"[0:v]scale={img_w}:{img_h}:force_original_aspect_ratio=decrease[fg];"
                          f"[bg][fg]overlay=(W-w)/2:(H-h)/2")
                flag = "-vf" if modo == "cover" else "-filter_complex"
                r = sh(["ffmpeg", "-y", "-loglevel", "error", "-i", origem,
                        flag, vf, str(destino)])
                if r.returncode == 0:
                    it.update(caminho=str(destino),
                              origem=f"arquivo-do-usuario ({modo}, ajustada para {img_w}x{img_h})")
                else:
                    it.update(erro=(r.stderr or "ffmpeg falhou").strip()[:200])
                man["imagens"].append(it); continue
            # Reaproveitar so vale se o tamanho BATE. Trocar de template muda a
            # proporcao pedida, e reusar a imagem antiga entregava 1088x704 onde
            # o quadro inteiro precisava de 1088x1920 — silenciosamente.
            if destino.exists() and destino.stat().st_size > 0 and \
                    dimensoes_png(destino) == (img_w, img_h):
                it.update(caminho=str(destino), origem="reaproveitada")
                man["imagens"].append(it); continue
            r = sh([sys.executable, str(AQUI / "gen-imagem.py"),
                    "--prompt", it["prompt"], "--out", str(destino),
                    "--seed-key", f"{a.alvo}#{it['n']}",
                    "--width", str(img_w), "--height", str(img_h)])
            it.update({"caminho": str(destino), "origem": "gerada"} if r.returncode == 0
                      else {"erro": (r.stderr or r.stdout).strip()[:200]})
            man["imagens"].append(it)

    # ---- tempos + esqueleto do segmentos.json ----
    #
    # Com headline vindo do dominio (regra 11b) e o tempo saindo do transcript,
    # o roteiro visual fica PRONTO aqui — o agente nao precisa inventar nada, e
    # por isso nao ha caminho alternativo para ele seguir. Era esse o buraco:
    # no A#22 o montar.py foi usado em 2 de 5 reels porque usa-lo era conselho.
    if man.get("imagens") and transcript.exists():
        try:
            tr = json.loads(transcript.read_text(encoding="utf-8"))
        except Exception:
            tr = {}
        tempos = tempos_dos_segmentos(tr, man["imagens"])
        segs, faltando = [], []
        for it, (t, origem) in zip(man["imagens"], tempos):
            it["inicio"] = t
            it["inicio_origem"] = origem
            if not it.get("headline"):
                faltando.append(it["n"])
            segs.append({"inicio": t,
                         "headline": it.get("headline", ""),
                         "hook": it.get("hook", "")})
        (ws / "segmentos.json").write_text(
            json.dumps(segs, ensure_ascii=False, indent=1), encoding="utf-8")
        man["segmentos"] = str(ws / "segmentos.json")
        if faltando:
            man["segmentos_aviso"] = (
                f"sem headline nas imagens {faltando} — a fase de texto deveria "
                f"escrever `headline:` em cada uma (regra 11b). Complete o "
                f"segmentos.json antes de montar.")

    (ws / "manifesto.json").write_text(json.dumps(man, ensure_ascii=False, indent=2),
                                       encoding="utf-8")

    # ---- resumo COMPACTO (isto entra no contexto do agente; nao floode) ----
    av = man["avatar"]
    print(f"workspace  {ws}")
    print(f"avatar     {av.get('duracao')}s {av.get('largura')}x{av.get('altura')} "
          f"{av.get('fps')}fps audio={av.get('tem_audio')}")
    if "explicativo" in man:
        e = man["explicativo"]
        print(f"explicativo{e.get('duracao')}s {e.get('largura')}x{e.get('altura')}")
    t = man.get("transcript", {})
    print(f"transcript {t.get('caminho') or t.get('erro') or 'pulado'}"
          f"{' (reaproveitado)' if t.get('reaproveitado') else ''}")
    if man.get("repeticoes") is not None:
        print(f"repeticoes {man['repeticoes']}"
              + ("  <- rode detect-repeats.py e corte antes de animar" if man["repeticoes"] else ""))
    ok = sum(1 for i in man["imagens"] if i.get("caminho"))
    ruim = [i for i in man["imagens"] if i.get("erro")]
    print(f"imagens    {ok}/{len(man['imagens'])} em {imgdir}")
    for i in ruim:
        print(f"  ERRO imagem {i['n']}: {i['erro']}")
    if man.get("imagens_aviso"):
        print(f"  AVISO: {man['imagens_aviso']}")
    if man.get("segmentos"):
        origens = {i.get("inicio_origem") for i in man["imagens"]}
        print(f"segmentos  {len(man['imagens'])} · tempos: {', '.join(sorted(o for o in origens if o))}")
        print(f"           {man['segmentos']}")
    if man.get("segmentos_aviso"):
        print(f"  AVISO: {man['segmentos_aviso']}")
    if man.get("template"):
        print(f"template   {man['template']}   <- {man['template_origem']}")
    if man.get("template_aviso"):
        print(f"  AVISO: {man['template_aviso']}")
    print(f"manifesto  {ws/'manifesto.json'}")
    return 1 if ruim else 0


if __name__ == "__main__":
    sys.exit(main())
