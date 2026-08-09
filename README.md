# promoavatar3

Três vídeos por público, em vez de um. O bot escreve os textos e PARA;
`/aprovar C#N` libera avatar, download e reel.

**Este projeto é AUTÔNOMO** (desde 2026-08-06). Ele já foi descrito como "igual
ao promoavatar": não é mais. O motor do reel (`scripts/`), os layouts
(`templates/`) e a skill de edição vivem AQUI, e os dois sistemas evoluem
separados — o promoavatar está congelado. Mexer nos alvos, prompts ou templates
de lá **não afeta nada aqui**.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/promoavatar3/guia/**

Referência: `C#7`. O `promoavatar` é `A#`, o `promoclub` é `P#` — o bot recusa
referência com prefixo trocado.

Uso, opções e a tabela dos três tipos: `HELP.md` (ou `/promoavatar3 help` no
chat). As decisões de engenharia e o porquê de cada uma: `CLAUDE.md`.

## O que é deste repo, e o que é do bot

A divisão vale para os dois lados e evita a documentação em dobro que envelhece
desencontrada:

| aqui (domínio) | no [`inemaccbot`](https://github.com/inematds/inemaccbot) (motor) |
|---|---|
| **quem** é o público (`alvos` no `flow.json`), o gatilho e o fecho de cada um | como uma fila funciona, lease, retomada, portão |
| para **qual canal** vai (`lives2`, `lives22`…) — pelo NOME, nunca o caminho | onde esse nome mora no disco |
| o **prompt** da fase de texto (`prompts/`) | como um prompt de fase é executado |
| o **template** de reel (`templates/`) e o motor (`scripts/`) | como a fase `reel.montar` dispara o motor |
| o `TEMPLATE-AVATAR` e o motor de voz (`engine`, `voice_id`) | as rotas `\| api`, `\| creditos`, `\| estudio` e de que bolso cada uma sai → [`docs/rotas-de-avatar.md`](https://github.com/inematds/inemaccbot/blob/master/docs/rotas-de-avatar.md) |
| o CTA (`cta/cta-9x16.mp4`) | instalação, `.env`, systemd, comandos do chat |

Regra curta: **se muda com o público, é daqui; se muda com a máquina, é de lá.**

## Onde mudar o quê

| quero mudar | arquivo |
|---|---|
| público, gatilho, fecho, canal | `flow.json` → `alvos` |
| como o texto é escrito (as 3 versões, as `## IMAGENS`) | `prompts/fase1-3versoes.md` |
| avatar, voz, motor, template do estúdio | `flow.json` → `avatar_id`, `voice_id`, `engine`, `template` |
| o layout do reel | `templates/` (e `template` na raiz do `flow.json`) |
| o motor do reel | `scripts/montar-reel.py` e vizinhos |
| a ajuda que o chat responde | `HELP.md` |
| o vídeo de CTA | `cta/cta-9x16.mp4` (versionado desde 2026-08-08) |

**Nada aqui tem caminho de máquina.** O que dependia (`localhost:8000` do
inemaimg, a chave do Groq) virou variável de ambiente com o mesmo default de
antes — `INEMAIMG_HOST`, `INEMAIMG_MODEL`, `GROQ_ENV_PATH`, documentadas no
`.env.example` do bot. O teste que pega regressão é
`git grep /home/ -- .` dar zero em arquivo versionado.

## As imagens: aqui GPU, fora API

`scripts/gen-imagem.py` fala com mais de um provedor. **O default não mudou** —
quem roda em casa continua na GPU local, sem configurar nada:

| `IMG_PROVEDOR` | quem gera | custo | seed |
|---|---|---|---|
| `inemaimg` *(default)* | a GPU local, `flux2-klein` | zero | **respeitado** |
| `agnes` | API da Agnes AI, `agnes-image-2.1-flash` | **US$ 0**, ~10 s/imagem | **não existe** |
| `kie`, `fal` | — | — | **não implementados**: o script recusa em vez de fingir |

Na VPS: `IMG_PROVEDOR=agnes` e a chave em `IMG_ENV_PATH` (arquivo com
`AGNES_API_KEY=`, `chmod 600`) — ou `AGNES_API_KEY` direto no ambiente.

**Duas coisas mudam ao sair da GPU, e nenhuma tem conserto aqui:**

1. **O determinismo cai.** A Agnes não aceita seed, então a mesma `--seed-key`
   gera imagem diferente a cada render. Só o inemaimg cumpre "mesmo reel, mesma
   imagem" — inclusive por túnel (`ssh -R 8000:localhost:8000 <vps>`), que é a
   opção a considerar se a reprodutibilidade importar mais que a independência.
2. **O tamanho pedido vira sugestão.** Medido: pedimos 1088x736 e voltou
   1248x832. O adaptador **normaliza** cortando pelo centro (nunca esticando,
   que deformaria rosto) — sem isso o `preparar.py` regeraria a imagem toda vez,
   porque ele compara dimensão para decidir reaproveitar.

Detalhe por provedor, com o que foi medido em cada um:
[`inemaimg/docs/prompt-por-provedor.md`](https://github.com/inematds/inemaimg/blob/main/docs/prompt-por-provedor.md).

## Os três tipos, e por que não são três variações

| sufixo | tipo | duração | o que o público faz depois |
|---|---|---|---|
| `-alc` | alcance | 25–40s | compartilha, comenta |
| `-aut` | autoridade | 35–60s | salva, segue |
| `-pro` | promocional | 30–45s | clica |

Não é o mesmo roteiro com três ganchos. São três FUNÇÕES diferentes, e o que as
separa é o fecho: o `-alc` não tem CTA comercial nenhum (nem falado, nem no
reel), o `-aut` toca a marca de leve, o `-pro` converte. Um vídeo que tenta ser
os três ao mesmo tempo é promocional com abertura simpática — e é o de menor
alcance dos três.

Ordem de publicação recomendada: alcance → autoridade → promocional.

## O prompt do texto (`prompts/fase1-3versoes.md`)

Nesta ordem: os alvos e o que cada sufixo significa · CONTEXTO FIXO (Nei e Tiza
como gestores) · NÃO MEXA NA MÁQUINA · PASSO ZERO (tese central, motivo para
assistir, elemento demonstrável) · **assunto que é debate** · as 14 regras de
escrita · o que muda em cada tipo · o contrato de saída.

Variáveis que o bot injeta: `{{input}}` (o assunto), `{{publicos}}` (os alvos
REAIS do fluxo, já filtrados por `| alvos=`), `{{pasta}}` (onde gravar,
absoluto), `{{ref}}`, `{{saida}}`.

### Assunto que é DEBATE: o prompt crava uma posição

Assunto que chega como pergunta em aberto ("isso é bom ou ruim?", "o que você
acha?") tinha um resultado previsível: o agente explicava os dois lados e
fechava em "o importante é se preparar". Correto e morno — ninguém comenta com
equilibrista.

A causa não era falta de talento: são as regras 9 e 10 (não invente dado, não
invente urgência) fazendo o agente recuar até o meio-termo, que é o único lugar
onde ele tem certeza de não estar afirmando nada.

Aqui isso custava mais caro que no `promoavatar`: **sem uma posição na mesa, os
três tipos colapsam num só.** Os três viram o mesmo resumo equilibrado com três
embalagens, e o `-alc` fica impossível — "opinião contrária", o formato que mais
engaja em tema polêmico, não existe sem alguém tomando um lado.

Então o prompt manda tomar um lado e **escrever no `resumo-estrategico.md` qual
posição cravou e por quê**. Com a posição definida os três se separam de
verdade: o `-alc` defende, o `-aut` explica a mecânica que sustenta, o `-pro`
transforma em consequência prática. Isso não afrouxa as regras 9 e 10: opinião é
permitida, fato inventado não.

**A posição que você mandar vence a dele.** Se você escreve a sua no assunto, ele
usa a sua; o bloco só existe para quando você não escreveu. Escrever a sua
continua sendo o melhor caminho — junto com um fato concreto (para a linha PROVA
não ficar vazia) e a pergunta que você quer nos comentários.

Como o resumo diz a posição escolhida, você discorda dela **no portão**, antes de
gerar avatar nenhum. Aqui isso vale três renders manuais por público, não um.

## Legenda: quem decide é o estúdio

A fase `baixar` prefere o `video_url_caption` (o MP4 com a legenda **queimada**)
quando a HeyGen o devolve preenchido, e cai no `video_url` limpo quando não vem
(`escolherUrl`, `inemaccbot/src/fila/tarefas/heygen.ts`). Gravou com legenda no
estúdio, o reel sai com ela; gravou sem, sai sem — o bot não escolhe.

Duas consequências que nenhum código desfaz: legenda queimada vem enquadrada
para 16:9 e no reel 9:16 pode ser cortada ou colidir com a base; e se o reel
também for montado com `| legenda`, saem **duas**. Ligar uma é decidir desligar
a outra. Aqui isso vale por três vídeos por público, não um.

## O que roda sem modelo

Das quatro fases, **só a de texto usa LLM**. As outras três são função:

| fase | como roda |
|---|---|
| texto | agente — escreve os 3 roteiros por público |
| avatar (`\| estudio`) | **script** Playwright no estúdio do HeyGen (~50s/público) |
| baixar | função — acha pelo TÍTULO e baixa |
| reel | **função** — `scripts/montar-reel.py`, e entrega no canal |

Medido no promoavatar antes do porte: o custo por vídeo caiu de **US$ 3,09 para
US$ 0,18** quando avatar e reel deixaram de ser agente. O detalhamento está em
`inemaccbot/docs/custo-por-fase-a19-a29.md`.

## O motor do reel mora aqui

`scripts/montar-reel.py` encadeia: preparar → portão 1 (lint + ritmo) → render →
revisor → CTA → QC. Nomes fixos (`motion/corpo.mp4`, `final/reel.mp4`,
`qc/mosaico.png`), exit 3 quando um portão reprova.

**O portão de entrada é a seção `## IMAGENS` do texto** (regra 11b do prompt da
fase 1): uma linha por SEGMENTO da fala, com `headline:` e `hook:`. Sem ela o
`preparar.py` sai com exit 3 e o reel não é montado — não é preferência de
estilo, é o que impede o reel de sair com painel vazio ou headline inventada.

Os layouts estão em `templates/` e o padrão é o `template` da raiz do
`flow.json`; um alvo pode cravar o seu.

## Atenção: tudo aqui é congelado na criação

`flow.json` e o prompt são copiados para dentro do fluxo no momento em que ele
nasce. Editar aqui só afeta fluxos NOVOS — um fluxo em andamento não muda de
regra no meio. Para valer no que já existe, crie outro.
