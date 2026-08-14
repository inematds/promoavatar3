# C#66 — resumo estratégico (variante viral)

## 0. ESSÊNCIA (retrato fiel do assunto)

O autor argumenta que estamos ensinando IAs cada vez mais inteligentes como se
fossem estagiárias — instrução exaustiva, passo a passo, formato fixo — quando
deveríamos tratá-las como um profissional de vinte anos de experiência: dar o
problema, o resultado desejado, os limites, o padrão de qualidade, e cobrar
prova de que ficou certo. Ele fez uma "auditoria de ablação" no próprio
sistema — reduziu skills, tirou buscas automáticas sempre ligadas, moveu
contexto pros projetos certos, simplificou instruções — e o resultado foi
menos tokens, menos ruído e uma IA mais capaz de pensar por conta própria.
Conclusão do autor: modelos menos capazes precisam de mais instrução; modelos
mais capazes precisam de mais intenção e melhor verificação. **Não é um
tutorial técnico de prompt** — é uma mudança de mentalidade sobre como
delegar pra uma IA que já é competente, dirigida a quem já usa IA a sério.
NÃO é sobre uma ferramenta específica, nem sobre um produto, nem sobre
"aprender a fazer prompt melhor" no sentido raso.

## Assunto (fonte)

Texto corrido enviado por quem pediu o fluxo — transcrição livre sobre a
analogia estagiário / 2 anos / 20 anos de experiência aplicada a como
instruir modelos de IA, e o relato da auditoria de ablação feita no próprio
sistema de instruções.

## Tese central

"Quanto mais inteligente o modelo, menos instrução e mais intenção ele
precisa."

## Motivo para assistir agora

Padrão que qualquer pessoa que usa IA todo dia reconhece na própria prática —
instruir demais um modelo capaz tende a piorar o resultado, e isso foi
confirmado pelo próprio experimento do autor (cortou instrução, a IA
melhorou).

## Elemento demonstrável

Dois: (1) a analogia estagiário vs. profissional de 2 anos vs. profissional
de 20 anos — três formas diferentes de delegar a MESMA tarefa; (2) a
auditoria de ablação em si — antes (skills empilhadas, buscas automáticas
sempre rodando, instruções longas) e depois (menos tokens, menos ruído, mais
autonomia).

## Como os 12 públicos se diferenciam (gancho / emoção / engajamento por tipo)

Cada público usou UMA situação concreta e pessoal (não plural genérico) e
emoções distintas entre os três tipos do mesmo público, conforme exigido.
Ganchos completos e as 5 candidatas de cada roteiro estão na seção ESTRUTURA
de cada arquivo — aqui só o resumo de qual venceu e por quê.

### 40mais
- alc: "A vaga foi pro mais novo. De novo." — injustiça — binária (ainda escrevo manual / já parei)
- aut: "Ele tirou metade das instruções e ela ficou melhor." — alívio negado — auto-classificação
- pro: "Sua experiência virou instrução. Devia virar critério." — medo de ficar pra trás — compromisso público

### 60mais
- alc: "Eu tratava a IA igual estagiária." — vergonha — binária numerada
- aut: "Todo mundo acha que quanto mais detalhe você dá, melhor ela responde." — orgulho ferido — auto-classificação (3 perfis)
- pro: "Você escreve um parágrafo inteiro e a resposta ainda vem torta." — injustiça — compromisso público

### criadores
- alc: "Cortei três coisas da minha IA e ela ficou melhor." — vergonha — binária
- aut: "Você acha que instrução demais ajuda a IA. É o contrário." — injustiça — auto-classificação
- pro: "Você paga ferramenta cara e ainda escreve prompt de estagiário." — injustiça — compromisso público

### educadores
- alc: "O aluno não colou. Ele orquestrou." — medo de ficar pra trás — binária
- aut: "Você escreve pra IA como se ela fosse estagiária." — orgulho ferido — auto-classificação
- pro: "Ela pede pra IA e ainda reescreve tudo." — alívio negado — compromisso público

### empreendedores
- alc: "Eu tratei minha IA igual estagiária por meses." — vergonha — binária
- aut: "Todo mundo acha que prompt bom é prompt detalhado." — orgulho ferido — binária
- pro: "Você paga agência cara pra fazer o que a IA já faria." — injustiça — compromisso público

### familia
- alc: "O erro não é do seu filho. É seu." — vergonha — binária
- aut: "A IA ficou mais esperta. Seu jeito de usar não." — medo de ficar pra trás — auto-classificação
- pro: "A escola do seu filho prepara ele pro ontem." — injustiça — compromisso público

### jovens
- alc: "Seu colega de estágio não é mais inteligente que você." — injustiça — binária numerada
- aut: "Prompt gigante não é cuidado. É desconfiança escrita." — orgulho ferido — confronto amistoso (teste de cortar pela metade)
- pro: "Você já escolheu a faculdade com medo de a profissão sumir." — medo de ficar pra trás — compromisso público

### mulheres
- alc: "A IA ficou mais esperta e você não percebeu." — vergonha — binária
- aut: "Quanto mais você explica, pior a IA responde." — orgulho ferido — auto-classificação
- pro: "Você gasta a manhã explicando o óbvio pra IA." — perda do que já é seu — compromisso público

### pessoa-comum
- alc: "Ela não é sua estagiária. Você trata como uma." — medo de ficar pra trás — binária
- aut: "Quanto mais você explica pra IA, pior a resposta fica. Às vezes." — vergonha — auto-classificação
- pro: "Você tá fazendo o trabalho que a IA devia fazer." — orgulho ferido — compromisso público

### profissionais
- alc: "Ele não é mais rápido. Ele pede diferente." — medo de ficar pra trás — binária
- aut: "Você acha que sabe usar IA. Sabe pela metade." — vergonha — auto-classificação
- pro: "Você escreveu um prompt de dez linhas e ainda corrigiu à mão." — perda do que já é seu — compromisso público

### recolocacao
- alc: "Você trata a IA como estagiária. Ela percebe." — vergonha — binária
- aut: "Você acha que sabe usar IA. Sabe metade." — orgulho ferido — auto-classificação
- pro: "Cada instrução extra que você escreve, ela ignora uma." — medo de ficar pra trás — compromisso público

### tecnicos
- alc: "Eu tinha 40 linhas de instrução numa skill. A IA piorou." — vergonha — binária
- aut: "Prompt longo não é cuidado. É desconfiança disfarçada de organização." — orgulho ferido — confronto amistoso
- pro: "Você empilhou 40 prompts numa skill e o resultado piorou a cada versão." — injustiça — compromisso público

## Riscos de repetição / o que precisa de revisão humana

- **Padrão de gancho repetido entre públicos diferentes** (não dentro do mesmo
  público, que é o que a regra proíbe): a estrutura "Você trata/tratava a IA
  como estagiária" aparece, com variação, em `40mais-pro`(implícito),
  `60mais-alc`, `pessoa-comum-alc`, `recolocacao-alc`, `jovens-alc`
  (invertido: "colega não é mais inteligente"). Individualmente cada um é
  honesto e específico ao público, mas publicados juntos no mesmo feed a
  semelhança de abertura pode cansar quem segue vários. Revisar se convém
  variar mais a estrutura sintática antes de publicar em sequência.
- **Emoção "orgulho ferido" concentrada nos `-aut`**: por ser o tipo que
  desmonta um erro comum, a maioria dos roteiros de autoridade usa essa
  emoção. Esperado pela natureza do tipo, mas revisar se o lote inteiro não
  fica monocórdio nesse eixo.
- **"Compromisso público" (comentar "cortei"/"vou testar hoje") é o
  engajamento dominante nos `-pro`**: por ser o formato que mais combina com
  "direção", mas maioria dos 12 `-pro` usa essa mesma mecânica de CTA.
  Funciona, mas o pipeline de moderação vai receber muitos comentários com a
  mesma palavra ("cortei") — vale revisar se isso é desejável em escala.
- **`tecnicos-aut` e `40mais-aut` usam confronto amistoso/frase quase idêntica**
  ("prompt longo não é cuidado, é desconfiança") — dois públicos diferentes
  chegaram à mesma virada de frase de forma independente (agentes separados).
  Não é proibido (públicos diferentes), mas revisar antes de publicar os dois
  próximos um do outro.
- **Todos os roteiros seguem a regra de honestidade** (nada de data/preço/vaga
  inventados, sem urgência fabricada, sem promessa de renda/emprego) e nenhum
  menciona marca, curso ou inema.club na fala — checagem feita por amostragem
  em vários arquivos, mas revisão humana arquivo por arquivo antes do HeyGen
  continua necessária, como sempre.
- **Seção IMAGENS**: todos os 36 arquivos têm a seção obrigatória com
  headline + hook + prompt em inglês, evitando os clichês proibidos (perfil
  diante de holograma, HUD, matrix, robô-mão, lâmpada). Revisão humana de cada
  IMAGEM 1 (capa) recomendada antes de gastar render, conforme os três testes
  da regra 11b (transferência, polegar, tensão).
