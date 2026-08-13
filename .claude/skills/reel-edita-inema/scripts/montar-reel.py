#!/usr/bin/env python3
"""montar-reel.py — do avatar ao MP4 entregavel, numa chamada.

Fecha a fase `reel`. Depois das decisoes de 2026-08-04 (SFX fora, legenda SEM,
revisor virou script — `docs/decisoes-reel.md`) a sequencia nao tem mais
ramificacao: preparar -> portao 1 -> render -> revisor -> CTA -> QC. Isto e um
encadeamento, e encadeamento e trabalho de script.

Por que existe: levantados 7 workspaces do A#22, sairam 7 estruturas
DIFERENTES — a mesma coisa com tres nomes (`reel-body` / `corpo-final` /
`render-high`), listas de concat escritas a mao, e 3 reels que nao chegaram a um
MP4 de corpo. Nada no conteudo daqueles publicos justificava sete caminhos: era
improviso. Aqui os nomes sao FIXOS:

  <ws>/motion/index.html   composicao
  <ws>/motion/corpo.mp4    render sem CTA (e o que o revisor analisa)
  <ws>/final/reel.mp4      ENTREGAVEL (corpo + CTA)
  <ws>/qc/mosaico.png      o que o olho humano ve — uma imagem

O revisor roda no CORPO, nao no final: o CTA tem audio proprio e 3s sem fala,
que o `verify-cut.py` leria como silencio longo. O QC visual roda no FINAL,
justamente para confirmar que o CTA entrou.

O que sobra para o modelo depois disto: olhar o mosaico (a imagem 1 provoca? a
headline le de relance? o fecho tem o CTA?) e reagir a exit != 0. Mais nada.

Uso:
  python3 montar-reel.py --avatar <mp4> --ws <workspace> --alvo <publico> \\
      --textos <repo>/textos/<REF>/<publico>.md
  [--qualidade high|standard|draft] [--sem-cta] [--cta <mp4>] [--pular-preparo]

Exit 0 = entregavel pronto · 3 = algum portao reprovou · 2 = erro de arquivo.
"""
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parent


def sh(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def erro(msg: str, code: int = 2):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(code)


def passo(n: str):
    print(f"\n=== {n}", flush=True)


def duracao(v: str) -> float:
    r = sh(["ffprobe", "-v", "error", "-of", "json",
            "-show_entries", "format=duration", v])
    try:
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        return 0.0


def _hyperframes_do_cache():
    """O binario mais NOVO que ja esta no cache do npx. None se nao houver.

    Por que isto existe (2026-08-05, A#25): `npx --no-install hyperframes`
    resolve sempre a versao LATEST do registry. Quando o upstream publicou a
    0.7.94, o cache tinha ate 0.7.92 — e o `--no-install` recusou, certissimo,
    porque a regra desta maquina e nao baixar nada no meio do job. Resultado: 5
    reels reprovados no portao 1 por um erro que nao tem nada a ver com o reel.

    Chamar o binario do cache tira o pipeline da mao do registry: ele passa a
    depender do que ESTA na maquina, que e o que a regra sempre quis dizer.
    """
    base = Path.home() / ".npm" / "_npx"
    achados = []
    for pkg in base.glob("*/node_modules/hyperframes/package.json"):
        binario = pkg.parent.parent / ".bin" / "hyperframes"
        if not binario.exists():
            continue
        try:
            v = json.loads(pkg.read_text()).get("version", "0")
            achados.append((tuple(int(x) for x in v.split(".")[:3]), v, binario))
        except Exception:
            continue
    if not achados:
        return None
    return max(achados)[1:]


def npx_hyperframes(args, cwd):
    """Nada de baixar no meio do job — nem por acidente do `npx`."""
    achado = _hyperframes_do_cache()
    if achado:
        versao, binario = achado
        r = sh([str(binario)] + args, cwd=cwd)
        r.versao_hyperframes = versao   # so para o log dizer o que rodou
        return r
    return sh(["npx", "--no-install", "hyperframes"] + args, cwd=cwd)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--avatar", required=True)
    ap.add_argument("--ws", required=True)
    ap.add_argument("--alvo", default="reel")
    ap.add_argument("--textos", default=None)
    ap.add_argument("--qualidade", default="high", choices=["high", "standard", "draft"])
    # `--flow` existe para o MOTOR SER COMPARTILHADO entre domínios. Sem ele o
    # `preparar.py` deriva o repo da pasta-pai DESTE script — o que faz um job do
    # promoavatar3 ler o `flow.json` do promoavatar (templates e padrão errados).
    # Passe o `flow.json` do domínio do job; `--mapa` acompanha, para o caso de o
    # domínio guardar os templates em outro lugar.
    ap.add_argument("--flow", default=None,
                    help="flow.json do DOMÍNIO do job (repassado ao preparar.py)")
    ap.add_argument("--mapa", default=None,
                    help="templates/mapa.json do domínio (repassado ao preparar.py)")
    ap.add_argument("--cta", default=str(REPO / "cta" / "cta-9x16.mp4"))
    ap.add_argument("--sem-cta", action="store_true")
    ap.add_argument("--sem-legenda", action="store_true",
                    help="legenda palavra a palavra e LIGADA por default "
                         "(docs/legenda.md); isto desliga")
    ap.add_argument("--pular-preparo", action="store_true",
                    help="ja existe index.html e voce so quer render/QC")
    ap.add_argument("--saida", default=None,
                    help="copia o entregavel para ESTE caminho no fim (contrato da "
                         "fase do bot: o servico vigia esse arquivo)")
    a = ap.parse_args()

    # CTA padrão segue o DOMÍNIO, não o repo do motor: com `--flow` de outro
    # projeto, `<repo do motor>/cta/cta-9x16.mp4` seria o clipe errado no fecho.
    if a.flow and a.cta == str(REPO / "cta" / "cta-9x16.mp4"):
        dominio = Path(os.path.expanduser(a.flow)).parent
        cand = dominio / "cta" / "cta-9x16.mp4"
        if cand.exists():
            a.cta = str(cand)

    ws = Path(os.path.expanduser(a.ws))
    motion, final = ws / "motion", ws / "final"
    final.mkdir(parents=True, exist_ok=True)

    # ---- 1. preparar: midia, imagens, tempos, template, index.html ----
    if not a.pular_preparo:
        passo("1/6 preparar (midia, transcricao, imagens, tempos, template, HTML)")
        cmd = [sys.executable, str(AQUI / "preparar.py"), "--avatar",
               os.path.expanduser(a.avatar), "--ws", str(ws), "--alvo", a.alvo]
        if a.textos:
            cmd += ["--textos", os.path.expanduser(a.textos)]
        # Repassar é o que faz o motor servir a outro domínio: sem isto o
        # `preparar.py` cai no fallback `REPO = <pasta do script>.parent`.
        if a.flow:
            cmd += ["--flow", os.path.expanduser(a.flow)]
        if a.mapa:
            cmd += ["--mapa", os.path.expanduser(a.mapa)]
        if a.sem_legenda:
            cmd += ["--sem-legenda"]
        r = sh(cmd)
        print(r.stdout.rstrip() or r.stderr.rstrip())
        if r.returncode != 0:
            return 3 if r.returncode == 3 else 2
    index = motion / "index.html"
    if not index.exists():
        erro(f"sem {index} — rode sem --pular-preparo")

    # ---- 2. portao 1: o determinismo ANTES de renderizar ----
    # Renderizar para descobrir com o olho o que o lint diria de graca e o
    # desperdicio mais caro da fase.
    passo("2/6 portao 1 (lint + ritmo visual) — antes de gastar render")
    r = npx_hyperframes(["lint", "."], cwd=str(motion))
    # Qual hyperframes rodou: sem isto, "o reel do A#25 saiu diferente" vira
    # investigacao. O binario vem do cache, entao a versao NAO e a latest.
    print(f"hyperframes {getattr(r, 'versao_hyperframes', 'via npx (latest)')}")
    print((r.stdout or r.stderr).strip()[-400:])
    if r.returncode != 0:
        print("REPROVADO no lint — nao renderizei.")
        return 3
    lt = AQUI / "lint-timeline.py"
    if not lt.exists():
        lt = Path.home() / ".claude/skills/reel-edita-inema/scripts/lint-timeline.py"
    if lt.exists():
        r = sh([sys.executable, str(lt), str(index)])
        print((r.stdout or r.stderr).strip()[-300:])
        if r.returncode != 0:
            print("REPROVADO no ritmo visual (beat > 4s) — nao renderizei.")
            return 3

    # ---- 3. render do CORPO ----
    passo(f"3/6 render do corpo (--quality {a.qualidade})")
    r = npx_hyperframes(["render", ".", "-o", "corpo.mp4", "-q", a.qualidade],
                        cwd=str(motion))
    corpo = motion / "corpo.mp4"
    if r.returncode != 0 or not corpo.exists():
        print((r.stdout or r.stderr).strip()[-600:])
        erro("render falhou")
    print(f"corpo {corpo}  {duracao(str(corpo)):.2f}s")

    # ---- 4. revisor, sobre o CORPO ----
    passo("4/6 revisor (audio do render, silencio, ritmo)")
    r = sh([sys.executable, str(AQUI / "revisor.py"), "--video", str(corpo),
            "--ws", str(ws)])
    print((r.stdout or r.stderr).rstrip())
    if r.returncode != 0:
        print("REPROVADO no revisor.")
        return 3

    # ---- 5. CTA no fim ----
    passo("5/6 CTA + entregavel")
    entrega = final / "reel.mp4"
    cta = os.path.expanduser(a.cta)
    if a.sem_cta:
        shutil.copy(corpo, entrega)
        print("CTA pulado (--sem-cta)")
    elif not os.path.exists(cta):
        erro(f"CTA nao existe: {cta}")
    else:
        # Mesmos parametros nos dois (h264/yuv420p/30fps, aac 48k stereo), entao
        # o concat demuxer copia sem reencodar. Se algum dia divergirem, o copy
        # falha ou sai com duracao errada — por isso a duracao e CONFERIDA
        # abaixo, e ai reencodamos.
        lista = ws / "concat.txt"
        lista.write_text(f"file '{corpo}'\nfile '{cta}'\n", encoding="utf-8")
        r = sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                "-i", str(lista), "-c", "copy", str(entrega)])
        esperado = duracao(str(corpo)) + duracao(cta)
        if r.returncode != 0 or abs(duracao(str(entrega)) - esperado) > 0.2:
            print("concat por copia nao bateu a duracao — reencodando")
            r = sh(["ffmpeg", "-y", "-v", "error", "-i", str(corpo), "-i", cta,
                    "-filter_complex",
                    "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    str(entrega)])
            if r.returncode != 0:
                erro("concat do CTA falhou: " + r.stderr.strip()[:300])
    print(f"entregavel {entrega}  {duracao(str(entrega)):.2f}s")

    # ---- 6. QC visual, sobre o ENTREGAVEL (para o CTA entrar no quadro) ----
    passo("6/6 QC (portoes 2 e 3)")
    r = sh([sys.executable, str(AQUI / "qc-frames.py"), "--video", str(entrega),
            "--ws", str(ws)])
    print((r.stdout or r.stderr).rstrip())
    if r.returncode != 0:
        print("REPROVADO no QC.")
        return 3

    # A copia para `--saida` e a ULTIMA coisa, depois de todos os portoes: o
    # servico do bot trata o aparecimento desse arquivo como "render pronto".
    # Copiar antes do QC faria um reel reprovado ser entregue como bom.
    if a.saida:
        destino = Path(os.path.expanduser(a.saida))
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(entrega, destino)
        print(f"saida       {destino}")

    print(f"\nPRONTO      {entrega}")
    print(f"OLHE        {ws/'qc'/'mosaico.png'}  — uma imagem, nao a serie de frames.")
    print("            imagem 1 provoca? headline le de relance? o fecho tem o CTA?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
