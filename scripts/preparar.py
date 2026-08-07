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
     procurando arquivo com ls/grep (isso era outro cluster grande de chamadas);
  7. CHAMA o montar.py e entrega `motion/index.html` pronto. `--flow`/`--mapa`
     tem default no proprio repo deste script, entao o template e resolvido
     mesmo que ninguem passe nada. Sem isso restava um caminho alternativo
     (escrever HTML a mao) e o agente pegava esse caminho em 3 de 5 reels.

O passo 5 e o que fecha a Etapa 3: a fase de texto decide as imagens, e aqui
elas sao geradas MECANICAMENTE. Medido no A#19: o agente do reel ignorou a
secao `IMAGENS` e inventou os proprios prompts — instrucao nao e portao.

Uso:
  python3 preparar.py --avatar edicion/avatar.mp4 --ws ~/projetos/output/reels/x \\
      --alvo jovens --textos ~/projetos/promoavatar/textos/A19/jovens.md
  [--explicativo edicion/exp.mp4] [--sem-imagens] [--sem-transcricao]
  [--sem-montar] [--flow ... --mapa ... --template ...  (so para override)]
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


MIN_CARD = 1.5   # segundos que um card do topo precisa ficar no ar


def tempos_dos_segmentos(transcript: dict, imagens: list,
                         duracao: float = 0.0) -> list:
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
        # Separacao MINIMA de verdade, nao 0,05s.
        #
        # O piso antigo existia so para forcar ordem crescente, e produzia
        # cards de 50 ms: no A#25/pessoa-comum as imagens 7 e 8 sairam em
        # 33,78s e 33,83s, e o `qc-frames.py` reprovou o reel — corretamente,
        # porque duas imagens a 50 ms uma da outra nao sao uma troca, sao um
        # piscar. Um card precisa ficar no ar tempo de ser visto.
        if k:
            t = max(t, ultimo + MIN_CARD)
        achados[k] = (round(t, 2), origem)
        ultimo = achados[k][0]

    # Empurrar em cascata pode jogar o ultimo card para fora do video. Se isso
    # acontecer, comprime de tras para frente respeitando o MIN_CARD — assim o
    # fim continua dentro do quadro e a ordem se mantem. O primeiro card fica
    # cravado em 0 (regra do cold-open), entao a compressao para nele.
    limite = (duracao - MIN_CARD) if duracao else None
    if limite and achados and achados[-1][0] > limite:
        for k in range(len(achados) - 1, 0, -1):
            t, origem = achados[k]
            teto = limite - MIN_CARD * (len(achados) - 1 - k)
            if t > teto:
                achados[k] = (round(max(0.0, teto), 2), f"{origem} (comprimido)")
    return achados


def ler_json_seguro(p) -> dict:
    """JSON de um caminho que pode nao existir — devolve {} em vez de explodir."""
    try:
        return json.loads(Path(os.path.expanduser(p)).read_text(encoding="utf-8"))
    except Exception:
        return {}


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
                    help="flow.json do projeto — de onde saem o template do alvo e o padrao. "
                         "Omitido: usa o do repo deste script, se existir.")
    ap.add_argument("--mapa", default=None,
                    help="templates/mapa.json — formato editorial -> layout. "
                         "Omitido: usa o do repo deste script, se existir.")
    ap.add_argument("--template", default=None, help="override do operador")
    ap.add_argument("--sem-montar", action="store_true",
                    help="para no manifesto, sem gerar o index.html")
    a = ap.parse_args()

    # `--flow`/`--mapa` eram opcionais e o flow.json PEDIA que o agente os
    # passasse — no A#22 nenhum dos 5 reels passou, e sem eles o template nao e
    # resolvido e o agente volta a escolher (ou a escrever HTML na mao). Pedir
    # nao e portao: o caminho dos dois sai do proprio __file__.
    REPO = AQUI.parent
    if not a.flow and (REPO / "flow.json").exists():
        a.flow = str(REPO / "flow.json")
    if not a.mapa:
        _dir = (ler_json_seguro(a.flow).get("templates_dir") or "templates") if a.flow else "templates"
        if (REPO / _dir / "mapa.json").exists():
            a.mapa = str(REPO / _dir / "mapa.json")

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

    ler_json = ler_json_seguro
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
        # Fallback para o repo do MOTOR: um dominio que usa os scripts daqui
        # (`motor_repo` no flow.json dele) herda os layouts sem manter copia.
        # O do dominio VENCE — quem quiser layout proprio e so criar o arquivo.
        cands.append(REPO / (flow.get("templates_dir") or "templates") / f"{escolha}.json")
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
        tempos = tempos_dos_segmentos(tr, man["imagens"],
                                      man["avatar"].get("duracao") or 0.0)
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

    # O manifesto e escrito ANTES de montar porque o montar.py o le do disco —
    # ele e reescrito logo abaixo com o resultado do HTML.
    def grava_manifesto():
        (ws / "manifesto.json").write_text(json.dumps(man, ensure_ascii=False, indent=2),
                                           encoding="utf-8")
    grava_manifesto()

    # ---- monta o index.html na mesma chamada ----
    #
    # Usar o montar.py era CONSELHO no `entrega` do flow.json, e conselho perde:
    # no A#22 ele foi usado em 2 de 5 reels — nos outros 3 o agente escreveu o
    # HTML a mao, que e de onde vinham o loop de lint e o `top:1372px-1312px`.
    # Aqui nao ha mais caminho alternativo: quem prepara, monta.
    if a.sem_montar:
        man["html"] = {"pulado": True}
    elif not man.get("segmentos"):
        man["html"] = {"erro": "sem segmentos.json (faltou transcript ou secao IMAGENS)"}
    elif not any((i.get("headline") or "").strip() for i in man.get("imagens", [])):
        # Visto no primeiro teste do encadeamento: com um .md antigo (sem as
        # linhas `headline:` da 11b) o montar.py gerava um index.html com TODAS
        # as manchetes vazias e o preparar.py saia 0. Reel mudo de texto passando
        # por pronto e pior do que falhar aqui.
        man["html"] = {"erro": "nenhuma imagem tem `headline:` — o texto do publico "
                               "e antigo (regra 11b). Complete o segmentos.json e rode "
                               "o montar.py, ou refaca a fase de texto."}
    elif not man.get("template_arquivo"):
        man["html"] = {"erro": f"template nao resolvido: {man.get('template_aviso') or 'sem flow.json/mapa.json'}"}
    else:
        saida = motion / "index.html"
        r = sh([sys.executable, str(AQUI / "montar.py"),
                "--manifesto", str(ws / "manifesto.json"),
                "--segmentos", man["segmentos"], "--out", str(saida)])
        man["html"] = ({"caminho": str(saida)} if r.returncode == 0
                       else {"erro": (r.stderr or r.stdout).strip()[:300]})

    grava_manifesto()

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
    h = man.get("html") or {}
    if h.get("caminho"):
        print(f"html       {h['caminho']}")
    elif h.get("pulado"):
        print("html       pulado (--sem-montar)")
    else:
        print(f"  ERRO html: {h.get('erro')}")
    print(f"manifesto  {ws/'manifesto.json'}")
    # Falha alto se o HTML nao saiu: e o produto da chamada. Sair 0 com o
    # index.html faltando e o convite para o agente escrever um a mao.
    if h.get("erro"):
        return 3
    return 1 if ruim else 0


if __name__ == "__main__":
    sys.exit(main())
