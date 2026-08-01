# promoavatar2

Irmão do `promoavatar`, com o mesmo portão humano (o bot escreve os textos e
PARA; você gera os avatares no HeyGen; `/aprovar C#N` libera download e reel).
A diferença é uma só: **cada público rende três roteiros, não um.**

Referência: `C#7`. O `promoavatar` é `A#`, o `promoclub` é `P#`.

## Por que é um repo separado, e não uma opção do promoavatar

O motor (`~/projetos/inemaccbot`) resolve `flow.json` na raiz do repo de domínio
(`src/dominio/registry-fluxos.ts`), e o `prompt` é campo fixo da fase dentro da
definição congelada. **Um repo = um fluxo.** Uma flag `--modo=3versoes` exigiria
mudar o bot para atender um domínio — o inverso da regra do README dele.

## Por que o alvo é `<publico>-<tipo>` e não `<tipo>`

A fase 3 (reel) interpola `"capa impacto, público {canal}"` e monta a headline a
partir de `{gatilho}`. Com o alvo sendo só o tipo, o reel receberia "público
alcance" e um gatilho com objetivo editorial no lugar da dor do público — e a
fase 3 roda sem revisão humana, então ninguém pegaria.

Com a chave composta, `{canal}` e `{gatilho}` mantêm o sentido e o título do
estúdio (`tituloEstudio` = `<prefixo><id>-<alvo>-v<versao>`, literal da chave do
alvo) sai distinto por versão de graça.

Sufixos curtos (`alc`/`aut`/`pro`) porque título longo truncou no HeyGen em
produção e quebrou o match do download.

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
