# C#180 — resumo estratégico

## Passo zero

**Essência (2-4 frases fiéis):** A IA moderna não é apenas programada, é cultivada.
O modelo vem pronto do laboratório — quem faz a diferença é quem cuida do AGENTE:
o ambiente ao redor dele (contexto, ferramentas, regras, exemplos, memória,
avaliação, feedback). Não é um tutorial de prompt nem uma promessa de resultado —
é um jeito de encarar o trabalho com IA como um ciclo contínuo de melhoria, não
como uma ferramenta usada do mesmo jeito pra sempre. Não é sobre qual modelo é
melhor; é sobre quem constrói o melhor ambiente em volta dele.

**Tese central:** IA não se programa uma vez, se cultiva todo dia — quem só usa
o modelo pronto repete o mesmo resultado, quem cultiva o ambiente melhora a cada
ciclo (executar → avaliar → corrigir o ambiente → executar de novo).

**Motivo para assistir agora:** todo mundo já usa IA, mas quase ninguém trata o
erro dela como dado pra melhorar o sistema — a maioria corrige na conversa e
esquece, em vez de transformar a correção em regra, exemplo, memória ou
ferramenta permanente.

**Elemento demonstrável:** o contraste entre "modelo pronto, mesmo resultado
sempre" e "ambiente cultivado, resultado que melhora" — visualizado nas imagens
como semente idêntica x planta cuidada, engrenagem travada x roda que gira,
ciclo de três passos que se repete e evolui.

## Assunto (fonte)

8 elementos pra cultivar um agente (Função, Contexto, Ferramentas, Regras e
limites, Exemplos, Memória, Avaliação, Feedback — os 4 primeiros fazem o agente
funcionar, os 4 últimos fazem ele melhorar); ciclo executar → avaliar → corrigir
o ambiente → executar de novo; os 3 "jardins" (vida pessoal, Jarvis pessoal,
negócios); autonomia progressiva em 3 níveis (propõe/humano executa → executa/
humano revisa → executa e reporta); para empresas, o diferencial deixa de ser o
melhor modelo e passa a ser melhor contexto + processos + ferramentas +
exemplos + feedback + gestão dos agentes.

## Por público: como os 3 tipos se diferenciam

Cada público usa a Dor/Gatilho da tabela da skill `inemaclub-textos` como
matéria-prima, adaptado pro "jardim" mais relevante daquele público dentro do
tema. Resumo do ângulo de cada um (gancho/estrutura/CTA variam entre os 3 tipos
do mesmo público, conforme regra 14):

- **40mais** — jardim: experiência vira memória do agente. `-alc` contrasta
  modelo pronto x ambiente; `-aut` ensina o ciclo aplicado à memória; `-pro`
  aponta o custo de ser tratado como caro/ultrapassado e propõe escrever regras
  do agente hoje.
- **60mais** — jardim: uma vida de decisão vira contexto. Ângulo de propósito
  em vez de medo de tecnologia.
- **criadores** — jardim: agente que aprende o estilo/tom, ligado à dor de
  ritmo de postagem que esgota.
- **educadores** — jardim: agente de apoio só ensina certo com as regras do
  professor; liga à dor de virar fiscal de cola.
- **empreendedores** — jardim negócios: agente de vendas/atendimento/
  financeiro só entrega com ambiente cuidado; liga à dor de custo de agência.
- **familia** — jardim: formar o filho é ensinar a cultivar um agente (dar
  contexto, marcar limite, cobrar explicação); liga à dor de não saber orientar
  pro mundo que vem.
- **jovens** — jardim: cuidar do ambiente da IA é a profissão nascendo; liga à
  dor de medo de escolher profissão que some.
- **mulheres** — jardim: autonomia progressiva do agente espelha a autonomia
  que a própria pessoa busca; liga à dor de jornada dupla sem tempo.
- **pessoacomum** — jardim: quem cultiva o ambiente (contexto) tira mais
  proveito da IA; liga à dor de sentir que todo mundo tira mais proveito.
- **profissionais** — jardim: a diferença está no ambiente que o colega
  montou, não no modelo; liga à dor de medo de ser substituído.
- **recolocacao** — jardim: feedback vira melhoria, não desculpa — cada
  rejeição é dado pra ajustar o próximo passo; liga à dor da renda acabando.
- **tecnicos** — jardim: autonomia progressiva em níveis (propõe → executa/
  revisa → executa/reporta), provando consistência; liga à dor de virar
  testador eterno de ferramenta.

Dentro de cada público, `-alc` interrompe a rolagem com afirmação/pergunta/
comparação e fecha em escolha binária ou outro engajamento; `-aut` ensina o
ciclo executar-avaliar-corrigir aplicado ao elemento daquele jardim e fecha
pedindo pra salvar; `-pro` liga a dor específica à consequência de adiar e
termina com o primeiro passo nomeado (abrir conversa nova com a IA e escrever
regras que o agente nunca deve quebrar sem perguntar) + compromisso público nos
comentários.

## Riscos de repetição

- O primeiro passo nomeado no `-pro` ("abra uma conversa nova e escreva as
  regras que a IA nunca deve quebrar sem perguntar") é o MESMO texto nos 12
  públicos — deliberado, pra fixar uma ação memorável e replicável, mas em
  publicação sequencial pode soar repetitivo pra quem vê vários seguidos.
  Se for publicar vários `-pro` próximos, considerar variar essa frase manualmente.
- Os ganchos de abertura são sorteados de um pool de 5 frases por tipo,
  rotacionado por índice do público — com 12 públicos e 5 ganchos, há 2-3
  publicos por tipo compartilhando a MESMA frase de abertura (idx % 5: com 12
  públicos na ordem 40mais/60mais/criadores/educadores/empreendedores/familia/
  jovens/mulheres/pessoacomum/profissionais/recolocacao/tecnicos, `40mais` e
  `familia` dividem o gancho 1, `60mais` e `jovens` o gancho 2, e assim por
  diante). O gancho falado é idêntico, mas a
  cena/dor/exemplo que vem em seguida diferencia o vídeo — ainda assim, revisão
  humana deve conferir se dois vídeos com abertura idêntica vão ao ar próximos
  um do outro.
- A frase de fecho do `-alc` ("IA não se programa uma vez. Se cultiva todo
  dia.") e do `-aut` ("Corrigir a conversa resolve hoje. Corrigir o ambiente
  resolve sempre.") se repetem literalmente nos 12 públicos de cada tipo —
  também deliberado como frase-mãe/princípio repetível da série, mas é o ponto
  de maior redundância entre os 36 arquivos.

## O que precisa de revisão humana

- Conferir se a analogia jardim/agente soa natural falada em voz alta pro
  público leigo (`pessoacomum`, `60mais`) — o vocabulário "ambiente",
  "cultivar" pode soar abstrato demais sem o contexto visual das IMAGENS.
  Ajustar tom na hora da gravação se necessário.
- Os 8 elementos (memória, contexto, ferramentas, regras e limites, exemplos,
  função, autonomia progressiva, feedback) foram distribuídos 1 por público —
  não são citados pelo nome técnico na fala (regra de linguagem falada), mas
  aparecem no headline da IMAGEM 1 de cada `-aut`; confirmar que isso não soa
  como jargão fora de lugar pro público leigo.
- Duração real depende da locução do avatar no HeyGen — o texto foi calibrado
  por contagem de palavras (~2,5 palavras/segundo) pra ficar dentro de
  25-40s (`alc`), 35-60s (`aut`) e até ~45s (`pro`), mas vale conferir a
  duração real após a primeira geração e ajustar se necessário.
- Como é variante viral, os 36 vídeos NÃO citam marca/curso/inema.club na
  fala — confirmar no motor do reel que o clipe final de 3s com a marca está
  configurado corretamente pra esses 36 alvos antes de publicar.
