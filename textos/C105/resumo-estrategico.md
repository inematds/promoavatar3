# C#105 — Resumo estratégico (variante viral)

## ESSÊNCIA (retrato fiel do assunto)

O texto apresenta o framework **VAULT** (Verify, Augment, Understand the Why,
Loop Humans In, Transparency), inspirado em práticas usadas no Goldman Sachs
para tornar sistemas de IA mais seguros e confiáveis dentro de empresas. Fala
para quem toma decisões sobre onde e como usar IA (times, gestores, quem
constrói sistemas), e defende: nem tudo precisa virar "agente de IA" —
automação tradicional é mais barata, previsível e auditável quando a tarefa
tem regra clara; toda afirmação crítica de IA precisa de verificação
(fontes originais, testes, revisão humana); comece pelo problema, não pela
tecnologia; o nível de supervisão humana tem que acompanhar o risco (dinheiro,
clientes, dados, publicações, grandes grupos); e é preciso registrar fontes,
entradas, ferramentas, decisões e ações para o sistema ficar auditável — sem
expor o raciocínio interno do modelo. O melhor sistema normalmente combina
automação determinística (para os fatos) com IA (para interpretar e
comunicar).

O texto NÃO é um manifesto anti-IA, não promete renda nem emprego, e não é um
elogio genérico de "use mais IA" — é um checklist de responsabilidade técnica
sobre QUANDO e COMO usar IA com segurança.

## Assunto (fonte)

Framework VAULT para uso responsável de IA em empresas/times, com as 5 letras
(Verify, Augment, Understand the Why, Loop Humans In, Transparency) e a
conclusão de que a melhor arquitetura combina automação determinística +
IA para interpretar/comunicar, sem transformar tudo em agente.

## Tese central

"Quem usa IA sem verificar, sem entender o porquê e sem manter humano no
controle está construindo em cima de areia — e vai descobrir isso na pior
hora."

## Motivo para assistir agora

Relevância prática: cada vez mais gente e empresas delegam decisões para IA
sem checar nada, e o custo desse erro aparece depois, não na hora. Sem data
nem urgência fabricada — não há elemento temporal no assunto.

## Elemento demonstrável

A sigla V-A-U-L-T como checklist visível na tela, e o contraste visual entre
dois caminhos: "automação determinística + IA" (funciona) vs. "virar tudo
agente de IA" (quebra, custa caro, não passa em auditoria).

## Como os 36 roteiros se diferenciam

Cada um dos 12 públicos usa a mesma tese e a mesma sigla VAULT, mas entra por
uma dor e um ângulo emocional diferentes (ver tabela do CLAUDE.md do projeto):
`40mais` via experiência tratada como custo; `60mais` via desconfiar antes de
confiar como vantagem de vida; `criadores` via conteúdo automatizado que a
audiência fareja como falso; `educadores` via aluno que usa IA sem checar;
`empreendedores` via dinheiro vazando em automação desnecessária;
`familia` via filho aceitando resposta de IA sem questionar; `jovens` via
testar ferramenta vs. entender o que está por trás; `mulheres` via disciplina
de checar com pouco tempo disponível; `pessoacomum` via uso preguicoso da IA;
`profissionais` via risco de ser pego no erro por confiar cego;
`recolocacao` via currículo genérico feito 100% por IA sem revisão;
`tecnicos` via "agente" aplicado onde bastava automação simples (única
variante com jargão técnico liberado).

Dentro de cada público, os 3 tipos mudam gancho, formato e fecho:
- `-alc`: alcance puro, sem marca, formato livre (afirmação/pergunta/mito/
  erro comum/etc.), CTA de comentário/compartilhamento.
- `-aut`: ensina uma parte concreta do VAULT, termina com princípio
  repetível, CTA de salvar/seguir.
- `-pro`: dor → consequência → primeiro passo nomeado hoje, CTA de
  compromisso público. Nesta variante viral, o `-pro` TAMBÉM não cita marca,
  curso nem inema.club na fala — o `fecho` comercial do fluxo padrão foi
  ignorado por instrução explícita da tarefa.

## Riscos de repetição e pontos de revisão humana

- Vários públicos compartilham a mesma dor-base ("confiar cego na IA") —
  checar na revisão se o ÂNGULO de entrada (a cena/pessoa concreta) de fato
  varia o suficiente entre públicos próximos (ex.: `profissionais` vs.
  `tecnicos`; `pessoacomum` vs. `40mais`).
- Cada agente escreveu de forma independente: revisar se a menção a "Goldman
  Sachs" (quando presente) está sempre explicada em 1 frase ou evitada, como
  pedido — nome que o público não entenderia sem contexto não pode aparecer
  cru.
- Conferir que nenhum `-pro` deslizou para CTA comercial ou citou
  inema.club/curso na FALA (regra do topo da variante viral vence sobre o
  fluxo padrão).
- Conferir que a seção `## IMAGENS` de cada arquivo tem `headline:` e
  `hook:` em toda imagem, sem texto embutido pedido no prompt visual, e sem
  os clichês proibidos (perfil diante de holograma, HUD, matrix, cérebro de
  circuito, robô apertando mão humana, lâmpada).
- Verificar que nenhuma cena de "pessoa concreta" (regra 15) foi escrita em
  primeira pessoa como testemunho real (proibido) — deve estar em segunda
  pessoa ou hipótese no presente.
