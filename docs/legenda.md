# Legenda do reel

Legenda palavra a palavra na faixa do avatar, **ligada por default**. Este
documento é o desenho aprovado; enquanto não houver código, ele descreve o que
será construído, não o que já existe.

> **Para quem for implementar aqui:** este desenho foi fechado no repo
> `promoavatar` e copiado para cá para ser aplicado. As decisões de produto
> (formato, cores, origem das keywords, default da flag) estão fechadas — não
> as reabra. Já as **referências `arquivo:linha` foram levantadas no
> `promoavatar` e precisam ser reconferidas neste repo antes de editar**: os
> scripts têm os mesmos nomes, mas não há garantia de que as linhas coincidam.
> Confira também se as diferenças deste repo (motor, layouts e skill próprios,
> commit `fda1c72`) mudam algum ponto do desenho — se mudarem, avise antes de
> improvisar.

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

Tudo num nó só, `legenda`, em `templates/empilhado-capa.json` — ao lado das
coordenadas das três faixas, que já moram lá:

```jsonc
"legenda": {
  "fonte": "Montserrat Black",
  "corpo": 86,
  "cor": "#FFFFFF",          // palavra comum
  "acento": "#F5A623",       // palavra-chave
  "contorno": "#000000",
  "contorno_px": 8,
  "respiro": 28              // px acima da base da faixa do avatar
}
```

`scripts/montar.py` **lê** esses valores e injeta no CSS. Nenhuma cor de legenda
pode ser escrita direto no `montar.py` — se estiver lá, é bug.

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

## Ordem de aplicação (importa)

A peça da flag **não mora neste repo** — mora no `inemaccbot`, e mexer nela
**exige reiniciar o bot**. Reiniciar com job na fila derruba trabalho em curso.
Por isso:

1. **Primeiro, tudo que é deste repo:** `scripts/legendas.py`, a camada de
   legenda no `montar.py`, o nó `legenda` no template, o `--sem-legenda` no
   `montar-reel.py`. **Nada disso exige restart** — os scripts são lidos a cada
   job, então dá para implementar e testar por linha de comando com o bot no ar
   e a fila cheia.
2. **Só depois, e só com a fila vazia:** a flag no `inemaccbot`
   (`comandos-fluxo.ts:282`, `:182-186`, `:336`) e o restart.

Feito nessa ordem, o motor já está pronto e verificado quando o default liga; o
restart vira o último passo, não um risco no meio do caminho.

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

## Verificação

- **`legendas.py` sobre o `transcript.json` real do A#35:** contagem de palavras
  bate, nenhuma lacuna temporal entre palavras consecutivas, e as marcadas `kw`
  correspondem às SOBREPOSIÇÕES;
- **reel de ponta a ponta** em `--qualidade draft` + `qc-frames.py`, para ver a
  legenda no quadro montado pelo HyperFrames.

O segundo teste não é opcional. Os arquivos de amostra em
`output/promoavatar-A35/demo-legenda/` foram queimados com ffmpeg/libass só para
escolher a aparência — **o pipeline não renderiza assim**, e nenhuma linha
daquele mock entra no código.
