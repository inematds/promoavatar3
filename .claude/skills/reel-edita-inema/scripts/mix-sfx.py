#!/usr/bin/env python3
"""Mistura SFX sobre um render (em pós). A voz do vídeo é mantida; os SFX
são sobrepostos nos tempos indicados. Aplica um limitador para não saturar.

Uso:
  mix-sfx.py --base render.mp4 --sfx-dir sfx --out final.mp4 \
    --events '[["boom",0.0],["whoosh",6.5],["ding",8.6], ...]'

events: lista JSON de [nome_sfx, tempo_segundos]. nome = arquivo <nome>.wav em sfx-dir.
Volumes padrão pensados como acentos por baixo da voz; ajuste com --vol se for preciso.
Se re-cortar/re-sincronizar o vídeo, RE-TEMPORIZE os eventos (os tempos deles mudam).
"""
import argparse, json, subprocess, os, sys

DEFAULT_VOL = {"whoosh":0.32,"pop":0.28,"type":0.26,"buzz":0.30,"boom":0.42,"ding":0.36,"riser":0.30}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--sfx-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--events", required=True, help='JSON: [["sfx",t],...]')
    ap.add_argument("--vol", default="{}", help='JSON de override de volumes por sfx')
    args = ap.parse_args()

    events = json.loads(args.events)
    vol = dict(DEFAULT_VOL); vol.update(json.loads(args.vol))

    inputs = ["-i", args.base]
    fc, labels = [], ["[0:a]"]
    for i, (name, t) in enumerate(events, start=1):
        path = os.path.join(args.sfx_dir, f"{name}.wav")
        if not os.path.exists(path):
            print(f"AVISO: não existe {path}, pulando", file=sys.stderr); continue
        inputs += ["-i", path]
        ms = int(float(t) * 1000)
        v = vol.get(name, 0.3)
        fc.append(f"[{i}:a]adelay={ms}|{ms},volume={v}[s{i}]")
        labels.append(f"[s{i}]")
    n = len(labels)
    fc.append("".join(labels) + f"amix=inputs={n}:normalize=0:dropout_transition=0,alimiter=limit=0.97[a]")
    cmd = ["ffmpeg","-y",*inputs,"-filter_complex",";".join(fc),
           "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k",args.out,"-loglevel","error"]
    subprocess.run(cmd, check=True)
    print("OK ->", args.out)

if __name__ == "__main__":
    main()
