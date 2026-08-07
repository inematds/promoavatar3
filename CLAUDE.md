# promoavatar3

Cada público rende **três roteiros, não um** — e o portão humano continua (o bot
escreve os textos e PARA; `/aprovar C#N` libera avatar, download e reel).

**Não é o promoavatar com uma opção a mais, e desde 2026-08-06 não é nem irmão:
é um sistema separado.** Motor do reel (`scripts/`), layouts (`templates/`) e a
skill de edição estão AQUI. O `promoavatar` está congelado por decisão do dono —
mexer nos alvos, prompts ou templates de lá não afeta nada aqui, e o inverso
também vale.

A cópia do motor foi deliberada. A primeira tentativa (2026-08-06) foi
compartilhar o do promoavatar via `motor_repo` no `flow.json`, justamente para
não duplicar código que envelhece — foi cópia velha de `preparar.py` que
produziu o `template: None` do A#23. A decisão mudou quando o promoavatar foi
congelado: com a origem parada, a cópia não diverge — ela vira a única versão
viva.

Referência: `C#7`. O `promoavatar` é `A#`, o `promoclub` é `P#`.

## Por que é um repo separado, e não uma opção do promoavatar

O motor (`~/projetos/inemaccbot`) resolve `flow.json` na raiz do repo de domínio
(`src/dominio/registry-fluxos.ts`), e o `prompt` é campo fixo da fase dentro da
definição congelada. **Um repo = um fluxo.** Uma flag `--modo=3versoes` exigiria
mudar o bot para atender um domínio — o inverso da regra do README dele.

## A fase 3 não usa mais agente (2026-08-06)

`reel` é `kind: function` / `reel.montar`: o bot chama
`scripts/montar-reel.py` e vigia o arquivo. Saíram o `perfil` (não há modelo a
escolher) e a `entrega` — que era prosa para o agente e dizia `"público
{canal}"`, o mesmo erro que fez o agente do A#25 procurar `textos/A25/lives2.md`.
Canal é destino de publicação, não identidade de público.

O que a função ganhou junto: entrega no canal (`yt-pub-livesN/imports/videos`)
como parte da tarefa, prazo explícito de 6h (36 alvos em série a ~165s são ~100
min, e o default interno de 3h não daria margem a um requeue), e o `--flow`
deste domínio no comando — sem ele o `preparar.py` derivaria o repo da pasta-pai
do script.

**O portão de entrada do motor é a seção `## IMAGENS`** (regra 11b do prompt da
fase 1), com `headline:` e `hook:` por segmento. Sem ela o `preparar.py` sai com
exit 3 — e todos os 36 públicos falhariam no primeiro job.

## Por que o alvo é `<publico>-<tipo>` e não `<tipo>`

A fase 3 montava a headline a partir de `{gatilho}` e interpolava o público. Com
o alvo sendo só o tipo, o reel receberia "público alcance" e um gatilho com
objetivo editorial no lugar da dor do público — e a fase 3 rodava sem revisão
humana, então ninguém pegaria. (Hoje a fase é função e não interpola nada, mas a
chave composta segue certa: é ela que dá título distinto no estúdio e o canal
por público.)

Com a chave composta, `{canal}` e `{gatilho}` mantêm o sentido e o título do
estúdio (`tituloEstudio` = `<prefixo><id>-<alvo>-v<versao>`, literal da chave do
alvo) sai distinto por versão de graça.

Sufixos curtos (`alc`/`aut`/`pro`) porque título longo truncou no HeyGen em
produção e quebrou o match do download.

## O campo `fecho` (não apague)

`{cta}` é resolvido **por fluxo**, não por alvo: `comandos-fluxo.ts:107` troca
`{cta}` na definição inteira no momento da criação, a partir de
`<repo>/cta/cta-9x16.mp4`. Sem contramedida, o CTA comercial entraria também nos
12 alvos `-alc`, que por definição não têm CTA comercial — e a fase 3 roda sem
revisão humana, então ninguém pegaria.

Por isso cada alvo carrega um `fecho`, que é resolvido POR ALVO
(`entrada-fase.ts:130`, a partir dos campos do alvo) e manda no `{cta}`: o
`-alc` proíbe, o `-aut` permite de leve, o `-pro` usa inteiro.

Se você acrescentar um alvo, ele precisa de `canal`, `gatilho` **e** `fecho`.

## Onde vive o quê

- `flow.json` — os 36 alvos (12 públicos × 3 tipos) e as 3 fases;
- `prompts/fase1-3versoes.md` — o prompt da fase de texto, congelado a cada
  fluxo criado (editar aqui só afeta fluxos NOVOS);
- `textos/C<N>/` — os roteiros gerados, um por alvo, mais o
  `resumo-estrategico.md`.

Os avatares baixados vão para `state/artefatos/fluxos/C<N>/` no repo do bot, com
o título `C<N>-<alvo>-v1` — o MESMO nome que você deve usar no estúdio, senão o
download não encontra o vídeo.

## Custo

36 alvos × avatar gerado à mão. Rode filtrado (`| alvos=…`), e confira em
`| sombra` antes.
