#!/usr/bin/env python3
"""detect-repeats.py — acha repeticoes num transcript word-level (Groq/whisper).

Existia na documentacao da skill e NAO existia em disco (achado em 2026-08-03:
os 9 caminhos de script citados estavam quebrados). Escrito para fechar isso e,
de quebra, tirar do olho humano um trabalho que e determinstico.

Acha dois tipos de repeticao, que sao os que aparecem em gravacao de avatar/
talking-head:

  1. TOMADA DOBRADA — a mesma sequencia de palavras dita duas vezes seguidas
     ("o que muda / o que muda na sua vida"). Compara janelas de n-gramas
     vizinhas, ignorando pontuacao e caixa.
  2. FALSA PARTIDA — a frase reinicia: um prefixo curto repetido logo em
     seguida ("quem aprende... quem aprende isso agora").

Saida legivel por padrao; `--json` para consumo por script/portao.
Exit 0 = nada encontrado. Exit 1 = achou (serve como comporta em CI/QC).

Uso:
  python3 detect-repeats.py edicion/transcript.json
  python3 detect-repeats.py edicion/transcript.json --json --min-palavras 3
"""
import argparse, json, re, sys, unicodedata


def normalizar(p: str) -> str:
    """Compara som/letra, nao pontuacao nem acento — o whisper varia nisso."""
    p = unicodedata.normalize("NFD", p.lower())
    p = "".join(c for c in p if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", p)


def palavras(doc) -> list:
    """Aceita os formatos que o transcribe-groq.sh produz, sem inventar:
    {"words":[{"word","start","end"}]} ou {"segments":[{"words":[...]}]}."""
    if isinstance(doc, dict):
        if isinstance(doc.get("words"), list):
            return doc["words"]
        if isinstance(doc.get("segments"), list):
            out = []
            for s in doc["segments"]:
                out.extend(s.get("words") or [])
            if out:
                return out
    if isinstance(doc, list):
        return doc
    return []


def achar(ws, minp: int, maxp: int):
    txt = [normalizar(str(w.get("word", ""))) for w in ws]
    ini = [w.get("start") for w in ws]
    fim = [w.get("end") for w in ws]
    achados, cobertos = [], set()

    # n-gramas grandes primeiro: "o que muda o que muda" deve virar UM achado
    # de 3 palavras, nao tres de 1.
    for n in range(maxp, minp - 1, -1):
        for i in range(len(txt) - 2 * n + 1):
            a, b = txt[i:i + n], txt[i + n:i + 2 * n]
            if not all(a) or a != b:
                continue
            if any(j in cobertos for j in range(i, i + 2 * n)):
                continue
            cobertos.update(range(i, i + 2 * n))
            achados.append({
                "tipo": "tomada-dobrada",
                "palavras": n,
                "texto": " ".join(str(w.get("word", "")).strip() for w in ws[i:i + n]),
                "inicio": ini[i], "fim": fim[min(i + 2 * n - 1, len(fim) - 1)],
            })
    achados.sort(key=lambda a: (a["inicio"] is None, a["inicio"]))
    return achados


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("--min-palavras", type=int, default=2,
                    help="menor repeticao considerada (default 2; 1 gera ruido)")
    ap.add_argument("--max-palavras", type=int, default=8)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    try:
        doc = json.load(open(a.transcript, encoding="utf-8"))
    except Exception as e:
        print(f"ERRO: nao consegui ler {a.transcript}: {e}", file=sys.stderr)
        return 2

    ws = palavras(doc)
    if not ws:
        print("ERRO: transcript sem palavras (esperado word-level: "
              "{'words':[...]} ou {'segments':[{'words':[...]}]})", file=sys.stderr)
        return 2

    achados = achar(ws, a.min_palavras, a.max_palavras)

    if a.json:
        print(json.dumps({"total": len(achados), "achados": achados},
                         ensure_ascii=False, indent=2))
    elif not achados:
        print(f"OK — nenhuma repeticao em {len(ws)} palavras.")
    else:
        print(f"{len(achados)} repeticao(oes) em {len(ws)} palavras:\n")
        for r in achados:
            t = f"{r['inicio']:.1f}s" if isinstance(r["inicio"], (int, float)) else "?"
            print(f"  [{t}] {r['palavras']}x2 palavras: \"{r['texto']}\"")
        print("\nCorte entre SILENCIOS (silencedetect), nao pelo timestamp do "
              "whisper — ele erra ±0.2-0.3s. Re-transcreva e rode isto de novo.")
    return 1 if achados else 0


if __name__ == "__main__":
    sys.exit(main())
