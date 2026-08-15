promoavatar3 — três vídeos por público

O bot escreve os textos e PARA. Você gera os avatares no HeyGen; com
/aprovar C#N o resto segue sozinho até a entrega no canal. A diferença
para o promoavatar: cada público rende TRÊS roteiros, não um.

  /promoavatar3 <assunto> [campos]

Campos mais usados:

  | alvos=jovens-alc,jovens-pro   só esses (sem isto são os 36)
  | prompt=viral                  outra estratégia de texto
  | estudio                       o BOT gera os avatares
  | sombra                        mostra o plano, não enfileira
  | legenda=nao                   reel sem legenda
  | versao=N · | de=<fase> · | sem-portao

Fases:  texto ⏸️ → avatar → baixar ⏸️ → reel (entrega no canal)
        ⏸️ = para e espera o seu /aprovar

Referência: C#7 (o promoavatar usa A#, o promoclub usa P#). Acompanhe
com /status C#7; o bot recusa referência com prefixo trocado.

## TIPOS — os três vídeos de cada público

  -alc   alcance      25–40s   interromper a rolagem, ser compartilhado
                               CTA: comentar ou compartilhar
                               (nunca comercial)

  -aut   autoridade   35–60s   ensinar algo concreto, ser salvo
                               CTA: salvar, seguir ou testar

  -pro   promocional  30–45s   ligar dor a solução
                               CTA: um só, para o inema.club

Ordem de publicação recomendada: alcance → autoridade → promocional.

## ALVOS — os 36 e como filtrar

São 36: os 12 públicos × 3 tipos, escritos <publico>-<tipo>
(jovens-alc, mulheres-pro, 40mais-aut…). O canal e o gatilho são do
PÚBLICO — os três tipos de um público dividem os dois e caem no mesmo
livesN.

Os 36 estão declarados, mas rodar os 36 de uma vez são 36 avatares e 36
renders. O normal é filtrar:

  /promoavatar3 <assunto> | alvos=jovens-alc,jovens-aut,jovens-pro

Os 12 públicos:

  pessoacomum jovens profissionais mulheres empreendedores tecnicos
  40mais 60mais educadores criadores recolocacao familia

## VARIANTES de texto (o campo | prompt=)

Trocam a ESTRATÉGIA com que a fase de texto escreve. As outras fases não
mudam. A variante é escolhida na criação e fica CONGELADA no fluxo.

  (nada)              o prompt padrão: três tipos, CTA comercial no -pro

  | prompt=manifesto  para assunto que chega como MANIFESTO (lista de
                      preceitos). Vira uma tese sobre o custo de não
                      agir, usando no máximo 3 preceitos da lista

  | prompt=viral      alcance acima de tudo: sem marca, sem curso, sem
                      inema.club na fala. CTA sempre de engajamento,
                      duração livre de 15 a 45s, e o -pro vira direção
                      em vez de venda

O clipe de encerramento acompanha a variante: o padrão é o CTA ("SAIBA
MAIS EM inema.club") e o viral leva um de 3s só com a marca, sem ordem
nenhuma — assim ele não compete com o pedido de comentário, que é onde a
variante viral ganha.

## FASES — o que cada uma faz

  1. texto (escopo fluxo, PARA depois)
     Um arquivo por alvo em textos/C<N>/<alvo>.md, mais um
     resumo-estrategico.md. O bot manda a FALA de cada um no chat e para.

  2. avatar (por alvo, OPCIONAL)
     Quem gera o vídeo. Sem opção nenhuma, é você no estúdio.
     Ver /promoavatar3 help rotas.

  3. baixar (por alvo)
     Depois do /aprovar C#N, procura no HeyGen o vídeo cujo nome é
     exatamente C<N>-<alvo>-v1 e baixa o MP4 — a versão COM legenda
     queimada quando o estúdio gravou com ela, a limpa quando não.
     Prazo: 40h. A fila do HeyGen chega a 36h, e esperar não é erro —
     o teto existe só para o vídeo que nunca foi gerado.

  4. reel (por alvo)
     Monta o reel 9:16 e ENTREGA no canal do público
     (yt-pub-livesN/imports/videos). É função: sem agente, sem token.
     Roda um por vez (a fila render é a GPU), ~3 min cada.

## ROTAS de avatar — só UMA por fluxo

  (nada)        você, no estúdio            assinatura
  | estudio     o bot, por SCRIPT no        créditos da assinatura
                estúdio (Playwright)
  | creditos    o bot, pela CLI (OAuth)     créditos da assinatura
  | api         o bot, pela chave de API    carteira em US$
                                            (~US$ 0,73 por vídeo)

Pedir duas é recusado na criação: juntas gerariam o mesmo vídeo duas
vezes.

O | estudio clona o TEMPLATE-AVATAR e herda cenário, avatar, voz e motor
— o vídeo sai igual ao que você gravaria à mão. Medido em 48 avatares:
~50s por público, zero falha, zero token. As outras duas rotas montam o
vídeo SEM template (mesmo rosto e voz, cenário diferente).

Com 36 alvos são 36 avatares em série (~31 min) e depois a fila do
HeyGen. Filtre com | alvos= na primeira vez.

## TITULO no estúdio — o contrato

Ao gerar no HeyGen, o título do vídeo tem que ser EXATAMENTE
C<N>-<alvo>-v<versao> — ex.: C7-jovens-pro-v1. É por esse nome que o
download casa; um caractere fora e a fase de baixar não encontra nada.

Os sufixos são abreviados (alc, aut, pro — não alcance, promocional)
porque título longo já truncou no HeyGen em produção e derrubou o match.

## PORTAO — conferir antes de gastar

Nenhuma rota de avatar tira o portão: você revisa os textos e dá
/aprovar C#N antes de gastar. Para a esteira inteira rodar sem parar,
some o campo | sem-portao ao comando.

  /promoavatar3 <assunto> | alvos=jovens-alc | sombra

O | sombra imprime fase × alvo × fila × tarefa e NÃO enfileira nada. É
assim que se confere um assunto novo antes de gastar GPU — e a fase de
avatar só aparece no plano quando a opção dela está ligada.

## LEGENDA — ligada por default

Desde 2026-08-13 o motor deste repo legenda, com o mesmo desenho do
promoavatar: uma palavra por vez, caixa alta, branca com contorno preto
grosso, âmbar só na palavra-chave, colada na base da faixa do avatar.
As palavras-chave saem das SOBREPOSIÇÕES do texto do público; sem elas a
legenda fica toda branca — resultado válido, não falha.

Cuidado com legenda DUPLA: a do estúdio vem queimada no MP4 do avatar e
não tem remoção. Se você gravar com legenda lá E o reel legendar aqui,
saem duas. Escolher uma é desligar a outra — e desligar a do estúdio é no
TEMPLATE-AVATAR do HeyGen, não aqui.

Desliga a daqui com | legenda=nao.

Detalhes de cor, corpo e posição: docs/legenda.md
