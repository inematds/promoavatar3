#!/usr/bin/env python3
"""FASE 1 (passo 2) — Monta o corte a partir de islands.json (as ilhotas com keep=true),
colando-as sem pausas. Pad para DENTRO do silêncio (seguro: há >=0.35s de silêncio entre
ilhotas, não há bleed da frase vizinha).

Uso: cut.py --islands islands.json --out edicion/corte-final.mp4 [--crf 17]
"""
import json, subprocess, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--islands", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--crf", type=int, default=17)
    a = ap.parse_args()
    d = json.load(open(a.islands))
    src = d["media"]; pin = d.get("pad_in",0.04); pout = d.get("pad_out",0.09); dur = d["duration"]
    keeps = [(max(0.0, isl["start"]-pin), min(dur, isl["end"]+pout))
             for isl in d["islands"] if isl["keep"]]
    if not keeps:
        print("ERRO: não há ilhotas com keep=true"); return 1
    total = sum(e-s for s,e in keeps)
    print(f"montando {len(keeps)} ilhotas -> ~{total:.2f}s")
    parts=[]
    for i,(s,e) in enumerate(keeps):
        parts.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS[a{i}]")
    ci="".join(f"[v{i}][a{i}]" for i in range(len(keeps)))
    fc=";".join(parts)+f";{ci}concat=n={len(keeps)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",fc,
        "-map","[v]","-map","[a]","-r","30","-c:v","libx264","-preset","medium",
        "-crf",str(a.crf),"-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",a.out],check=True)
    print("OK ->",a.out)

if __name__ == "__main__":
    raise SystemExit(main())
