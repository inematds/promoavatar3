# promoavatar3 — três vídeos por público

Igual ao `promoavatar` (portão humano: o bot escreve, você gera os avatares no
HeyGen, `/aprovar C#N` libera o resto), com uma diferença: cada público rende
**três roteiros** em vez de um.

```
/promoavatar3 <assunto> [| estudio] [| alvos=jovens-alc,jovens-pro] [| versao=N] [| de=<fase>] [| sombra]
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
/promoavatar3 <assunto> | alvos=jovens-alc,jovens-aut,jovens-pro
```

## Fases

1. **texto** (escopo fluxo, pausa depois) — um arquivo por alvo em
   `textos/C<N>/<alvo>.md`, mais um `resumo-estrategico.md`. O bot manda a
   `### FALA` de cada um no chat e PARA.
2. **avatar** (por alvo, OPCIONAL) — quem gera o vídeo. Sem opção nenhuma, é
   você no estúdio. Ver "As quatro rotas de avatar" abaixo.
3. **baixar** (por alvo) — depois do `/aprovar C#N`, procura no HeyGen o vídeo
   cujo nome é exatamente `C<N>-<alvo>-v1` e baixa o MP4 — a versão COM
   legenda queimada quando o estúdio gravou com ela, a limpa quando não.
   **Prazo: 40h.** A fila de renderização do HeyGen chega a 36h, e esperar não é
   erro — o teto existe só para o vídeo que nunca foi gerado.
4. **reel** (por alvo) — monta o reel 9:16 e **entrega no canal do público**
   (`yt-pub-livesN/imports/videos`). É `kind: function`: sem agente, sem token.
   Roda um por vez (a fila `render` é a GPU).

## As quatro rotas de avatar — só UMA por fluxo

| você escreve | quem gera | de onde sai o custo |
|---|---|---|
| *(nada)* | **você**, no estúdio | assinatura |
| `\| estudio` | o bot, por SCRIPT no estúdio (Playwright) | créditos da assinatura |
| `\| creditos` | o bot, pela CLI (OAuth) | créditos da assinatura |
| `\| api` | o bot, pela chave de API | **carteira em US$** (~US$ 0,73/vídeo) |

Pedir duas é recusado na criação: juntas gerariam o mesmo vídeo duas vezes.

**`| estudio`** clona o `TEMPLATE-AVATAR` e herda cenário, avatar, voz e motor —
o vídeo sai igual ao que você gravaria à mão. Medido em 48 avatares: **~50s por
público, zero falha, zero token**. As outras duas rotas montam o vídeo SEM
template (mesmo rosto e voz, cenário diferente).

Com 36 alvos, a rota é séria: são 36 avatares em série (~31 min) e depois a fila
do HeyGen. Filtre com `| alvos=` na primeira vez.

## O nome no estúdio

Ao gerar no HeyGen, o título do vídeo tem que ser **exatamente**
`C<N>-<alvo>-v<versao>` — ex.: `C7-jovens-pro-v1`. É por esse nome que o
download casa; um caractere fora e a fase 2.5 não encontra nada.

Os sufixos são abreviados (`alc`/`aut`/`pro`, não `alcance`/`promocional`)
porque título longo já truncou no HeyGen em produção e derrubou o match.

## Confira antes de gastar

```
/promoavatar3 <assunto> | alvos=jovens-alc | sombra
```

Imprime fase × alvo × fila × tarefa e **não enfileira nada**.

## O portão continua

Nenhuma rota de avatar tira o portão: você revisa os textos e dá `/aprovar C#N`
antes de gastar. Para a esteira inteira sem parar, some `| sem-portao`.

```
/promoavatar3 <assunto> | estudio
/promoavatar3 <assunto> | estudio | sem-portao    gera E não para para aprovar
```

Confira antes com `| sombra`: a fase de avatar só aparece no plano quando a
opção dela está ligada.

## Legenda: LIGADA por default

Desde 2026-08-13 o motor deste repo legenda, com o mesmo desenho do promoavatar:
**uma palavra por vez**, caixa alta, branca com contorno preto grosso, âmbar só
na palavra-chave, colada na base da faixa do avatar. As palavras-chave saem das
`## SOBREPOSIÇÕES` do texto do público; sem elas, a legenda fica toda branca —
resultado válido, não falha.

**Cuidado com legenda DUPLA:** a do estúdio vem queimada no MP4 do avatar e não
tem remoção. Se você gravar com legenda lá E o reel legendar aqui, saem duas.
Escolher uma é desligar a outra — e desligar a do estúdio é no `TEMPLATE-AVATAR`
do HeyGen, não aqui.

Detalhes de cor, corpo e posição: `docs/legenda.md`.
