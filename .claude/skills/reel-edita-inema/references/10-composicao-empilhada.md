# 10-composicao-empilhada.md — Montar o reel de 3 faixas (1080×1920)

Layout fixo (o único molde fixo da skill; o resto adapta ao conteúdo):

```
┌────────────────────────────┐  y=0
│  TOPO ~704px               │  headline grande OU imagem-com-texto (o gancho)
├────────────────────────────┤  y=704
│  MEIO ~608px               │  AVATAR 16:9 -> 1080x608
├────────────────────────────┤  y=1312
│  BASE ~608px               │  EXPLICATIVO 16:9 -> 1080x608
└────────────────────────────┘  y=1920
```

Áudio mestre = fala do **avatar**. O explicativo entra em **loop** até a fala terminar (não estica o reel).

## Dois caminhos

### A) RÁPIDO / determinístico — `scripts/stack-9x16.sh` (ffmpeg)
Para quando o topo é uma **imagem pronta** ou um **headline estático**:
```bash
scripts/stack-9x16.sh --avatar edicion/avatar.mp4 --explainer edicion/explicativo.mp4 \
  --out reel.mp4 --top motion/capa-topo.png
# ou headline em cartao solido:
scripts/stack-9x16.sh --avatar ... --explainer ... --out reel.mp4 --headline "A VERDADE SOBRE X"
```
Bom para primeira versão/preview. Sem animação.

### B) COM MOVIMENTO — Hyperframes (caminho de entrega)
Quando o topo tem **headline animado**, **legendas** sincronizadas ou o Modo 3 (painel de imagens na base):
1. `bash ~/.claude/skills/reel-edita-inema/scripts/hf.sh init` numa pasta `motion/`, canvas **1080×1920**.
2. Três camadas de vídeo/painel nas bandas (use os `data-*` de tempo do motor — `02-motion-graphics.md`):
   - **topo:** headline animado (entra o gancho nos 1-3s) — ou `<img>` da imagem gerada (`gen-imagem.py`).
   - **meio:** `<video>` do avatar (recorte 1080×608, `object-fit: cover`).
   - **base:** `<video>` do explicativo, OU painel de imagens (Modo 3).
3. Legendas na **altura do peito** sobre a faixa do meio (`07-subtitulos.md`, palavra-chave em `#F5A623`).
4. **CTA** "Saiba mais no inema.club" nos últimos ~1.5s.
5. `lint`/`check` a 0 erros + `python3 scripts/lint-timeline.py motion/index.html` (nenhum beat > 4s) antes de renderizar.
6. Render `--quality standard` → QC com `/watch` → corrige → `--quality high`.

> Determinismo Hyperframes: sem `Math.random()`/`Date.now()`, `repeat` finito, timelines `paused`.

## Notas de recorte do 16:9
- `scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608` centraliza e corta o 16:9 na faixa. Se o avatar HeyGen tiver o rosto muito à esquerda/direita, ajustar o `crop` (offset x) para manter o rosto centralizado.

## Modo 4 — capa de impacto (topo com imagem trocando + headline sobreposta)
Mesmo esqueleto de 3 faixas, mas a faixa do TOPO vira uma sequência de **cards** (um por segmento de fala, `09-modos.md`): imagem cheia (`object-fit: cover`) com a headline-choque como camada de texto POR CIMA (não embutida no PNG — texto legível/animável exige camada Hyperframes). Ao trocar de segmento, troque a imagem do topo com uma transição curta (crossfade/whoosh) sincronizada à fala — é o motor de re-hook do modo, então cada troca é um beat visual (conta para a regra dos ≤4s de `03-sfx-e-qc.md`). A faixa do MEIO leva legenda **palavra-a-palavra** (ver nota em `07-subtitulos.md`), e a faixa da BASE é o hook curto em texto (não painel de imagens do Modo 3).

**A BASE é um PAINEL, não uma legenda.** Conferido no reel 229 (2026-08-03): a
faixa de 608px estava ~500px vazia, com uma linha única de texto colada perto do
rodapé e um tracinho solto no meio — leitura de legenda de vídeo, não de bloco
de design, enquanto o topo (imagem sangrando + manchete grande em duas linhas)
parecia pôster. A base é **1/3 da tela**; entregar ela vazia é jogar fora um
terço do reel. Regras:

- **Ocupe a faixa.** O bloco de texto se distribui na altura da base, centrado —
  nunca ancorado no rodapé como legenda.
- **Duas linhas, tipografia grande**, no mesmo peso visual da manchete do topo.
  Se o texto não enche duas linhas, ele está longo demais para uma e curto
  demais para o espaço: reescreva o hook, não diminua a fonte.
- **Dê corpo ao bloco:** caixa com fundo (sólido ou gradiente), faixa de cor ou
  imagem esmaecida atrás. O topo tem a imagem para dar peso; a base precisa do
  equivalente, senão o texto flutua.
- **O acento é o MESMO do card do topo daquele segmento.** No 229 o topo
  destacava em âmbar e a base em ciano — dois acentos brigando no mesmo frame.
  "Cores livres" vale para escolher a paleta do card, não para divergir dentro
  do mesmo quadro.
- O traço/divisor, se houver, faz parte do bloco (junto do texto), não solto no
  meio do vazio. Cores livres — decida a paleta do card pelo conteúdo, não pelo `estilo.md`. **O primeiro card (imagem do topo + headline) e o hook da base já entram 100% visíveis no `t=0`** — o frame 0 é a capa que aparece na página, então nunca começa com topo/base vazios (ver a REGRA DURA em `08-cold-open.md`); a troca de cards começa a partir do segundo segmento, não do preto.
