#!/usr/bin/env python3
"""gen-imagem.py — wrapper do inemaimg (flux2-klein) para a skill reel-edita-inema.

Gera uma imagem via a API HTTP local do inemaimg (POST localhost:8000/generate) e
grava o PNG. NAO usa fal (a regra do perfil e midia 100% local). Robusto ao nome do
campo da resposta (image_base64 / image / images[0]).

Uso:
  python3 gen-imagem.py --prompt "..." --out capa.png [--model flux2-klein] [--steps 4] [--seed 7] [--host http://localhost:8000]
  python3 gen-imagem.py --prompt "..." --out topo.png --width 1088 --height 704

Host e modelo saem de INEMAIMG_HOST / INEMAIMG_MODEL quando definidos (default:
localhost:8000 e flux2-klein). Numa maquina sem GPU, apontar INEMAIMG_HOST para
o inemaimg de outra maquina (tunel SSH) e o caminho barato; provedor de nuvem
(kie/fal/agnes) NAO cabe aqui, porque muda o corpo e a resposta, nao so o host.

NAO mexa em --steps: o flux2-klein e step-distilled e a doc do inemaimg e
explicita — "piora acima de 4". Medido em 2026-08-03: subir para 24 nao melhora,
so muda a imagem (outra trajetoria de amostragem) e custa 5x o tempo.

NAO troque para flux2-dev: ele nao sobe nesta maquina de proposito (falta
bitsandbytes, e carregar o dev atrapalha a GPU). O erro 500
"PackageNotFoundError: bitsandbytes" e esperado, nao e bug para consertar.
"""
import argparse, base64, hashlib, json, os, struct, sys, time, urllib.request

# Host e modelo vêm do AMBIENTE, com o default sendo exatamente o de sempre.
#
# Por quê: numa VPS não há inemaimg em localhost:8000, e o caminho literal fazia
# toda imagem falhar com "o servidor esta no ar?". Com INEMAIMG_HOST a mesma
# máquina pode apontar para a GPU de casa (túnel SSH) sem editar script — e sem
# mudar nada aqui, onde o default continua valendo.
#
# Trocar de PROVEDOR (kie, fal, agnes) é outra coisa: muda o formato do corpo e
# da resposta, não só o endereço. Isso é adaptador, não variável — não finja que
# apontar INEMAIMG_HOST para outra API resolve.
HOST_PADRAO = os.environ.get("INEMAIMG_HOST", "http://localhost:8000")
MODELO_PADRAO = os.environ.get("INEMAIMG_MODEL", "flux2-klein")

# QUEM gera. `inemaimg` é o default e o caminho de casa (GPU local, custo zero).
# Fora daqui não há GPU, e aí entra um provedor de API — que NÃO é só outro
# endereço: muda o corpo do request, o formato da resposta e o que o serviço
# respeita do que voce pediu. Por isso adaptador, e nao variavel de host.
PROVEDOR = os.environ.get("IMG_PROVEDOR", "inemaimg").strip().lower()

def chave(nome: str) -> str:
    """Segredo do ambiente, ou do arquivo em IMG_ENV_PATH — mesmo padrao do
    GROQ_ENV_PATH e do HEYGEN_ENV_PATH: caminho no .env, segredo no arquivo."""
    v = os.environ.get(nome)
    if v:
        return v
    caminho = os.environ.get("IMG_ENV_PATH", "")
    if caminho and os.path.exists(caminho):
        for linha in open(caminho, encoding="utf-8"):
            linha = linha.strip()
            if linha.startswith("#") or "=" not in linha:
                continue
            k, _, val = linha.partition("=")
            if k.strip() == nome:
                return val.strip().strip('"').strip("'")
    print(f"ERRO: falta {nome} (no ambiente ou no arquivo IMG_ENV_PATH)", file=sys.stderr)
    sys.exit(5)

def extrair_b64(j: dict):
    """Acha o campo da imagem sem inventar: tenta os nomes usuais. Serve aos dois
    provedores porque a divergencia de nome e a regra, nao a excecao."""
    for k in ("image_base64", "image", "png_base64", "b64", "output", "b64_json"):
        v = j.get(k)
        if isinstance(v, str) and len(v) > 100:
            return v
    for lista in (j.get("images"), j.get("data")):
        if isinstance(lista, list) and lista:
            it = lista[0]
            if isinstance(it, str) and len(it) > 100:
                return it
            if isinstance(it, dict):
                for k in ("b64_json", "image_base64", "b64"):
                    if isinstance(it.get(k), str) and len(it[k]) > 100:
                        return it[k]
    return None


def bytes_de(b64: str) -> bytes:
    if "," in b64[:64] and b64.strip().startswith("data:"):
        b64 = b64.split(",", 1)[1]
    return base64.b64decode(b64)


def via_inemaimg(a, seed: int):
    """O caminho de casa: GPU local, custo zero, seed respeitado."""
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
    b64 = extrair_b64(j)
    if b64 is None:
        print(f"ERRO: nao achei o campo da imagem na resposta. Chaves: {list(j.keys())}",
              file=sys.stderr)
        sys.exit(3)
    return bytes_de(b64), f"model {j.get('model_used', a.model)}, seed {seed}"


def via_agnes(a):
    """Agnes AI — custo US$ 0. Medido em 2026-08-09: ~10s por imagem.

    DUAS diferencas que mudam o contrato, e nenhuma tem conserto por aqui:

    1. **Nao ha seed.** O determinismo do reel (mesma --seed-key -> mesma imagem)
       NAO vale neste provedor: re-renderizar o mesmo alvo da outra imagem. Isso
       e escolha do servico, nao esquecimento nosso.
    2. **O tamanho pedido e sugestao.** Pedimos 1088x736 e voltou 1248x832 (a
       proporcao foi respeitada, os pixels nao). Quem corrige e `normalizar`.

    A base ja inclui /v1 no AGNES_BASE_URL desta casa — dai o teste do sufixo em
    vez de concatenar as cegas, que rendeu um 404 /v1/v1 no primeiro teste.
    """
    base = os.environ.get("AGNES_BASE_URL", "https://api.agnesai.io/v1").rstrip("/")
    alvo = base + ("/images/generations" if base.endswith("/v1") else "/v1/images/generations")
    # AGNES_MODEL no .env aponta para o modelo de CHAT; o de imagem e outro, e
    # mandar o de chat devolve 400 "is a chat model".
    modelo = os.environ.get("AGNES_IMAGE_MODEL", "agnes-image-2.1-flash")
    body = json.dumps({
        "model": modelo, "prompt": a.prompt,
        "size": f"{a.width}x{a.height}",
        "extra_body": {"response_format": "b64_json"},
    }).encode()
    req = urllib.request.Request(alvo, data=body, headers={
        "content-type": "application/json",
        "authorization": f"Bearer {chave('AGNES_API_KEY')}",
    })
    # ~34% de 503 documentado na skill imagens-agnes: retry com backoff, senao
    # um terco dos segmentos do reel nasceria sem imagem por azar de momento.
    ultimo = None
    for tentativa in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                j = json.loads(r.read())
            b64 = extrair_b64(j)
            if b64 is None:
                print(f"ERRO agnes: sem imagem na resposta. Chaves: {list(j.keys())}",
                      file=sys.stderr)
                sys.exit(3)
            return bytes_de(b64), f"model {modelo}, SEM seed"
        except Exception as e:
            ultimo = e
            corpo = e.read()[:200].decode("utf-8", "replace") if hasattr(e, "read") else ""
            if tentativa < 3:
                time.sleep(2 ** tentativa)
                continue
            print(f"ERRO agnes: {e} {corpo}", file=sys.stderr)
            sys.exit(2)
    print(f"ERRO agnes: {ultimo}", file=sys.stderr)
    sys.exit(2)


def normalizar(png: bytes, largura: int, altura: int):
    """Devolve o PNG no tamanho EXATO pedido, cortando pelo centro o excesso.

    Corta em vez de esticar: esticar deforma rosto, e a faixa do topo do reel e
    quase sempre uma pessoa. Se ja estiver no tamanho, devolve intacto e nao
    reescreve nada.
    """
    if dimensoes(png) == (largura, altura):
        return png, ""
    origem = dimensoes(png)
    try:
        from PIL import Image
    except ImportError:
        print(f"AVISO: imagem veio {origem[0]}x{origem[1]} em vez de {largura}x{altura} "
              f"e nao ha Pillow para corrigir (pip install Pillow). preparar.py vai "
              f"regerar esta imagem toda vez.", file=sys.stderr)
        return png, " [tamanho NAO corrigido]"
    import io
    im = Image.open(io.BytesIO(png)).convert("RGB")
    escala = max(largura / im.width, altura / im.height)
    im = im.resize((max(1, round(im.width * escala)), max(1, round(im.height * escala))),
                   Image.LANCZOS)
    esq = (im.width - largura) // 2
    topo = (im.height - altura) // 2
    im = im.crop((esq, topo, esq + largura, topo + altura))
    saida = io.BytesIO()
    im.save(saida, format="PNG")
    return saida.getvalue(), f", {origem[0]}x{origem[1]} -> {largura}x{altura}"


def dimensoes(png: bytes):
    """Largura/altura do cabecalho IHDR — mesma leitura que o preparar.py faz."""
    try:
        return struct.unpack(">II", png[16:24])
    except Exception:
        return (0, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default=MODELO_PADRAO)
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
    ap.add_argument("--host", default=HOST_PADRAO)
    a = ap.parse_args()

    seed = a.seed
    if a.seed_key:
        seed = int(hashlib.sha256(a.seed_key.encode()).hexdigest()[:8], 16) % (2**31)

    for nome, valor in (("width", a.width), ("height", a.height)):
        if not (128 <= valor <= 2048) or valor % 16:
            print(f"ERRO: --{nome}={valor} invalido — use 128..2048 em passos de 16",
                  file=sys.stderr)
            sys.exit(4)

    if PROVEDOR == "inemaimg":
        png, detalhe = via_inemaimg(a, seed)
    elif PROVEDOR == "agnes":
        png, detalhe = via_agnes(a)
    else:
        print(f"ERRO: IMG_PROVEDOR={PROVEDOR} nao implementado. Hoje: inemaimg, agnes.",
              file=sys.stderr)
        sys.exit(5)

    # O tamanho EXATO nao e capricho: preparar.py compara as dimensoes do PNG
    # para decidir se reaproveita a imagem, e o empilhamento 9x16 espera a faixa
    # do topo no tamanho certo. Provedor que devolve outro tamanho (a Agnes
    # devolveu 1248x832 quando pedimos 1088x736) quebraria os dois em silencio.
    png, ajuste = normalizar(png, a.width, a.height)

    with open(a.out, "wb") as f:
        f.write(png)
    print(f"OK imagem -> {a.out} ({PROVEDOR}: {detalhe}{ajuste})")

if __name__ == "__main__":
    main()
