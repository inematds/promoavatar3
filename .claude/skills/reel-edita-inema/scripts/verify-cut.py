#!/usr/bin/env python3
"""COMPORTA DURA — Verifica programaticamente que um corte está LIMPO antes de animar.
Falha (exit 1) se houver silêncios longos no corpo ou repetições. É bloqueante: NÃO se
anima nem se entrega um corte que não passe nisto.

Verifica 3 coisas:
  1) Silêncios >= --max-sil dentro do CORPO (são permitidos no final, p.ex. encerramento "tchau tchau").
  2) N-gramas (2/3/4) consecutivos repetidos na transcrição -> repetição audível.
  3) (info) duração total.

Uso:
  verify-cut.py --media corte.mp4 --transcript corte-word.json [--max-sil 0.6]
                [--noise -30dB] [--tail 1.5]
  (transcript = re-transcrição do CORTE já feito, word-level)

Exit 0 = PASSA. Exit 1 = FALHA (imprime o que falha).
"""
import json, re, sys, subprocess, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--media", required=True)
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--max-sil", type=float, default=0.6, help="silêncio máx permitido no corpo (s)")
    ap.add_argument("--noise", default="-30dB")
    ap.add_argument("--tail", type=float, default=1.5, help="margem final ignorada (encerramento)")
    ap.add_argument("--allow", action="append", default=[],
        help="n-grama de repetição PRÓXIMA confirmado como paralelismo retórico intencional "
             "(não é tomada dobrada). Repetível. Só use após LER o texto e confirmar que "
             "não soa repetido. Ex: --allow 'lo veo para'")
    a = ap.parse_args()
    allow = {s.lower().strip() for s in a.allow}

    fails = []

    # duração
    dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",a.media], capture_output=True, text=True).stdout.strip())

    # 1) silêncios no corpo
    out = subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",a.media,
        "-af",f"silencedetect=noise={a.noise}:d={a.max_sil}","-f","null","-"],
        capture_output=True, text=True).stderr
    # start e duration saem em linhas distintas; são emparelhados na ordem de aparição
    starts = [float(m) for m in re.findall(r"silence_start: ([-\d.]+)", out)]
    sdurs  = [float(m) for m in re.findall(r"silence_duration: ([\d.]+)", out)]
    durs = list(zip(starts, sdurs))
    body_sil = [(s,sd) for (s,sd) in durs if max(0.0,s) < dur - a.tail]
    if body_sil:
        fails.append("SILÊNCIOS longos no corpo (s, dur): " +
                     ", ".join(f"{s:.1f}s/{d:.2f}" for s,d in body_sil))

    # 2) repetições n-gram consecutivas
    words = json.load(open(a.transcript)).get("words", [])
    wl = [w["word"].lower().strip("¿?¡!,.\"'") for w in words if w.get("word")]
    reps = []
    for n in (2,3,4):
        for i in range(len(wl)-2*n+1):
            x, y = wl[i:i+n], wl[i+n:i+2*n]
            if x == y and all(len(t) > 1 for t in x):
                reps.append((n, " ".join(x)))
    if reps:
        uniq = sorted(set(reps))
        fails.append("REPETIÇÕES consecutivas: " + "; ".join(f"[{n}] {g}" for n,g in uniq))

    # 2b) repetições PRÓXIMAS não adjacentes (tomada dobrada com inciso no meio:
    #     p.ex. "quem entender ... e é que é assim ... quem entender").
    #     o verify consecutivo não as pega. Busca um n-grama de CONTEÚDO que reapareça
    #     dentro das próximas GAP palavras. Filtra stopwords para não marcar vícios de linguagem.
    STOP = {"de","la","el","que","y","a","en","lo","un","una","o","se","es","le","su",
            "por","con","los","las","sea","te","me","va","al","ya","si","no","más","mas",
            "tu","mi","él","el","ese","eso","esto","esta","este","como","cómo"}
    GAP = 7
    near = []
    for n in (2,3):
        for i in range(len(wl)-n):
            x = wl[i:i+n]
            # o n-grama deve ter ao menos uma palavra de CONTEÚDO (len>=4 e não stopword)
            if not any(len(t) >= 4 and t not in STOP for t in x):
                continue
            for j in range(i+n, min(i+n+GAP, len(wl)-n+1)):
                if wl[j:j+n] == x:
                    near.append((n, " ".join(x)))
                    break
    near = [(n,g) for (n,g) in near if g not in allow]   # remove paralelismos já confirmados
    if near:
        uniq = sorted(set(near))
        fails.append("REPETIÇÕES próximas SUSPEITAS (tomada dobrada com inciso). LEIA o texto "
                     "e, para cada uma: se for tomada dobrada -> conserte o corte; se for paralelismo "
                     "retórico intencional -> rode de novo com --allow '<n-grama>'. Suspeitas: " +
                     "; ".join(f"[{n}] {g}" for n,g in uniq))

    print(f"duração: {dur:.2f}s")
    if fails:
        print("RESULTADO: ❌ FALHA")
        for f in fails: print("  -", f)
        return 1
    print("RESULTADO: ✅ PASSA — sem silêncios longos no corpo, sem repetições.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
