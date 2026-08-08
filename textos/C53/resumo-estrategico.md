# C#53 — Resumo estratégico

## Assunto
Empresas preparadas para o futuro: o agente deixa de ser um chatbot e vira uma
camada operacional de inteligência ("brain agent"), conectada a conhecimento,
dados, ferramentas e processos. Arquitetura-base: Pessoas → Canais → Agente
central → Skills/Tools/Subagentes → Sistemas e dados → Ações. As skills viram
propriedade intelectual (o "como fazemos aqui" codificado). Surge uma nova
força de trabalho — Pessoas + Agentes + Inteligência Organizacional — e a
liderança muda de função: arquiteta da inteligência, gestora de skills,
designer de decisões, treinadora de agentes. Segurança é estrutural: o agente
não pode ser superusuário — Pessoa → Identidade → Política → Agente → Gateway
de ferramentas → Dados autorizados → Ação → Auditoria. Internos e externos
usam o mesmo sistema com acessos diferentes por identidade. O EVE é o
framework que organiza tudo (instructions.md, skills, ferramentas,
subagentes, eventos, schedules, políticas, evals).

## Tese central
A empresa preparada pro futuro não compra um chatbot — constrói uma
inteligência própria, com regras de acesso, onde cada skill vira patrimônio
da empresa.

## Motivo para assistir agora
Virada de fase: sair de "usar ferramenta de IA" para "ter uma camada de
inteligência organizacional com controle de acesso real". O risco prático e
atual é dar acesso demais a um agente sem política nenhuma — o "superusuário
sem auditoria" que qualquer um pode montar hoje sem perceber o risco.

## Elemento demonstrável
As duas cadeias visuais do assunto — (1) Pessoas → Canais → Agente central →
Skills/Tools/Subagentes → Sistemas e dados → Ações; (2) Pessoa → Identidade →
Política → Agente → Gateway de ferramentas → Dados autorizados → Ação →
Auditoria — e a cena de "mesma pergunta, resposta diferente por identidade"
(CEO/estagiário/cliente). Essas cadeias aparecem na linha PROVA e nas IMAGENS
de praticamente todos os 36 roteiros.

## Como os três tipos se diferenciam, por público

Todos os 12 públicos seguem o mesmo padrão estrutural: `-alc` é opinião
contrária / pergunta incômoda / previsão / mito x realidade, sem CTA
comercial; `-aut` explica uma das duas cadeias como mecânica e fecha num
princípio (ex.: "todo acesso de agente é uma política, não uma permissão
default"); `-pro` é problema→consequência→solução nomeada→benefício→CTA único
para "a trilha de IA do seu perfil no inema.club".

- **40mais**: dor de ficar pra trás tecnicamente apesar da experiência. `-alc`
  opinião contrária (moda não é fundamento); `-aut` modelo mental de acesso;
  `-pro` situação atual e transformação.
- **60mais**: dor de sentir a experiência de vida "não contar mais". Mesmo
  padrão de formato que 40mais, ângulo mais voltado a propósito/legado.
- **criadores**: dor da dependência de ferramentas soltas e processo que não
  escala. `-alc` previsão; `-aut` passo a passo de codificar o "jeito de
  criar" como skill; `-pro` problema e solução.
- **educadores**: medo de irrelevância, conhecimento pedagógico que não é
  transferido. `-alc` previsão; `-aut` passo a passo aplicado a plano de
  aula; `-pro` problema e solução.
- **empreendedores**: dependência de pessoa-chave, medo de dar acesso demais
  a um agente. `-alc` pergunta incômoda; `-aut` passo a passo de revisar
  processo; `-pro` problema e solução.
- **familia**: adaptado para o filho, não para a empresa do pai/mãe — dor de
  que a escola não prepara pro mercado que vem. `-alc` previsão; `-aut`
  conceito explicado; `-pro` problema e solução.
- **jovens**: falta de experiência, medo de escolher profissão que some.
  Gancho aproveita a figura do "estagiário" do próprio assunto. `-alc`
  opinião contrária; `-aut` conceito explicado; `-pro` problema e solução.
- **mulheres**: sobrecarga e desejo de autonomia. `-alc` opinião contrária;
  `-aut` explicação prática em 3 passos; `-pro` problema e solução.
- **pessoa-comum**: leigo, achava que IA é só chat. Zero jargão sem tradução.
  `-alc` mito x realidade; `-aut` conceito explicado (a jornada de uma
  pergunta até virar ação); `-pro` problema e solução.
- **profissionais**: medo de a profissão virar commodity. `-alc` opinião
  contrária; `-aut` conceito explicado; `-pro` problema e solução.
- **recolocacao**: perdeu emprego ou quer mudar de área, medo de que a
  experiência não sirva mais. `-alc` previsão (critério de contratação);
  `-aut` conceito explicado (cadeia de acesso); `-pro` problema e solução,
  sem prometer emprego.
- **tecnicos**: já entende tecnologia, mas só testa ferramenta sem projetar
  sistema. Vocabulário técnico direto (gateway, política, subagente). `-alc`
  opinião contrária; `-aut` passo a passo; `-pro` problema e solução.

## Riscos de repetição
Os 12 `-pro` convergem para o mesmo CTA genérico ("a trilha de IA do seu
perfil no inema.club") por design — é o CTA seguro do catálogo, já que
nenhum curso específico do catálogo cobre exatamente "brain agent
empresarial". Isso é esperado, mas se algum público tiver um curso mais
específico no catálogo (ex. Claude Code / Agentes para `tecnicos` ou
`empreendedores`), vale revisar no portão e trocar pelo nome real.

As duas cadeias (execução e controle) aparecem como PROVA em quase todos os
36 roteiros — natural, já que é o único elemento demonstrável forte do
assunto, mas quem revisa deve conferir se a repetição visual entre públicos
diferentes não cansa quando vistos em sequência (o ângulo de cada IMAGEM 1
varia por público, isso ajuda a diferenciar).

## O que precisa de revisão humana
- Conferir se o CTA genérico-seguro é aceitável para os 12 `-pro`, ou se
  algum público merece um curso nomeado do catálogo.
- `familia` interpreta o assunto pela ótica do filho (mercado de trabalho
  futuro), não da empresa do pai/mãe — confirmar se essa adaptação está
  alinhada com a intenção de quem pediu o fluxo.
- Conferir tom técnico de `tecnicos` (usa "superusuário", "gateway",
  "subagente" sem tradução) — está dentro da regra do público, mas é o mais
  denso dos 12.
