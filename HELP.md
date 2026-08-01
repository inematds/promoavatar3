# promoavatar2 — três vídeos por público

Igual ao `promoavatar` (portão humano: o bot escreve, você gera os avatares no
HeyGen, `/aprovar C#N` libera o resto), com uma diferença: cada público rende
**três roteiros** em vez de um.

```
/promoavatar2 <assunto> [| alvos=jovens-alc,jovens-pro] [| legenda] [| versao=N] [| de=<fase>] [| sombra]
```

Referência: `C#7` (o `promoavatar` usa `A#`, o `promoclub` usa `P#`). O bot
recusa referência com prefixo trocado.

## Os três tipos

| sufixo | tipo | duração | objetivo | CTA |
|---|---|---|---|---|
| `-alc` | alcance | 25–40s | interromper a rolagem, ser compartilhado | comentar / compartilhar — **nunca comercial** |
| `-aut` | autoridade | 35–60s | ensinar algo concreto, ser salvo | salvar / seguir / testar |
| `-pro` | promocional | 30–45s | ligar dor a solução | um só, para o inema.club |

Ordem de publicação recomendada: alcance → autoridade → promocional.

## Alvos

São 36: os 12 públicos do `promoavatar` × 3 tipos, escritos `<publico>-<tipo>`
(`jovens-alc`, `mulheres-pro`, `40mais-aut`…). O canal e o gatilho são os do
público — os três tipos de um público dividem os dois, e caem no mesmo `livesN`.

**Os 36 estão declarados, mas rodar os 36 de uma vez são 36 avatares gerados na
mão.** O normal é filtrar:

```
/promoavatar2 <assunto> | alvos=jovens-alc,jovens-aut,jovens-pro
```

## Fases

1. **texto** (escopo fluxo, pausa depois) — um arquivo por alvo em
   `textos/C<N>/<alvo>.md`, mais um `resumo-estrategico.md`. O bot manda a
   `### FALA` de cada um no chat e PARA.
2. **baixar** (por alvo) — depois do `/aprovar C#N`, procura no HeyGen o vídeo
   cujo nome é exatamente `C<N>-<alvo>-v1` e baixa o MP4 **sem legenda**.
3. **reel** (por alvo) — monta o reel 9:16 no canal do público.

## O nome no estúdio

Ao gerar no HeyGen, o título do vídeo tem que ser **exatamente**
`C<N>-<alvo>-v<versao>` — ex.: `C7-jovens-pro-v1`. É por esse nome que o
download casa; um caractere fora e a fase 2.5 não encontra nada.

Os sufixos são abreviados (`alc`/`aut`/`pro`, não `alcance`/`promocional`)
porque título longo já truncou no HeyGen em produção e derrubou o match.

## Confira antes de gastar

```
/promoavatar2 <assunto> | alvos=jovens-alc | sombra
```

Imprime fase × alvo × fila × tarefa e **não enfileira nada**.
