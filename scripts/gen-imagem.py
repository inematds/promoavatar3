#!/usr/bin/env python3
"""gen-imagem.py — wrapper do inemaimg (flux2-klein) para a skill reel-edita-inema.

Gera uma imagem via a API HTTP local do inemaimg (POST localhost:8000/generate) e
grava o PNG. NAO usa fal (a regra do perfil e midia 100% local). Robusto ao nome do
campo da resposta (image_base64 / image / images[0]).

Uso:
  python3 gen-imagem.py --prompt "..." --out capa.png [--model flux2-klein] [--steps 4] [--seed 7] [--host http://localhost:8000]
  python3 gen-imagem.py --prompt "..." --out topo.png --width 1088 --height 704

NAO mexa em --steps: o flux2-klein e step-distilled e a doc do inemaimg e
explicita — "piora acima de 4". Medido em 2026-08-03: subir para 24 nao melhora,
so muda a imagem (outra trajetoria de amostragem) e custa 5x o tempo.

NAO troque para flux2-dev: ele nao sobe nesta maquina de proposito (falta
bitsandbytes, e carregar o dev atrapalha a GPU). O erro 500
"PackageNotFoundError: bitsandbytes" e esperado, nao e bug para consertar.
"""
import argparse, base64, hashlib, json, sys, urllib.request

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="flux2-klein")
    ap.add_argument("--steps", type=int, default=4)
    ap.add_argument("--seed", type=int, default=7)  # fixo p/ determinismo do reel
    # Variedade SEM perder determinismo.
    #
    # Com --seed 7 em tudo, dois publicos do MESMO assunto (prompts parecidos,
    # que e o caso do promoavatar: muda so o gatilho) recebem imagens GEMEAS de
    # composicao. Medido em 2026-08-03: "jovens" e "profissionais" sairam com o
    # mesmo enquadramento por cima do ombro, o mesmo HUD circular no centro da
    # tela, o mesmo grafico de barras no mesmo canto — mudou a pessoa, nao a
    # cena. Isso e o oposto do "nao repita molde" que a skill exige.
    #
    # --seed-key deriva o seed de um rotulo estavel (ex.: "jovens#2"): mesma
    # chave -> mesmo seed -> mesmo reel re-renderiza igual. A derivacao mora
    # AQUI, e nao no julgamento de quem chama, para ninguem "variar" sorteando
    # numero e quebrar o determinismo sem perceber.
    ap.add_argument("--seed-key", default=None,
                    help='rotulo estavel, ex.: "jovens#2" (alvo#segmento). '
                         'Deriva o seed; tem precedencia sobre --seed.')
    # Default 1024x1024 de proposito: a doc do klein chama 1:1 de "baseline,
    # melhor qualidade geral", e mudar o default mudaria TODO reel, inclusive os
    # disparados no chat. Quem sabe o alvo passa o tamanho.
    #
    # Para a FAIXA DO TOPO do reel empilhado (1080x704 em stack-9x16.sh), usar
    # --width 1088 --height 704: gera ja na proporcao em vez de gerar quadrado e
    # deixar o crop central comer ~35% da altura. Medido em 2026-08-03: 5,0s
    # contra 6,7s do quadrado, porque sao menos pixels. Limites do klein:
    # 128-2048, incrementos de 16 (1088 = 68x16, 704 = 44x16).
    ap.add_argument("--width", type=int, default=1024)
    ap.add_argument("--height", type=int, default=1024)
    ap.add_argument("--host", default="http://localhost:8000")
    a = ap.parse_args()

    seed = a.seed
    if a.seed_key:
        seed = int(hashlib.sha256(a.seed_key.encode()).hexdigest()[:8], 16) % (2**31)

    for nome, valor in (("width", a.width), ("height", a.height)):
        if not (128 <= valor <= 2048) or valor % 16:
            print(f"ERRO: --{nome}={valor} invalido — use 128..2048 em passos de 16",
                  file=sys.stderr)
            sys.exit(4)

    body = json.dumps({
        "model": a.model, "prompt": a.prompt, "steps": a.steps, "seed": seed,
        "width": a.width, "height": a.height,
    }).encode()
    req = urllib.request.Request(f"{a.host}/generate", data=body,
                                 headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            j = json.loads(r.read())
    except Exception as e:
        print(f"ERRO inemaimg: {e} (o servidor esta no ar? curl {a.host}/health)", file=sys.stderr)
        sys.exit(2)

    # descobre o campo da imagem sem inventar: tenta os nomes usuais
    b64 = None
    for k in ("image_base64", "image", "png_base64", "b64", "output"):
        v = j.get(k)
        if isinstance(v, str) and len(v) > 100:
            b64 = v; break
    if b64 is None and isinstance(j.get("images"), list) and j["images"]:
        b64 = j["images"][0]
    if b64 is None:
        print(f"ERRO: nao achei o campo da imagem na resposta. Chaves: {list(j.keys())}", file=sys.stderr)
        sys.exit(3)
    if "," in b64[:64] and b64.strip().startswith("data:"):
        b64 = b64.split(",", 1)[1]
    with open(a.out, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"OK imagem -> {a.out} (model {j.get('model_used', a.model)}, seed {seed})")

if __name__ == "__main__":
    main()
