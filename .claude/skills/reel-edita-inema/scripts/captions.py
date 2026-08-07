#!/usr/bin/env python3
"""Gera 'beats' de legenda a partir de um transcript word-level (Groq/Whisper).
Estilo retenção: 2-3 palavras por beat, sincronizadas com a voz, com uma palavra-chave
em destaque. Saída JSON: [{start, end, words:[{w, hi}]}].

Uso: captions.py --transcript corte-final.json [--max-words 3] [--out captions.json]
     [--keywords "palavra1,palavra2,..."] [--windows "2.4-6.1,34-38"]

O destaque: se uma palavra está na lista de --keywords, é marcada com hi=true (é pintada
na sua COR DE ACENTO na composição). Se não houver match, destaca-se a palavra mais longa
do beat. NÃO há lista de keywords fixa: passe as SUAS por --keywords conforme o conteúdo
de cada vídeo (números, nomes de marca, conceitos fortes). É isto que evita que as
legendas saiam iguais às de ninguém.
"""
import json, re, argparse

def norm(w): return re.sub(r"[^a-zA-Z0-9à-ÿ.]", "", w.lower())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--max-words", type=int, default=3)
    ap.add_argument("--out", default="captions.json")
    ap.add_argument("--keywords", default="",
                    help="palavras a destacar (na SUA cor de acento), separadas por vírgula")
    ap.add_argument("--windows", default="",
                    help="apenas beats dentro destas janelas (na câmera), ex '2.4-6.1,34-38'")
    a = ap.parse_args()
    wins = []
    for seg in a.windows.split(","):
        seg = seg.strip()
        if "-" in seg:
            lo, hi = seg.split("-"); wins.append((float(lo), float(hi)))
    kw = set(k.strip().lower() for k in a.keywords.split(",") if k.strip())

    words = [w for w in json.load(open(a.transcript)).get("words", []) if w.get("start") is not None]
    beats = []
    i = 0
    while i < len(words):
        chunk = words[i:i+a.max_words]
        # quebrar o beat se uma palavra terminar em sinal forte (. ? !)
        cut = len(chunk)
        for j, w in enumerate(chunk):
            if re.search(r"[.?!]$", w["word"].strip()):
                cut = j+1; break
        chunk = chunk[:cut]
        start = chunk[0]["start"]
        end = chunk[-1].get("end", chunk[-1]["start"]+0.3)
        # escolher keyword: primeira que esteja em kw, senão a mais longa do beat
        hi_idx = -1
        for j, w in enumerate(chunk):
            if norm(w["word"]) in kw: hi_idx = j; break
        if hi_idx == -1:
            hi_idx = max(range(len(chunk)), key=lambda j: len(norm(chunk[j]["word"])))
        ws = [{"w": w["word"].strip(), "hi": (j == hi_idx)} for j, w in enumerate(chunk)]
        mid = (start+end)/2
        if not wins or any(lo <= mid <= hi for lo, hi in wins):
            beats.append({"start": round(start, 2), "end": round(end, 2), "words": ws})
        i += cut

    json.dump(beats, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"{len(beats)} beats -> {a.out}")
    for b in beats[:6]:
        print(f"  {b['start']:5.2f}-{b['end']:5.2f}  " +
              " ".join(("*"+x["w"]+"*" if x["hi"] else x["w"]) for x in b["words"]))
    print("  ...")

if __name__ == "__main__":
    main()
