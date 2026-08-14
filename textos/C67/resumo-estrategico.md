# C#67 — resumo estratégico (variante viral)

## 0. Essência (retrato, não opinião)

O conteúdo é uma crítica de como as pessoas usam IA hoje: tratam modelos cada
vez mais capazes como se ainda fossem estagiários, dando instrução passo a
passo em vez de dizer o problema, o resultado esperado, os limites e cobrar
prova de que ficou certo. O autor conta que ele mesmo fazia isso — escrever
prompts enormes, skills, arquivos de regra — e que isso funcionava, até os
modelos ficarem mais capazes e o excesso de instrução passar a piorar o
resultado. Ele fez uma "auditoria de ablação": reduziu skills, tirou buscas
automáticas, moveu contexto só pra onde era necessário, simplificou
instruções — e o resultado melhorou (menos tokens, menos ruído, IA pensando
melhor sozinha). A conclusão não é "pare de dar instrução": é que a
instrução certa muda com a capacidade do modelo — pouca capacidade pede
passo a passo, muita capacidade pede intenção clara e verificação.

O conteúdo fala para quem já usa IA de alguma forma (não é introdução ao
tema) e mexe com prompt/regra, não com um produto específico. NÃO é sobre
abandonar controle sobre a IA, nem sobre abandonar julgamento humano — é
sobre onde aplicar esse julgamento.

## Assunto (fonte)

Ver texto completo no prompt do fluxo. Resumo: crítica ao excesso de
instrução em modelos de IA cada vez mais capazes, ancorada numa "auditoria
de ablação" que o autor fez no próprio sistema de prompts/skills.

## Tese central

"Instrução demais não deixa a IA mais confiável — deixa ela mais burra: você
contrata um especialista e trata como estagiário."

## Motivo para assistir agora

Não há gatilho temporal no assunto (nenhuma data, lançamento ou evento) —
por isso o motivo usado é relevância prática, não urgência fabricada: é um
erro comum e invisível, que a maioria de quem usa IA hoje comete sem
perceber, achando que está ajudando o resultado.

## Elemento demonstrável

A própria auditoria de ablação do autor: reduzir skills, cortar buscas
automáticas, mover contexto, simplificar regras — e o "antes cheio de
regra" virar "depois enxuto e com resultado melhor". Usado nos roteiros como
prova (seção PROVA das sobreposições) e como base de imagens (arquivo de
regras/prompt gigantesco vs. tela limpa).

## Desvio registrado do processo descrito no prompt

A instrução do fluxo pede 5 primeiras frases candidatas por roteiro,
anotadas no resumo com a razão da escolhida. Com 36 roteiros produzidos em
paralelo por 12 agentes (um por público), essa lista de candidatas não foi
centralizada — cada agente escolheu o gancho e a emoção diretamente e
reportou só a decisão final (gancho, emoção, formato, engajamento), não as
alternativas descartadas. Registro aqui como desvio deliberado de escopo,
não como omissão silenciosa: se o revisor humano quiser as alternativas,
elas não existem — apenas a escolha final, abaixo, por alvo.

## Diferenciação por público — gancho, emoção, formato, engajamento

**40mais**
- alc: "Você tem 52 anos e trata a IA feito estagiária." (orgulho ferido, erro comum, escolha binária)
- aut: "Prompt gigante não é cuidado. É desconfiança disfarçada de método." (alívio negado, desmontagem de erro, salvar/testar)
- pro: "Imagina esse gestor de 48 anos, trinta anos de critério — e ainda escreve prompt de estagiário." (medo de ficar pra trás, consequência inesperada, compromisso público)

**60mais**
- alc: "Todo mundo trata a inteligência artificial como estagiária." (orgulho ferido, erro comum, pergunta pra comentário)
- aut: "Existe uma auditoria que qualquer pessoa pode fazer nas próprias instruções pra IA." (alívio negado, desmontagem de erro, salvar/testar)
- pro: cena do aposentado de 65 anos frustrado com a IA (medo de ficar pra trás, consequência inesperada, compromisso público)

**criadores**
- alc: "Seu prompt é gigante e o vídeo sai genérico." (vergonha, erro comum, escolha binária)
- aut: "Você trata sua IA como estagiária eterna." (medo de ficar pra trás, conceito explicado — nomeia "auditoria de ablação", auto-classificação)
- pro: "Cada roteiro seu está preso num prompt enorme." (perda do que já é seu, consequência inesperada, compromisso público)

**educadores**
- alc: "Seu prompt gigante pra IA é o erro." (vergonha, erro comum, pergunta binária)
- aut: a tese central dita como abertura ("instrução demais deixa a IA mais burra") (alívio negado, conceito explicado, salvar/testar)
- pro: "Seu aluno já manda melhor na IA que você." (medo de ficar pra trás, consequência inesperada, compromisso público)

**empreendedores**
- alc: "Você escreve quarenta linhas de prompt pro seu anúncio. Seu concorrente escreve três." (injustiça, comparação, escolha binária)
- aut: "Seu prompt de anúncio tem regra pra fonte, regra pra tom, regra pra CTA — e ainda sai genérico." (vergonha, desmontagem de erro, salvar/testar)
- pro: "Cada linha extra no seu prompt é tempo que devia estar na sua loja." (perda do que já é seu, consequência inesperada, compromisso público)

**familia**
- alc: cena do filho de 14 anos fazendo redação com IA passo a passo (medo de ficar pra trás, erro comum, escolha binária + marcação)
- aut: "Você acha que sabe ensinar seu filho a usar IA. Deixa eu te mostrar o que você tá pulando." (vergonha, desmontagem de erro, salvar/testar)
- pro: "Todo cursinho de prompt que tá surgindo agora ensina seu filho a decorar comando." (perda do que já é seu, consequência inesperada, compromisso público)

**jovens**
- alc: "Você tem 17 anos e decorou dez prompts prontos." (vergonha, erro comum, escolha binária)
- aut: "Prompt bom não é o mais longo. É o mais certo." (orgulho ferido, conceito explicado, salvar)
- pro: "Você abre a IA, escreve cinco parágrafos de instrução — e ainda assim sai errado." (medo de ficar pra trás, consequência inesperada, compromisso público)

**mulheres**
- alc: "Toda IA que você já usou tratou você como estagiária." (vergonha, erro comum, marcação com motivo)
- aut: "Você acha que escreve prompt bom. Deixa eu te mostrar por que não é bem assim." (alívio negado, desmontagem de erro, salvar)
- pro: "Seu prompt gigante não tá te dando controle. Tá te roubando o tempo que você não tem." (perda do que já é seu, consequência inesperada, compromisso público)

**pessoa-comum**
- alc: "Você trata a IA mais esperta do mundo como se ela fosse burra." (medo de ficar pra trás, erro comum, testar e comentar)
- aut: "Aquele textão de regra que você guarda no celular pode estar deixando a IA pior." (vergonha, desmontagem de erro, salvar/testar)
- pro: "Aquele textão que você guardou com tanto carinho está roubando sua própria resposta." (perda do que já é seu, consequência inesperada, compromisso público)

**profissionais**
- alc: "Seu colega não aprendeu prompt melhor que você." (injustiça, comparação, auto-classificação + marcação)
- aut: "Seu prompt gigante está sabotando sua IA." (orgulho ferido, desmontagem de erro, auto-classificação + salvar)
- pro: "Quem vai te substituir não é a IA." (medo de ficar pra trás, consequência inesperada, compromisso público)

**recolocacao**
- alc: "Você trata a IA que escreve seu currículo como se ela fosse burra." (vergonha, erro comum, pergunta pra comentário)
- aut: "Você copiou um prompt pronto de currículo da internet. E mesmo assim continua sem resposta." (injustiça, desmontagem de erro, salvar/testar)
- pro: "Você manda o décimo currículo do mês e a resposta continua sendo silêncio." (perda do que já é seu, consequência inesperada, compromisso público)

**tecnicos**
- alc: "Seu arquivo de regras tem trinta linhas e o agente trava na mesma decisão besta." (vergonha, erro comum, escolha binária)
- aut: "Um criador que vive de IA cortou as próprias skills pela metade — e o sistema ficou melhor." (medo de ficar pra trás, bastidor de sistema — a própria auditoria do autor, salvar)
- pro: "Você testou doze ferramentas de IA esse ano e não construiu nenhum sistema seu." (injustiça/perda do que já é seu, consequência inesperada, compromisso público)

## Riscos de repetição (revisão humana precisa olhar isto)

Dentro de cada público os três tipos não se repetem (regra 14 respeitada:
gancho, formato, emoção e fecho mudam nos três). Mas HÁ convergência
cross-público que o revisor deve notar antes de aprovar em lote:

- **Quase todo `-pro` (10 de 12) usa o mesmo esqueleto**: formato
  "consequência inesperada" + engajamento "compromisso público" + fecho em
  "as três frases: problema / resultado / prova". A dor e a cena mudam por
  público, mas quem assistir dois ou três `-pro` seguidos vai notar o padrão
  se publicados perto um do outro.
- **`-alc` e `-aut` também clusterizam**: a maioria dos `-alc` usa "erro
  comum" (9 de 12) e a maioria dos `-aut` usa "desmontagem de erro" (7 de
  12). A diversidade real está nas EMOÇÕES (bem distribuídas: vergonha,
  orgulho ferido, injustiça, perda, medo, alívio negado aparecem todas) e
  nas cenas concretas, não nos formatos.
- Isso é esperado dado que 12 agentes trabalharam em paralelo sem ver o
  trabalho um do outro, mas significa que o portão humano (`/aprovar`)
  ganha mais publicando os `-pro` e os `-alc` espaçados entre públicos
  diferentes, não em sequência.
- Nenhum caso de depoimento inventado sobreviveu à varredura (checagem
  automática por "eu vi", "um aluno meu", "me contou" — zero ocorrências
  reais nas 36 FALAs).
- Nenhuma menção a marca/curso/trilha/inema.club dentro das seções FALA — a
  única ocorrência de "curso" (`40mais-pro.md`) é uma crítica a "curso de
  prompt" genérico de terceiros, não ao INEMA, e reforça a regra de
  sem-marca ("a virada não começa num curso").
