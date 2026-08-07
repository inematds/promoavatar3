#!/usr/bin/env python3
"""qc-frames.py — o portao 3 (o olho) como script.

Por que existe: os portoes 1 e 2 ja eram scripts; o 3 era prosa — "~10 frames
dirigidos, nunca a serie inteira". Instrucao nao e portao, e frame e o item MAIS
caro do job: cada um entra no contexto e e RELIDO em toda mensagem seguinte ate
o fim. Medido em outra fase do mesmo sistema: um loop de verificacao por imagem
levou uma tarefa de 3 min para 13 min e 13,5M tokens.

O que este script tira do modelo:
  - QUAIS frames olhar     -> sai do segmentos.json, nao do julgamento;
  - QUANTOS entram no contexto -> UM mosaico (+1 recorte da headline), nao 10;
  - o que NAO precisa de olho  -> checado aqui, de graca:
      * o PORTAO 2 inteiro (duracao, 1080x1920, os dois streams) — ele foi
        absorvido: rodar `ffprobe` a parte e depois isto era verificar duas
        vezes a mesma coisa;
      * a imagem do topo TROCOU em cada corte (o motor de retencao do reel);
      * nenhum frame preto/apagado (render truncado, asset faltando);
      * nenhum par de amostras identico (render congelado).

O que ele NAO faz, de proposito: OCR, nota estetica, qualquer tentativa de
substituir o julgamento. Os tres testes da imagem 1 (transferencia, polegar,
tensao) continuam sendo seus — o script so entrega o que olhar.

A comparacao e feita SO na faixa do topo. O meio e video de avatar falando:
dois frames quaisquer diferem, entao um diff de quadro inteiro passa sempre e
nao mede nada. A geometria sai do template que o preparar.py ja resolveu.

Rode UMA vez, no render ANTES do mix-sfx.py: o mix roda com `-c:v copy` e o
video sai bit a bit identico: uma segunda passada nao ve nada novo e custa mais
uma imagem no contexto.

Uso:
  python3 qc-frames.py --video <ws>/motion/out.mp4 --ws <ws>
  [--segmentos ...] [--manifesto ...] [--out <ws>/qc] [--limiar 6.0]

Saida: <out>/mosaico.png (o que voce olha), <out>/headline-t0.png (a capa em
resolucao cheia) e uma tabela. Exit 0 tudo passou · 3 alguma checagem falhou ·
2 erro de uso/arquivo.
"""
import argparse, json, math, os, subprocess, sys
from pathlib import Path

AMOSTRA = 64          # o diff roda em 64x64 cinza: 4096 bytes, sem dependencia
MARGEM_POS_TRANSICAO = 0.25   # respiro depois do crossfade, para nao amostrar o blend


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, **kw)


def erro(msg: str, code: int = 2):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(code)


def ler_json(p, oque):
    try:
        return json.loads(Path(os.path.expanduser(p)).read_text(encoding="utf-8"))
    except Exception as e:
        erro(f"{oque} invalido ou ausente ({p}): {e}")


def sonda(video: str) -> dict:
    """Duracao, resolucao e presenca de audio — o portao 2 inteiro, numa chamada.

    Fica AQUI de proposito: mandar o agente rodar `ffprobe` a parte e depois
    este script era pedir duas verificacoes que se sobrepoem. Portao 2 e 3
    passaram a ser um comando so.
    """
    r = sh(["ffprobe", "-v", "error", "-of", "json",
            "-show_entries", "format=duration:stream=width,height,codec_type", video])
    try:
        d = json.loads(r.stdout)
    except Exception:
        return {"duracao": 0.0}
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    return {"duracao": float(d.get("format", {}).get("duration", 0) or 0),
            "largura": v.get("width"), "altura": v.get("height"),
            "tem_audio": any(s.get("codec_type") == "audio" for s in d.get("streams", []))}


def miniatura(video: str, t: float, crop: tuple) -> bytes:
    """A faixa do topo no instante t, 64x64 em cinza. Sem PIL: rawvideo puro."""
    w, h, x, y = crop
    r = sh(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video,
            "-frames:v", "1",
            "-vf", f"crop={w}:{h}:{x}:{y},scale={AMOSTRA}:{AMOSTRA},format=gray",
            "-f", "rawvideo", "-"])
    return r.stdout or b""


def mad(a: bytes, b: bytes) -> float:
    """Diferenca media absoluta, 0-255. Troca de imagem >> zoom/pulso do template."""
    if not a or not b or len(a) != len(b):
        return -1.0
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def luma(a: bytes) -> float:
    return (sum(a) / len(a)) if a else -1.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True, help="o render ANTES do mix-sfx.py")
    ap.add_argument("--ws", default=None, help="workspace — de onde saem manifesto/segmentos")
    ap.add_argument("--manifesto", default=None)
    ap.add_argument("--segmentos", default=None)
    ap.add_argument("--out", default=None, help="destino dos frames (padrao <ws>/qc)")
    ap.add_argument("--limiar", type=float, default=6.0,
                    help="MAD minimo para considerar que a imagem do topo trocou")
    a = ap.parse_args()

    video = os.path.expanduser(a.video)
    if not os.path.exists(video):
        erro(f"video nao existe: {video}")
    ws = Path(os.path.expanduser(a.ws)) if a.ws else Path(video).parent.parent
    man_p = a.manifesto or (ws / "manifesto.json")
    seg_p = a.segmentos or (ws / "segmentos.json")
    man = ler_json(man_p, "manifesto")
    segs = ler_json(seg_p, "segmentos")
    if not isinstance(segs, list) or not segs:
        erro("segmentos.json precisa ser uma lista nao vazia")
    out = Path(os.path.expanduser(a.out)) if a.out else ws / "qc"
    (out / "frames").mkdir(parents=True, exist_ok=True)

    # ---- geometria da faixa do topo + duracao da transicao, do TEMPLATE ----
    # Sem o template nao da para cortar a faixa certa, e um diff de quadro
    # inteiro passa sempre (o avatar se mexe). Entao isso e requisito, nao
    # conveniencia.
    tpl_p = man.get("template_arquivo")
    if not tpl_p:
        erro("manifesto sem `template_arquivo` — rode o preparar.py antes; sem a "
             "geometria da faixa do topo este QC nao mede nada")
    tpl = ler_json(tpl_p, "template")
    cv = tpl.get("canvas", {})
    topo = (tpl.get("faixas") or {}).get("topo") or {}
    crop = (cv.get("largura", 1080), topo.get("altura", 704), 0, topo.get("y", 0))
    trans = float((tpl.get("transicao") or {}).get("duracao", 0.0))
    espera = trans + MARGEM_POS_TRANSICAO

    info = sonda(video)
    dur = info.get("duracao", 0.0)
    if dur <= 0:
        erro(f"ffprobe nao leu a duracao de {video}")
    portao2 = []
    esperado = (cv.get("largura", 1080), cv.get("altura", 1920))
    if (info.get("largura"), info.get("altura")) != esperado:
        portao2.append(f"resolucao {info.get('largura')}x{info.get('altura')} — "
                       f"o template pede {esperado[0]}x{esperado[1]}")
    if not info.get("tem_audio"):
        portao2.append("sem stream de audio — render mudo")

    # ---- quais frames: t=0, cada corte (pos-transicao), e o fecho/CTA ----
    pontos = [(0.0, "t=0 · capa")]
    for i, s in enumerate(segs[1:], start=2):
        t = float(s.get("inicio", 0)) + espera
        if t < dur:
            pontos.append((t, f"corte {i}"))
    pontos.append((max(0.0, dur - 1.0), "fecho · CTA"))

    linhas, falhas = [], list(portao2)
    anterior_mini, anterior_rot = None, None
    for k, (t, rot) in enumerate(pontos):
        arq = out / "frames" / f"f{k:02d}.png"
        r = sh(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", video,
                "-frames:v", "1", str(arq)])
        if r.returncode != 0 or not arq.exists():
            falhas.append(f"{rot}: nao extraiu o frame em {t:.2f}s")
            continue
        mini = miniatura(video, t, crop)
        lum = luma(mini)
        d = mad(anterior_mini, mini) if anterior_mini is not None else None
        marca = ""
        if lum < 8:
            falhas.append(f"{rot} ({t:.2f}s): faixa do topo PRETA (luma {lum:.1f}) "
                          f"— asset faltando ou render truncado")
            marca = "  <- PRETO"
        elif d is not None and rot.startswith("corte") and d < a.limiar:
            falhas.append(f"{rot} ({t:.2f}s): a imagem do topo NAO trocou "
                          f"(MAD {d:.1f} < {a.limiar}) — o motor de retencao do reel "
                          f"depende dessa troca")
            marca = "  <- NAO TROCOU"
        elif d is not None and d == 0.0:
            falhas.append(f"{rot} ({t:.2f}s): identico ao frame anterior — render congelado")
            marca = "  <- CONGELADO"
        linhas.append(f"  [{k:02d}] {t:6.2f}s  {rot:<14} luma {lum:5.1f}"
                      + (f"  dif {d:5.1f}" if d is not None else "  dif     —") + marca)
        anterior_mini, anterior_rot = mini, rot

    # ---- UM mosaico: e isso que entra no contexto, nao os frames soltos ----
    n = len(list((out / "frames").glob("f*.png")))
    cols = min(4, max(1, n))
    rows = math.ceil(n / cols)
    mosaico = out / "mosaico.png"
    r = sh(["ffmpeg", "-y", "-v", "error", "-f", "image2",
            "-i", str(out / "frames" / "f%02d.png"),
            "-filter_complex",
            f"scale=270:480,tile={cols}x{rows}:padding=8:margin=8:color=#111417",
            "-frames:v", "1", str(mosaico)])
    if r.returncode != 0:
        falhas.append("mosaico nao foi gerado: " + (r.stderr or b"").decode()[:200])

    # A headline em resolucao cheia. No mosaico (1/4) da para fazer o teste do
    # POLEGAR — a imagem provoca? — mas nao da para julgar se a manchete LE de
    # relance. Sao duas perguntas diferentes, e uma imagem a mais resolve a
    # segunda; olhar os 10 frames grandes resolveria as duas e custaria 10.
    hl = out / "headline-t0.png"
    w, h, x, y = crop
    sh(["ffmpeg", "-y", "-v", "error", "-ss", "0", "-i", video, "-frames:v", "1",
        "-vf", f"crop={w}:{h}:{x}:{y}", str(hl)])

    print(f"video      {video}  {dur:.2f}s  {info.get('largura')}x{info.get('altura')}"
          f"  audio={info.get('tem_audio')}   (portao 2 incluido)")
    print(f"faixa topo {crop[0]}x{crop[1]} em y={crop[3]}  (template {tpl.get('nome')})")
    print(f"amostras   {len(pontos)}  (corte + {espera:.2f}s: transicao {trans:.2f}s)")
    print("\n".join(linhas))
    for f in falhas:
        print(f"  FALHA {f}")
    print(f"mosaico    {mosaico}   <- OLHE ESTE. Nao abra os frames soltos.")
    print(f"headline   {hl}        <- so se precisar julgar legibilidade")
    if not falhas:
        print("portao 3   determinismo OK — resta o olho: imagem 1 provoca? "
              "headline le de relance? o fecho tem o CTA?")
    return 3 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
