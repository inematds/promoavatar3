# Legenda do reel

Legenda palavra a palavra na faixa do avatar, **ligada por default**.

> **Para quem for implementar aqui:** este desenho foi fechado E IMPLEMENTADO no
> repo `promoavatar`. Copie de lá: `scripts/legendas.py`, o bloco de legenda do
> `montar.py`, o nó `faixas.meio.legenda` do template, o `--sem-legenda` do
> `preparar.py`/`montar-reel.py` e `tests/test_legendas.py`. As decisões de
> produto estão fechadas — não as reabra. Mas as referências `arquivo:linha`
> deste doc são do `promoavatar` e **precisam ser reconferidas aqui**: este repo
> virou autônomo (motor, layouts e skill próprios, `fda1c72`) e não há garantia
> de que as linhas coincidam. Se alguma diferença deste repo mudar o desenho,
> avise antes de improvisar.

**Estado neste repo: nada implementado ainda.** No `promoavatar` o motor está
pronto e verificado (`legendas.py`, camada no `montar.py`, nó no template,
`--sem-legenda` em `preparar.py` e `montar-reel.py`); lá falta só a peça do
`inemaccbot` — a flag `| legenda=nao` —, que é a única que exige restart do bot.
Ver "Ordem de aplicação".

## Decisões

| decisão | escolha |
|---|---|
| formato | **uma palavra por vez**, caixa alta, sem fundo |
| tipografia | Montserrat Black, contorno preto grosso |
| cor base | branca |
| cor de acento | âmbar, **só na palavra-chave** |
| origem das keywords | derivadas das `## SOBREPOSIÇÕES` do `.md` do público |
| posição | colada na base da faixa do avatar (`#meio`), 28px de respiro |
| default | **ligada**; desliga com `\| legenda=nao` |

O que foi descartado, e por quê:

- **karaokê (toda palavra acende âmbar).** Deixa o âmbar sem função: ele já é o
  acento da headline no topo e da `.kw` no painel de baixo. Acento em toda parte
  é acento em lugar nenhum.
- **fundo sólido ou tarja escura.** O reel já empilha headline no topo e painel
  na base; uma legenda com caixa vira um terceiro bloco pesado no meio.
- **fallback "destaca a palavra mais longa".** O `captions.py` original faz isso
  para garantir um acento por bloco de 3 palavras. Em formato de uma palavra a
  regra degenera para "tudo âmbar". **Sem keyword, a legenda fica toda branca —
  isso é um resultado válido, não uma falha.**

## Onde mudar cor e formato

Tudo num nó só, `legenda`, em `templates/empilhado-capa.json`, dentro de
`faixas.meio` — ao lado das coordenadas da faixa do avatar:

```jsonc
"legenda": {
  "fonte": "Montserrat Black, Inter, system-ui, sans-serif",
  "fonte_arquivo": "~/.local/share/fonts/Montserrat-Black.ttf",
  "tamanho": 86, "peso": 900,
  "contorno": "#000000", "contorno_px": 8,
  "respiro": 28              // px acima da base da faixa do avatar
}
```

As **cores não estão aí de propósito**: a palavra comum usa `cores.texto` e a
palavra-chave usa `cores.acento` — as mesmas do reel inteiro, no mesmo template.
Mudar o acento muda headline, hook e legenda juntos, que é o comportamento
certo: são a mesma marca. `scripts/montar.py` só lê e injeta no CSS; nenhuma cor
de legenda pode estar escrita nele — se estiver, é bug.

### `fonte_arquivo` não é enfeite

Descoberto no primeiro render: o lint acusa `font_family_without_font_face` e o
renderer **cai calado numa fonte genérica** para qualquer família que ele não
resolva sozinho — Montserrat Black é uma delas. O `montar.py` copia o arquivo
apontado por `fonte_arquivo` para `motion/fonts/` e emite o `@font-face`. Sem
essa chave a legenda sai com a tipografia errada e **nada falha** — só fica
feio, e ninguém percebe até assistir.

### Templates com avatar em PiP

Quando o template põe o avatar como selo flutuante (`meio.forma == "pip"`,
468x264 sobre a imagem), a legenda é **ignorada** com aviso: naquele tamanho ela
sairia ilegível e taparia o próprio rosto.

## Como funciona

```
edicion/transcript.json ──┐
                          ├──> scripts/legendas.py ──> edicion/legendas.json ──> montar.py ──> HTML ──> HyperFrames
textos/<A#N>/<publico>.md ┘
```

**Entrada.** `preparar.py:288` já grava `<ws>/edicion/transcript.json` (Groq
`whisper-large-v3-turbo`, `timestamp_granularities=word`), no formato
`{"words": [{word, start, end}]}`. Não há ASR novo: o timing por palavra que a
legenda precisa já é produzido hoje.

**`scripts/legendas.py`** (novo, portado do `captions.py` da skill global —
**não** chamar a cópia global, ver `SKILL.md:8-22`: foi o que quebrou o A#23):

1. lê o transcript, descarta palavra sem `start`;
2. lê as `## SOBREPOSIÇÕES` do `.md` do público e monta o conjunto de keywords —
   normaliza com a mesma regra do original (minúscula, sem acento, sem
   pontuação), descarta palavras curtas e de função (artigo, preposição,
   conjunção);
3. para cada palavra: caixa alta, pontuação removida (`ANOS,` → `ANOS`);
4. `dur` de cada palavra vai até o `start` da seguinte — **sem buraco**, para a
   legenda não piscar entre palavras;
5. emite `<ws>/edicion/legendas.json`: `[{start, dur, palavra, kw}]`.

**`montar.py`** emite a camada dentro do bloco `#meio`, uma palavra por
elemento, com `data-start`/`data-duration` como os demais elementos da timeline.

## Nomenclatura obrigatória dos seletores

Container `#captions`, cada palavra `#cb<N>`. Isto **não é cosmético**:
`lint-timeline.py:107-113` reconhece esse padrão e exclui legendas da contagem
de ritmo. Com outro nome, cada palavra conta como beat visual e o portão 1 do
`montar-reel.py:172` reprova o reel com dezenas de beats falsos.

## A flag

Hoje `| legenda` é parseado e **rejeitado** neste fluxo
(`inemaccbot/src/gateway/comandos-fluxo.ts:182-186`), porque a fase de reel é
`kind: function` e o pipeline não gerava legenda. Muda:

1. `comandos-fluxo.ts:282` — `let legenda = false` vira `true`;
2. `comandos-fluxo.ts:182-186` — remover o bloco de rejeição;
3. `comandos-fluxo.ts:336` — incluir `legenda` na alternação de `campo=valor`,
   senão `| legenda=nao` não parseia. **Incluir `estudio` na mesma passada**: ele
   está em `CAMPOS`/`BANDEIRAS` mas falta nessa linha, e por isso
   `| estudio=nao` não funciona hoje. É o mesmo defeito;
4. a opção desce até a tarefa `reel.montar` e vira `--sem-legenda` no
   `montar-reel.py`.

## Casos-limite

| situação | comportamento |
|---|---|
| sem `transcript.json` (rodou `--sem-transcricao`) | reel sem legenda, com aviso — **não** é erro |
| palavra sem `start` no transcript | descartada |
| nenhuma keyword casa | legenda toda branca |
| avatar já veio com legenda queimada do estúdio | saem **duas**, sem remédio — ver abaixo |

## Aviso: legenda do estúdio

Com o default ligado, **não ligue legenda no estúdio do HeyGen**. A legenda do
estúdio vem queimada nos pixels do MP4 e sobrevive ao reel inteiro; não há
remoção, máscara nem inpaint no pipeline. Ligar as duas é ficar com duas.

E não dá para recuperá-la como texto: a API não entrega legenda de vídeo já
renderizado — medido em 2026-08-07, ver `README.md`.

## Verificação (feita no `promoavatar` — repetir aqui)

- `tests/test_legendas.py` — 19 testes sobre `legendas.py`: keywords só das
  SOBREPOSIÇÕES, rótulos e palavras de função fora, caixa alta sem pontuação,
  ausência de lacuna entre palavras, `.md` sem SOBREPOSIÇÕES não quebra. Rode
  com `python3 -m pytest tests/ -q`;
- **três transcripts reais** (a16-criadores, c15-jovens, o-google-jovens): 104 a
  129 palavras, **zero lacuna ou sobreposição**. O primeiro rodou com 1
  sobreposição de 10ms, causada por um piso de duração de 0,05s em cima de uma
  palavra de 40ms do ASR — o piso saiu, e o teste
  `test_palavra_curtissima_nao_invade_a_proxima` guarda a regressão;
- **lint de ritmo:** 20 beats com legenda e 20 sem, no mesmo reel. As 234
  operações de legenda são ignoradas, como a nomenclatura `#cb<N>` promete;
- **render draft de ponta a ponta** (A34-pessoacomum, 34,8s, 117 palavras): a
  legenda aparece palavra a palavra, branca, com `HORAS` em âmbar, na base da
  faixa do avatar, sem invadir o painel;
- **os dois caminhos do `preparar.py`:** com legenda (117 palavras no HTML,
  `@font-face` presente) e `--sem-legenda` (zero).

## Verificação (o que ninguém fez ainda, em nenhum repo)

- **`legendas.py` sobre o `transcript.json` real do A#35:** contagem de palavras
  bate, nenhuma lacuna temporal entre palavras consecutivas, e as marcadas `kw`
  correspondem às SOBREPOSIÇÕES;
- **reel de ponta a ponta** em `--qualidade draft` + `qc-frames.py`, para ver a
  legenda no quadro montado pelo HyperFrames.

O segundo teste não é opcional. Os arquivos de amostra em
`output/promoavatar-A35/demo-legenda/` foram queimados com ffmpeg/libass só para
escolher a aparência — **o pipeline não renderiza assim**, e nenhuma linha
daquele mock entra no código.
