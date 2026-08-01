# promoavatar2

Três vídeos por público, em vez de um. O resto é o `promoavatar`: o bot escreve
os textos e PARA, você gera os avatares no HeyGen, `/aprovar C#N` libera o
download e o reel.

Referência: `C#7`. O `promoavatar` é `A#`, o `promoclub` é `P#` — o bot recusa
referência com prefixo trocado.

Uso, opções e a tabela dos três tipos: `HELP.md` (ou `/promoavatar2 help` no
chat). As decisões de engenharia e o porquê de cada uma: `CLAUDE.md`.

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

## Atenção: tudo aqui é congelado na criação

`flow.json` e o prompt são copiados para dentro do fluxo no momento em que ele
nasce. Editar aqui só afeta fluxos NOVOS — um fluxo em andamento não muda de
regra no meio. Para valer no que já existe, crie outro.
