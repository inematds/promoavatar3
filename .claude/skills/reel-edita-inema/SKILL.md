---
name: reel-edita-inema
description: Monta um REEL EMPILHADO da marca INEMA (9:16, 1080x1920) a partir de vídeos 16:9 — TOPO com headline/imagem impactante, MEIO com o avatar (HeyGen), BASE com o explicativo. Quatro modos - (1) COMPOR quando você passa avatar + explicativo; (2) GERAR O EXPLICATIVO do narrado (reusa video-explicativo/hyperframes) quando você passa só o avatar; (3) GERAR VISUAIS (imagens via inemaimg + textos) a partir do avatar; (4) CAPA DE IMPACTO — modo focado em retenção/engajamento (cores livres, imagem do topo trocando por segmento + headline-choque sobreposta, legenda palavra-a-palavra), acionado por "capa/impacto/viral/retenção/gancho". Corta repetições/silêncios, legenda opcional (palavra-chave âmbar na altura do peito), SFX sutis, CTA fixo "Saiba mais no inema.club". Mídia 100% local (inemaimg/inemavox). Use quando disserem "faz o reel disso", "monta o reel empilhado", "/reel-inema", passarem um MP4 de avatar 16:9, ou um job chegar pelo worker mkivideos.
---

# reel-edita-inema — Vídeos 16:9 → reel empilhado INEMA

Você monta um **reel 9:16** de 3 faixas (topo: headline/imagem · meio: avatar · base: explicativo). O único molde fixo é esse esqueleto de 3 faixas; **o tratamento de cada faixa se adapta ao conteúdo** (leia o vídeo, proponha, não repita molde). Sua identidade visual está em `references/estilo.md` (base `#0E1116`, acento âmbar `#F5A623`, punchy/ágil).

## Regras de ouro (leia antes de tudo)
1. **Se cortar o áudio, o corte é BLOQUEADO e aprovado ANTES de qualquer animação** (as animações sincronizam a timestamps do corte). Renders limpos (HeyGen/explicativo) geralmente não precisam de corte forte.
2. **Corte por SILENCEDETECT, não por timestamps de Whisper.** Whisper (Groq) só rotula/verifica/sincroniza.
3. **Nada se entrega sem a COMPORTA DURA (`verify-cut.py` exit 0, quando houve corte) e o REVISOR PASS.**
4. **Mídia é 100% local:** imagens = `scripts/gen-imagem.py` (inemaimg/flux2-klein) · voz = `scripts/narra.sh` (inemavox, `rachel`) · SFX/música = inemavox/dlp. Nunca fal/agnes.
5. **API keys** (GROQ etc.) sempre em `~/projetos/openpcbotv2/.env` ou `~/projetos/wifi/.env` — carregar em runtime, nunca imprimir.
6. **Cada ida ao modelo relê o contexto inteiro — então agrupe.** O custo desta
   skill não é o que ela escreve (~0,5% do total): é o contexto relido a cada
   mensagem. Duas consequências práticas: **(a)** encadeie comandos de shell
   relacionados numa chamada só (`cmd1 && cmd2 && cmd3`) ou num script, em vez
   de uma chamada por comando; **(b)** frame de vídeo é o item mais caro que
   existe aqui, porque além de grande ele fica no contexto até o fim — veja a
   ordem dos três portões de QC em `03-sfx-e-qc.md` e nunca olhe com o olho o
   que o `lint` afirma de graça.

## Entrada, modo e workspace
- **Descubra o modo** pelo que foi fornecido — detalhes em `references/09-modos.md`:
  - **Modo 1 COMPOR:** avatar 16:9 **+** explicativo 16:9.
  - **Modo 2 GERAR EXPLICATIVO:** só avatar → gera o explicativo do narrado via **`video-explicativo`/`hyperframes`** e compõe.
  - **Modo 3 GERAR VISUAIS:** só avatar → gera imagens (inemaimg) + textos e compõe.
  - **Modo 4 CAPA DE IMPACTO:** só avatar, mas com foco em retenção/engajamento — topo com imagem trocando por segmento + headline-choque sobreposta (cores livres), avatar com legenda palavra-a-palavra, base com hook curto, CTA no fim. Acionado quando o input mencionar **capa / impacto / viral / retenção / gancho**, ou pela flag `capa` do bot (não muda a detecção 1-3, que segue pelas peças fornecidas).
- **Origem** das peças: caminho apontado · diretório atual · job do worker (`references/11-worker-mkivideos.md`).
- **Workspace / saída:** `~/projetos/output/reels/<slug-do-reel>/` com `edicion/` (corte, transcripts) e `motion/` (Hyperframes). **Nunca toque no bruto.** Resolução final **1080×1920**.
- Ao começar, verifique: `ffmpeg`, `bash ~/.claude/skills/reel-edita-inema/scripts/hf.sh --version`, `curl localhost:8000/health` (inemaimg), inemavox, `GROQ_API_KEY` (de openpcbot/.env), `/watch`.

> **Por que `hf.sh` e nunca `npx hyperframes` direto.** O hyperframes existe
> nesta máquina, no cache do npx (`~/.npm/_npx`), e roda offline. Duas coisas já
> quebraram job por causa de como ele é invocado, e o `hf.sh` existe para fechar
> as duas:
>
> 1. **`npx` sem `--no-install`** anuncia "package was not found and will be
>    installed", e um agente que leva a sério a regra "NÃO MEXA NA MÁQUINA" lê
>    isso como instalação proibida e **aborta o job inteiro** (A#18, job 237).
> 2. **`npx --no-install`** resolve sempre a versão LATEST do registry. Em
>    2026-08-05 o upstream publicou a `0.7.94`, o cache ia até a `0.7.92`, e o
>    `--no-install` recusou — corretíssimo, mas **cinco reels do A#25 morreram
>    no lint** por um erro que não tem nada a ver com reel.
>
> `scripts/hf.sh` chama o binário mais novo que JÁ ESTÁ no cache: nunca baixa, e
> não depende do que o registry publicou hoje. Se ele disser que não há nada em
> cache, é problema de ambiente: **reporte, não instale.**

---

## FASE 1 — (se precisar) BLOQUEAR O CORTE · `references/01-corte-e-limpeza.md`
Só quando o avatar/explicativo tiver silêncios/erros/repetição:
1. Transcreva o bruto word-level (Groq), reutilize.
2. `python3 scripts/islands.py --media <bruto> --transcript <word.json> --out islands.json` → revise KEEP/DROP (última tomada).
3. `python3 scripts/cut.py --islands islands.json --out edicion/corte-final.mp4`.
4. **COMPORTA:** re-transcreva e `python3 scripts/verify-cut.py --media edicion/corte-final.mp4 --transcript edicion/transcript-final.json` até exit 0.
5. Leia o texto corrido procurando repetições.
(Render HeyGen limpo → pule para a Fase 1.5 usando o próprio arquivo como `edicion/avatar.mp4`.)

## FASE 1.5 — LER E PROPOR TRATAMENTO · `references/04-recetas.md`
1. Veja as peças com `/watch`.
2. Escolha/combine uma receita (R1 headline-choque default … R5 número). Não repita molde.
3. Decida o **gancho do topo** (`references/08-cold-open.md`) — headline, imagem-hook, número.
4. `control.autonomia = decide-e-mostra`: **escolha a melhor, monte e mostre o resultado** (não fique perguntando a cada passo; só suba dúvida real).

## FASE 2 — PREPARAR AS PEÇAS (conforme o modo) · `references/09-modos.md`

**Comece por UMA chamada, não por dez:**
```bash
python3 ~/.claude/skills/reel-edita-inema/scripts/preparar.py \
  --avatar <avatar.mp4> --ws ~/projetos/output/reels/<slug> --alvo <publico> \
  --textos <repo>/textos/<REF>/<publico>.md [--explicativo <exp.mp4>]
```
Ele faz num passo o que eram ~14: sonda as mídias (`ffprobe`), extrai o áudio e
transcreve (reaproveita se já existir), roda `detect-repeats.py`, e **gera todas
as imagens da seção `## IMAGENS`** do texto do público — uma por segmento, com
`--seed-key "<publico>#<N>"` e `1088x704` (a faixa do topo). Escreve
`manifesto.json` com todos os caminhos: **leia o manifesto em vez de procurar
arquivo com `ls`/`grep`.**

As imagens são **decisão da fase de texto**, revisada no portão — não invente
prompt seu. Se o script avisar que não achou a seção `IMAGENS`, reporte; não
improvise. (Medido no A#19: o agente ignorou a seção e inventou os próprios
prompts, e as capas voltaram ao clichê que a seção existe para evitar.)
- **Modo 2:** gere o explicativo 16:9 chamando `video-explicativo` (ou `hyperframes`) a partir do texto narrado do avatar.
- **Modo 3:** gere as imagens (`scripts/gen-imagem.py`, seed fixo) e os rótulos; monte o painel da base.
- **Todos:** gere o **headline/imagem do topo** (`06-broll.md` / `08-cold-open.md`).

## FASE 3 — COMPOR O EMPILHADO · `references/10-composicao-empilhada.md`
- **Com movimento (entrega):** Hyperframes 1080×1920, 3 faixas de vídeo/painel + headline animado + legendas (opcionais) na **altura do peito** (`07-subtitulos.md`, palavra-chave âmbar) + CTA "Saiba mais no inema.club".
- **Rápido/preview:** `scripts/stack-9x16.sh --avatar … --explainer … --out … (--top IMG | --headline "…")`.
- Antes de renderizar: `lint`/`check` a 0 erros + `python3 scripts/lint-timeline.py motion/index.html` (nenhum beat > 4s).

## FASE 4 — SFX, QC E ENTREGA · `references/03-sfx-e-qc.md`
1. SFX sutis (`scripts/make-sfx.sh`; fontes via inemavox/dlp).
2. **QC em três portões, nesta ordem — o determinístico antes do olho:**
   **(1)** `lint` + `lint-timeline.py` + `verify-cut.py` ANTES de renderizar;
   **(2)** render `--quality standard` → `ffprobe` (duração, 1080x1920, os dois
   streams); **(3)** só então `/watch` **dirigido** (~10 frames: t=0, cada troca
   de imagem do topo, o CTA, e o que o portão 1 acusou) — sincronia,
   legibilidade, terço inferior livre → corrigir.
   Frame é o item mais caro do job: cada um entra no contexto e é relido em toda
   mensagem seguinte. Nunca extraia a série inteira duas vezes.
3. Mixe SFX (`scripts/mix-sfx.py`).
4. Render `--quality high` final. Grave em `~/projetos/output/reels/<slug>/`. Se veio do worker, entregue com `--enviar` (Telegram) — `references/11-worker-mkivideos.md`.

## FASE 5 — REVISOR (subagente independente, OBRIGATÓRIO) · `references/05-revisor.md`
Spawn de um subagente (tool `Agent`) que NÃO montou o reel: re-transcreve o ÁUDIO DO RENDER FINAL, lê inteiro procurando repetições, roda `verify-cut.py` e `lint-timeline.py --json` sobre o render. Só entrega se **PASS** e sem blockers.

## Regras que não se negociam
- Brutos intactos; output em `edicion/` e `motion/` dentro de `~/projetos/output/reels/<slug>/`.
- Esqueleto de 3 faixas fixo; tratamento adapta ao conteúdo.
- Áudio mestre = fala do avatar; explicativo em loop até a fala acabar.
- TEXTO/LEGENDAS/rótulos na **ALTURA DO PEITO**, nunca no terço inferior.
- Beat visual ≤4s (`lint-timeline.py`). Zero repetições/silêncios no corpo. Última tomada.
- **CTA fixo** "Saiba mais no inema.club" no fim de todo reel.
- Que NÃO pareça feito por IA (sem pílulas "PROBLEMA/SOLUÇÃO", sem template repetido).
- Determinismo Hyperframes: sem `Math.random()`/`Date.now()`; `repeat` finito; timelines `paused`. inemaimg com seed fixo.
