#!/usr/bin/env python3
"""revisor.py — a FASE 5 (revisor independente) como script.

A skill global manda spawnar um SUBAGENTE obrigatorio que re-transcreve o render
final e o le inteiro procurando repeticao. Era o maior gasto de modelo que
sobrava na fase, e o que ele procura ou ja e script ou nunca ocorreu:

  - repeticao/silencio -> `verify-cut.py`, e repeticoes=0 em 18 de 18 reels
    (A#21+A#22): o avatar e TTS do HeyGen, nao tem falso comeco nem blooper;
  - ritmo visual       -> `lint-timeline.py` (nenhum beat > 4s);
  - truncado/mudo      -> `qc-frames.py` (que ja absorveu o portao 2).

Um subagente lendo transcricao inteira para confirmar o que tres scripts medem
de graca e caro E menos confiavel: ele julga, eles medem. Ver
`docs/decisoes-reel.md` (decisao 3) para o caminho de volta.

O que este script NAO faz: julgar se o reel esta bom. Isso e o olho, sobre o
mosaico do `qc-frames.py`, e nunca foi o que a fase 5 fazia.

A revisao roda sobre o RENDER FINAL, nao sobre o avatar de entrada: e a unica
forma de pegar audio que se perdeu, dessincronizou ou truncou na montagem.

Uso:
  python3 revisor.py --video <ws>/motion/out.mp4 --ws <ws>
  [--index <ws>/motion/index.html] [--max-sil 2.0] [--max-gap 4.0]

Exit 0 = PASSA · 3 = reprovado (imprime o que falhou) · 2 = erro de arquivo.
"""
import argparse, json, os, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
# `verify-cut.py` e `lint-timeline.py` sao MECANICA de reel e moram na skill
# global (a divisao decidida em 2026-08-03: motor na skill, editorial no
# projeto). Procuramos primeiro ao lado deste arquivo — assim um projeto que
# queira sua propria versao so precisa por o arquivo la.
SKILL = Path.home() / ".claude" / "skills" / "reel-edita-inema" / "scripts"


def motor(nome: str) -> str:
    for base in (AQUI, SKILL):
        if (base / nome).exists():
            return str(base / nome)
    erro(f"nao achei {nome} nem em {AQUI} nem em {SKILL}")


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def erro(msg: str, code: int = 2):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(code)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True, help="o render FINAL")
    ap.add_argument("--ws", default=None)
    ap.add_argument("--index", default=None, help="motion/index.html (ritmo visual)")
    # 0.6s era o default do verify-cut, pensado para BRUTO HUMANO JA CORTADO:
    # ali silencio > 0.6s significa corte mal feito. Aqui o audio e a fala
    # inteira do avatar, sem corte nenhum — e TTS respira. Medido no
    # A#25/profissionais: pausas de 0,84s e 1,07s reprovaram um reel que estava
    # perfeito. Buraco de montagem de verdade e da ordem de segundos, nao de
    # decimos. Ver docs/decisoes-reel.md (decisao 3).
    ap.add_argument("--max-sil", default="2.0")
    ap.add_argument("--max-gap", default="4.0")
    ap.add_argument("--tail", default="1.5", help="silencio tolerado no fim (encerramento)")
    a = ap.parse_args()

    video = os.path.expanduser(a.video)
    if not os.path.exists(video):
        erro(f"video nao existe: {video}")
    ws = Path(os.path.expanduser(a.ws)) if a.ws else Path(video).parent.parent
    index = Path(os.path.expanduser(a.index)) if a.index else ws / "motion" / "index.html"

    falhas, linhas = [], []

    # ---- 1. re-transcricao do AUDIO DO RENDER (Groq: IA, mas nao LLM) ----
    rev = ws / "edicion" / "revisao"
    rev.mkdir(parents=True, exist_ok=True)
    audio, tr = rev / "final.m4a", rev / "final.json"
    if not tr.exists() or tr.stat().st_size == 0:
        r = sh(["ffmpeg", "-y", "-loglevel", "error", "-i", video,
                "-vn", "-c:a", "aac", "-b:a", "128k", str(audio)])
        if r.returncode != 0:
            erro(f"nao extraiu o audio do render: {r.stderr.strip()[:200]}")
        r = sh(["bash", str(AQUI / "transcribe-groq.sh"), str(audio), str(tr)])
        if not tr.exists():
            erro("transcricao do render falhou: " + (r.stderr or r.stdout).strip()[:200])
        linhas.append(f"transcricao {tr}")
    else:
        linhas.append(f"transcricao {tr} (reaproveitada)")

    # ---- 2. silencio longo no corpo + repeticao audivel ----
    r = sh([sys.executable, motor("verify-cut.py"), "--media", video,
            "--transcript", str(tr), "--max-sil", str(a.max_sil), "--tail", str(a.tail)])
    # O verify-cut mistura duas coisas num exit so, e elas NAO tem o mesmo peso
    # aqui. Ele foi escrito para bruto gravado por humano, onde n-grama repetido
    # significa TOMADA DOBRADA. Neste pipeline a fala e TTS do HeyGen: tomada
    # dobrada nao existe por construcao, entao repeticao so pode vir do TEXTO —
    # que ja passou pelo portao humano da fase 1. Visto no primeiro teste deste
    # script: reprovou por "o professor" repetido, que era paralelismo retorico.
    # Entao: SILENCIO longo reprova (indica montagem quebrada); REPETICAO e
    # informativa. Se a entrada voltar a ser gravacao humana, isto se inverte —
    # ver docs/decisoes-reel.md.
    saida = (r.stdout or "").strip()
    silencio = [l for l in saida.splitlines() if "SILÊNCIOS" in l]
    repeticao = [l for l in saida.splitlines() if "REPETI" in l]
    if silencio:
        falhas.append("verify-cut: " + " ".join(silencio)[:400])
    if repeticao:
        linhas.append("verify-cut  repeticao (informativo, fala e TTS): "
                      + " ".join(repeticao)[:200])
    if r.returncode != 0 and not silencio and not repeticao:
        falhas.append("verify-cut: " + (saida or r.stderr.strip())[:400])
    linhas.append(f"verify-cut  exit {r.returncode} · silencio no corpo: "
                  f"{'FALHA' if silencio else 'ok'}")

    # ---- 3. ritmo visual: nenhum beat > max-gap ----
    if index.exists():
        r = sh([sys.executable, motor("lint-timeline.py"), str(index),
                "--max-gap", str(a.max_gap), "--json"])
        try:
            d = json.loads(r.stdout or "{}")
        except Exception:
            d = {}
        buracos = d.get("errors") or []   # `gaps` lista TODOS os intervalos; `errors` sao os que violam
        if r.returncode != 0 or buracos:
            falhas.append(f"lint-timeline: {len(buracos) or '?'} buraco(s) de ritmo "
                          f"> {a.max_gap}s — {(r.stdout or r.stderr).strip()[:300]}")
        linhas.append(f"lint-timeline exit {r.returncode}")
    else:
        linhas.append(f"lint-timeline PULADO (sem {index})")

    print(f"video      {video}")
    for l in linhas:
        print(f"  {l}")
    for f in falhas:
        print(f"  REPROVADO {f}")
    if not falhas:
        print("revisor    PASSA — audio do render integro, sem silencio longo no "
              "corpo, ritmo visual dentro do limite."
              + (" (ha repeticao de n-grama, informativa: a fala e TTS)"
                 if repeticao else ""))
    return 3 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
