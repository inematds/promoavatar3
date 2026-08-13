# Essência do conteúdo + afiação dos prompts de fase 1 — Plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fazer a fase 1 do promoavatar3 (a) capturar e preservar a ESSÊNCIA do
conteúdo recebido antes de derivar os 36 roteiros (12 públicos × 3 tipos:
alcance / autoridade / promocional), e (b) aplicar os achados da avaliação de
2026-08-13: dores por público, oficina de gancho, pessoa concreta, frase
repetível, contradições internas do viral e cercas éticas.

**Architecture:** Só prosa — três arquivos de prompt (`prompts/fase1-3versoes.md`,
`prompts/fase1-promocao.md`, `prompts/fase1-viral.md`), a tabela da skill local
(`.claude/skills/inemaclub-textos/SKILL.md`) e três campos do `flow.json`.
Nenhum código muda. Os três prompts compartilham ~330 linhas idênticas: toda
edição em bloco compartilhado se aplica AOS TRÊS, exceto onde a tarefa disser o
contrário.

**Tech Stack:** Markdown (prompts congelados pelo bot inemaccbot na criação do
fluxo), JSON (`flow.json`), pytest só como rede de regressão.

## Contexto verificado (não re-descobrir)

- `flow.json` → fase `texto` congela `prompts/fase1-3versoes.md`. As variantes
  `fase1-promocao.md` e `fase1-viral.md` são INERTES hoje (a flag `| prompt=` do
  bot ainda não existe). **Não renomear nenhum arquivo de prompt.**
- 36 alvos no `flow.json` = 12 públicos × {alc, aut, pro}. Cada alvo carrega
  `gatilho` (cópia da tabela da skill) e `fecho`.
- `{{publicos}}` no prompt é só a lista de nomes de alvo (`jovens-alc, ...`).
  A dor/gatilho de cada público chega ao modelo APENAS pela tabela da skill.
- O bot lê a PRIMEIRA seção `### FALA` de cada arquivo gerado — linhas de
  decisão antes dela são permitidas (já existem `Tipo:` e `Formato escolhido:`).
- O motor do reel (`preparar.py`) exige `## IMAGENS` com `headline` e `hook`
  (exit 3 sem elas) — NENHUMA tarefa deste plano toca nas regras 11/11b.

## Global Constraints

- Autor e committer de TODO commit: `inematds <inematds@gmail.com>` (conferir
  `git config user.email` antes do primeiro commit; corrigir só localmente).
- Um commit por tarefa; `git push` só na Tarefa 7, uma vez.
- Repo de trabalho: `~/projetos/promoavatar3`. O repo
  `~/projetos/promoavatar` (1 formato) NÃO é tocado nesta rodada.
- Regras 9 e 10 dos prompts (nada inventado, nada de urgência fabricada) não se
  afrouxam em nenhuma tarefa — são a fronteira ética do dono.
- Edições nos blocos compartilhados: aplicar o MESMO texto nos três arquivos de
  prompt, na mesma posição relativa. Os `old_string` abaixo existem verbatim nos
  três arquivos, salvo indicação "(só no viral)" etc.
- Não usar AskUserQuestion (regra global do dono). Dúvida → pergunta em texto.

---

### Task 1: ESSÊNCIA do conteúdo no PASSO ZERO (os 3 prompts)

É o pedido central do dono: quando chegar um conteúdo, o modelo primeiro
EXPLICA O QUE ELE É (retrato fiel), e só então o transforma em conteúdo
individual por público × formato — sem perder a essência.

**Files:**
- Modify: `prompts/fase1-3versoes.md`
- Modify: `prompts/fase1-promocao.md`
- Modify: `prompts/fase1-viral.md`

**Interfaces:**
- Produces: seção `## ESSÊNCIA` como primeira seção do
  `resumo-estrategico.md` gerado em cada rodada (o dono revisa no portão).

- [ ] **Step 1: Inserir o item 0 no PASSO ZERO (×3 arquivos)**

Em CADA um dos três arquivos, localizar:

```
Antes de qualquer roteiro, decida e ANOTE (vai no resumo do fim):

**1. Tese central.**
```

e inserir entre as duas partes (o item 0 entra antes do item 1; a numeração
existente não muda):

```
**0. O que este conteúdo É (a essência).** Antes de decidir qualquer coisa,
descreva o conteúdo recebido em 2–4 frases FIÉIS: o que ele afirma (na intenção
de quem o escreveu), a quem ele fala, e o que ele NÃO é. Retrato, não melhoria
— aqui você ainda não opina, só demonstra que entendeu.

A essência é o contrato de fidelidade do lote inteiro: cada vídeo muda a
EMBALAGEM (gancho, dor, exemplo, formato, fecho — por público e por tipo),
NUNCA a essência. Teste de cada roteiro: quem escreveu o assunto reconheceria a
própria ideia neste vídeo? Se um roteiro só funciona traindo a essência, o
problema é do roteiro — refaça-o a partir dela.

```

- [ ] **Step 2: Atualizar a contagem do portão de erro (×3 arquivos)**

Em cada arquivo, trocar:

```
Se você não consegue escrever os três, o problema é o assunto — declare o
`ERRO:` e pare.
```

por:

```
Se você não consegue escrever os quatro, o problema é o assunto — declare o
`ERRO:` e pare.
```

- [ ] **Step 3: Exigir a ESSÊNCIA como primeira seção do resumo (×3 arquivos)**

Em cada arquivo, trocar:

```
5. Grave também `{{pasta}}/resumo-estrategico.md` com: assunto, tese central,
   motivo para assistir, elemento demonstrável, e — por público — como os três
```

por:

```
5. Grave também `{{pasta}}/resumo-estrategico.md` com: a ESSÊNCIA (item 0 do
   passo zero) como PRIMEIRA seção — é ela que o revisor confere antes de
   julgar qualquer roteiro —, depois assunto, tese central,
   motivo para assistir, elemento demonstrável, e — por público — como os três
```

- [ ] **Step 4: Verificar**

```bash
cd ~/projetos/promoavatar3
grep -c 'O que este conteúdo É' prompts/fase1-3versoes.md prompts/fase1-promocao.md prompts/fase1-viral.md
```
Esperado: `1` em cada arquivo (três linhas de saída terminando em `:1`).

```bash
grep -c 'escrever os quatro' prompts/*.md
```
Esperado: `1` nos três arquivos de variante, `0` em `reel-regras.md`.

- [ ] **Step 5: Commit**

```bash
git add prompts/fase1-3versoes.md prompts/fase1-promocao.md prompts/fase1-viral.md
git commit -m "fase1: passo zero ganha item 0 (essencia do conteudo) nas 3 variantes"
```

---

### Task 2: Dores por público (tabela da skill + flow.json + regra 2)

Hoje a tabela da skill só tem PROMESSAS; a dor de cada público não existe em
lugar nenhum e o modelo a inventa a cada rodada. Pior: o gatilho tabelado do
`40mais` ("Sua experiência vale mais quando é multiplicada pela IA") é
literalmente o exemplo de NÃO-gancho morno citado nos próprios prompts.

**Files:**
- Modify: `.claude/skills/inemaclub-textos/SKILL.md` (tabela, linhas 23–36)
- Modify: `flow.json` (campo `gatilho` dos alvos `40mais-alc`, `40mais-aut`,
  `40mais-pro`)
- Modify: `prompts/fase1-3versoes.md`, `prompts/fase1-promocao.md`,
  `prompts/fase1-viral.md` (regra 2)

- [ ] **Step 1: Substituir a tabela de públicos da skill**

Em `.claude/skills/inemaclub-textos/SKILL.md`, trocar a tabela inteira (do
cabeçalho `| slug | Público | Gatilho / promessa |` até a linha do `familia`,
inclusive) por:

```
| slug | Público | Dor (usar ANTES da solução) | Gatilho / promessa |
|---|---|---|---|
| `pessoa-comum` | Pessoa comum / leigo | Sente que todo mundo está tirando proveito da IA menos ele; medo de ficar para trás até no básico. | Você usa IA do jeito preguiçoso; dá pra fazer muito melhor com truques simples. |
| `jovens` | Jovens | Falta de experiência; medo de escolher profissão que vai sumir; dificuldade do primeiro trabalho; precisar de renda. | Você pode começar uma profissão que ainda está nascendo. |
| `profissionais` | Profissionais | Medo de ser substituído; rotina que come o dia; ver colega mais novo produzir mais usando IA. | Não abandone sua profissão. Aprenda a ampliá-la com IA. |
| `mulheres` | Mulheres | Jornada dupla que não deixa tempo para se atualizar; querer autonomia de renda; voltar ao mercado depois de uma pausa. | Use a IA para conquistar autonomia, produtividade e novas oportunidades. |
| `empreendedores` | Empreendedores | Custo de agência e freela comendo a margem; concorrente entregando mais rápido e mais barato; tempo preso na operação. | Transforme IA em redução de custos, vendas e novos negócios. |
| `tecnicos` | Técnicos | Virou testador de ferramenta da moda; medo de virar mão de obra commodity; tutoriais infinitos sem nunca ter um sistema seu. | Pare de apenas testar ferramentas. Aprenda a construir sistemas e agentes. |
| `40mais` | 40+ | Preterido por gente mais nova; experiência tratada como custo, não como ativo; recomeçar do zero assusta. | O mercado está tratando sua experiência como custo. A IA a transforma de novo em vantagem. |
| `60mais` | 60+ e aposentados | Sentir-se fora do jogo; medo de tecnologia; aposentadoria que não paga as contas; falta de propósito no dia a dia. | A IA pode transformar sua experiência de vida em conhecimento, renda e propósito. |
| `educadores` | Professores e educadores | Aluno usando IA melhor que o professor; medo de virar fiscal de cola; noites consumidas por prova e plano de aula. | Você não vai ser substituído pela IA — mas pode ser o professor que ensina com ela. |
| `criadores` | Criadores de conteúdo | Ferramenta cara demais para o retorno; ritmo de postagem que esgota; ver canal menor crescer mais rápido usando IA. | Pare de pagar ferramenta cara. Monte sua própria fábrica de conteúdo com IA. |
| `recolocacao` | Recolocação / transição de carreira | Currículo ignorado; vaga pedindo o que não tem; a renda acabando enquanto a resposta não vem. | Perdeu o emprego ou quer mudar de área? A IA pode ser o atalho do seu recomeço. |
| `familia` | Pais/família com visão de futuro (formar os filhos) | A escola prepara o filho para o mundo de ontem; medo de ele escolher uma carreira que vai sumir; não saber como orientar. | As formações de hoje não preparam seu filho para o mundo que vem; você (pai/mãe com visão) pode formá-lo em tecnologia, comportamento, gestão e atitude para o próximo momento da IA. |
```

(É a tabela atual + coluna Dor, com UMA promessa alterada: a do `40mais`.)

- [ ] **Step 2: Atualizar o gatilho do 40mais no flow.json**

Nos três alvos `40mais-alc`, `40mais-aut`, `40mais-pro` do `flow.json`, trocar
o valor do campo `gatilho`:

- De: `"Sua experiência vale mais quando é multiplicada pela IA."`
- Para: `"O mercado está tratando sua experiência como custo. A IA a transforma de novo em vantagem."`

São 3 ocorrências; nada mais muda no `flow.json`.

- [ ] **Step 3: Apontar a regra 2 dos prompts para a tabela (×3 arquivos)**

Em cada um dos três prompts, trocar:

```
**2. A dor vem antes da solução, e é a dor DESTE público.** Use o gatilho do
público (o mesmo gatilho vale para os três tipos daquele público). Para jovem:
falta de experiência, medo de escolher profissão que vai sumir, dificuldade de
conseguir o primeiro trabalho, precisar de renda. Genérico não dói.
```

por:

```
**2. A dor vem antes da solução, e é a dor DESTE público.** A dor e o gatilho
de cada público estão na tabela da skill `inemaclub-textos` (colunas Dor e
Gatilho) — use os de lá, não invente outros. O mesmo par vale para os três
tipos daquele público. Genérico não dói: a dor certa é a que este público
reconhece como sua no primeiro segundo.
```

- [ ] **Step 4: Verificar**

```bash
cd ~/projetos/promoavatar3
grep -c 'Dor (usar ANTES da solução)' .claude/skills/inemaclub-textos/SKILL.md   # esperado: 1
grep -c 'vale mais quando é multiplicada' flow.json .claude/skills/inemaclub-textos/SKILL.md prompts/*.md
python3 -c "import json; json.load(open('flow.json')); print('flow.json ok')"
```
Segunda linha esperada: `0` em TODOS os arquivos (a frase morna sumiu do
sistema; nos prompts ela só existia como exemplo negativo "com IA", que fica).
`flow.json ok` confirma JSON válido.

```bash
python3 -c "
import json; d=json.load(open('flow.json'))
assert all(d['alvos'][f'40mais-{t}']['gatilho'].startswith('O mercado') for t in ('alc','aut','pro'))
print('gatilho 40mais ok')"
```

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/inemaclub-textos/SKILL.md flow.json prompts/
git commit -m "publicos: coluna Dor na tabela da skill; gatilho do 40mais deixa de ser a frase morna"
```

---

### Task 3: Oficina de gancho (3versoes e promocao; reforço no viral)

O gancho é o elemento de maior alavancagem dos três tipos. O viral já exige 5
primeiras frases; o padrão e a promocao escrevem de primeira. Portar a oficina
do promoavatar (5 frases, teste da lacuna, máx. 9 palavras).

**Files:**
- Modify: `prompts/fase1-3versoes.md`
- Modify: `prompts/fase1-promocao.md`
- Modify: `prompts/fase1-viral.md` (só o Step 3)

- [ ] **Step 1: Inserir a seção OFICINA nos dois arquivos não-virais**

Em `fase1-3versoes.md` E `fase1-promocao.md`, inserir IMEDIATAMENTE ANTES da
linha `## REGRAS DE ESCRITA (valem para os três tipos, acima da fórmula da skill)`:

```
## OFICINA DE GANCHO (obrigatória, por alvo, antes de escrever a fala)

Para cada alvo, escreva **cinco** primeiras frases diferentes. Não uma. Cinco.
Depois mate quatro e registre no arquivo do alvo (linha `Ganchos descartados:`)
por que cada uma perdeu, em poucas palavras.

**O teste da lacuna** — o único critério que decide: depois de ouvir a frase, a
pessoa PRECISA da próxima para fechar o sentido? Se a frase já se basta, é
afirmação, não gancho. "Sua experiência vale mais com IA" fecha em si — morre.
"Aos 55 ele fez em duas horas o que a agência cobrava três mil" não fecha —
vive.

Tipos que passam no teste: número específico e estranho · contradição ("o mais
experiente é quem mais apanha") · custo ("você está pagando por algo que já
tem") · a ordem direta ("pare de X") · a confissão ("eu errei isso por dois
anos") · o nome inesperado · o prazo curto e concreto (só se vier do assunto —
regra 10 continua valendo).

**Máximo de 9 palavras na primeira frase.** Se não coube, não é gancho, é
introdução.

```

- [ ] **Step 2: Registrar a linha `Ganchos descartados:` na estrutura do arquivo (×2)**

Em `fase1-3versoes.md` E `fase1-promocao.md`, trocar:

```
4. Cada arquivo tem as seções FALA / SOBREPOSIÇÕES / IMAGENS / ESTRUTURA
   exatamente como a skill manda, mais uma linha `Tipo:` e uma linha
   `Formato escolhido:` no topo.
```

por:

```
4. Cada arquivo tem as seções FALA / SOBREPOSIÇÕES / IMAGENS / ESTRUTURA
   exatamente como a skill manda, mais uma linha `Tipo:`, uma linha
   `Formato escolhido:` e uma linha `Ganchos descartados:` (os 4 que perderam
   na OFICINA, com o porquê em poucas palavras) no topo.
```

(As linhas de decisão vêm ANTES do `### FALA` — o portão do bot lê a primeira
seção FALA e ignora o que vem antes, como já faz com `Tipo:`.)

- [ ] **Step 3: Reforçar a oficina que o viral já tem**

Em `fase1-viral.md`, trocar:

```
**O gancho é o vídeo.** Escreva CINCO primeiras frases diferentes antes de
escolher. Anote as cinco no resumo, com uma linha dizendo por que a escolhida
venceu. A primeira frase não pode ser saudação, contexto, "você já pensou" nem
"você sabia".
```

por:

```
**O gancho é o vídeo.** Escreva CINCO primeiras frases diferentes antes de
escolher. Anote as cinco no resumo, com uma linha dizendo por que a escolhida
venceu. A primeira frase não pode ser saudação, contexto, "você já pensou" nem
"você sabia". Aplique o teste da lacuna: depois de ouvir a frase, a pessoa
PRECISA da próxima para fechar o sentido? Frase que se basta é afirmação, não
gancho. **Máximo de 9 palavras na primeira frase.**
```

- [ ] **Step 4: Verificar**

```bash
cd ~/projetos/promoavatar3
grep -c 'OFICINA DE GANCHO' prompts/fase1-3versoes.md prompts/fase1-promocao.md   # esperado: 1 e 1
grep -c 'teste da lacuna' prompts/fase1-viral.md                                  # esperado: 1
grep -c 'Ganchos descartados' prompts/fase1-3versoes.md prompts/fase1-promocao.md # esperado: 2 e 2
```

- [ ] **Step 5: Commit**

```bash
git add prompts/
git commit -m "fase1: oficina de gancho (5 frases, teste da lacuna, 9 palavras) nas 3 variantes"
```

---

### Task 4: Pessoa concreta e frase repetível (regras 15 e 16, ×3)

Os dois dispositivos mais fortes do prompt do promoavatar, agnósticos de
formato, ausentes no promoavatar3.

**Files:**
- Modify: `prompts/fase1-3versoes.md`
- Modify: `prompts/fase1-promocao.md`
- Modify: `prompts/fase1-viral.md`

- [ ] **Step 1: Acrescentar as regras 15 e 16 após a regra 14 (×3 arquivos)**

Em cada arquivo, localizar:

```
**14. Os três tipos do MESMO público não podem se repetir.** Gancho diferente,
estrutura diferente, fecho diferente. Se der para trocar a fala do `-alc` pela
do `-aut` sem ninguém notar, os dois estão errados.
```

e inserir LOGO APÓS esse bloco:

```

**15. Uma pessoa, não um público.** Escreva para UMA pessoa concreta daquele
público, numa situação específica (o cara de 52 anos que foi dispensado, a mãe
que abriu o caderno do filho). Plural genérico ("os profissionais precisam se
atualizar") não gera identificação — e identificação é o que faz marcar alguém
nos comentários. Use a coluna Dor da tabela da skill como matéria-prima.

**16. A última frase decide o compartilhamento.** Ela reconecta com o gancho e
entrega algo que a pessoa consegue REPETIR — uma regra, um princípio, uma
virada. O CTA é a ordem, não o fecho: o fecho é a ideia que a pessoa leva. Sem
ela o vídeo é visto e esquecido.
```

- [ ] **Step 2: Nota viral na regra 16 (só em `fase1-viral.md`)**

Em `fase1-viral.md`, logo após o parágrafo da regra 16 recém-inserido,
acrescentar:

```

(Nesta variante, "pode terminar sem resolver" continua valendo: a frase
repetível pode ser a própria pergunta que fica aberta — desde que seja
repetível, não vaga.)
```

- [ ] **Step 3: Verificar**

```bash
cd ~/projetos/promoavatar3
grep -c '^\*\*15\. Uma pessoa' prompts/fase1-3versoes.md prompts/fase1-promocao.md prompts/fase1-viral.md  # 1,1,1
grep -c '^\*\*16\. A última frase' prompts/fase1-3versoes.md prompts/fase1-promocao.md prompts/fase1-viral.md  # 1,1,1
grep -c 'a própria pergunta que fica aberta' prompts/fase1-viral.md  # 1
```

- [ ] **Step 4: Commit**

```bash
git add prompts/
git commit -m "fase1: regras 15 (pessoa concreta) e 16 (frase repetivel) nas 3 variantes"
```

---

### Task 5: Contradições internas do viral

O arquivo diz "sem marca, sem inema.club" no topo e mantém o `-pro` com CTA
comercial embaixo; manda ignorar as regras 4/6/7/8 e as apresenta íntegras 100
linhas depois; solta a duração e mantém as durações fixas no topo; e o
engajamento binário não exige as opções NA FALA (a falha observada no teste do
dono: o resumo planejou "1 ou 2" e a fala não numerou).

**Files:**
- Modify: `prompts/fase1-viral.md` (somente)

- [ ] **Step 1: Durações no topo**

Trocar:

```
- `-alc` → **alcance** (25–40s): interrompe a rolagem, gera compartilhamento.
- `-aut` → **autoridade** (35–60s): ensina algo concreto, gera salvamento.
- `-pro` → **promocional** (30–45s): liga dor a solução, termina em CTA.
```

por:

```
- `-alc` → **alcance**: interrompe a rolagem, gera compartilhamento.
- `-aut` → **autoridade**: ensina algo concreto, gera salvamento.
- `-pro` → **direção**: liga a dor ao primeiro passo (adaptado nesta variante).

Duração nesta variante: LIVRE entre 15 e 45s, para os três tipos.
```

- [ ] **Step 2: Marcar as regras de venda como não-aplicáveis**

Quatro trocas, uma por regra (o restante de cada parágrafo fica intacto):

- `**4. Benefício antes de mecânica.**` →
  `**4. Benefício antes de mecânica.** *(NÃO SE APLICA nesta variante — regra de venda, liberada em "ESTA VARIANTE É VIRAL".)*`
- `**6. Promessa do tamanho certo.**` →
  `**6. Promessa do tamanho certo.** *(NÃO SE APLICA nesta variante — regra de venda, liberada em "ESTA VARIANTE É VIRAL".)*`
- `**7. Diferencie sem atacar.**` →
  `**7. Diferencie sem atacar.** *(NÃO SE APLICA nesta variante — regra de venda, liberada em "ESTA VARIANTE É VIRAL".)*`
- `**8. CTA imperativo e curto.**` →
  `**8. CTA imperativo e curto.** *(NÃO SE APLICA nesta variante — o CTA aqui é SEMPRE de engajamento, nunca comercial.)*`

- [ ] **Step 3: Reescrever o bloco `-pro` para a variante**

Trocar o bloco inteiro:

```
### `-pro` — promocional (30–45s)

Liga uma dor específica deste público à solução. Pode vender; não pode virar
lista de características.

Escolha UMA abordagem e diga qual: problema e solução · oportunidade e caminho ·
erro e correção · situação atual e transformação · consequência e prevenção ·
desejo e próximo passo · tentar sozinho versus seguir um método.

- Dor específica → consequência de não resolver → solução NOMEADA → benefício → CTA.
- Benefício antes da mecânica.
- Sem promessa de emprego, renda ou resultado garantido.
- Sem "transforme sua vida" e afins.
- UM CTA, para o destino que o assunto indicar (inema.club por padrão).

Critério antes de gravar: *fica claro por que esta solução é o próximo passo?*
Se não, reescreva.
```

por:

```
### `-pro` — direção (adaptado nesta variante)

Aqui vale a regra do topo: **sem marca, sem curso, sem inema.club** — na
variante viral até o `-pro` é de alcance. O que sobra do promocional é a
DIREÇÃO: ligar a dor ao primeiro passo, nomeado, do tamanho de hoje.

- Dor específica → consequência de não agir → PRIMEIRO PASSO nomeado (uma ação
  concreta, não um produto).
- Sem promessa de emprego, renda ou resultado garantido.
- CTA de ENGAJAMENTO — o compromisso público ("escreve nos comentários o que
  você vai fazer esta semana") é o que mais combina com este tipo.

Critério antes de gravar: *a pessoa sabe o que fazer HOJE ao terminar o vídeo,
sem precisar comprar nada?* Se não, reescreva.
```

- [ ] **Step 4: Escolha binária exige as opções NA FALA**

Trocar:

```
- **escolha binária com lado declarado** — "responde 1 ou 2, e não vale ficar em
  cima do muro";
```

por:

```
- **escolha binária com lado declarado** — "responde 1 ou 2, e não vale ficar
  em cima do muro". A FALA tem que dizer O QUE É o 1 e O QUE É o 2, com as duas
  opções numeradas literalmente na locução — "responde 1 ou 2" sem as opções
  nomeadas na fala não obriga ninguém a nada;
```

- [ ] **Step 5: Verificar**

```bash
cd ~/projetos/promoavatar3
grep -n 'inema.club' prompts/fase1-viral.md
```
Esperado: TODAS as ocorrências restantes são proibitivas ("sem... inema.club",
"NÃO cite") ou exemplos dentro de regras marcadas como não-aplicáveis. NENHUMA
instrui a usar o CTA comercial.

```bash
grep -c 'NÃO SE APLICA nesta variante' prompts/fase1-viral.md   # esperado: 4
grep -c 'O QUE É o 1' prompts/fase1-viral.md                    # esperado: 1
grep -c 'LIVRE entre 15 e 45s' prompts/fase1-viral.md           # esperado: 1
```

- [ ] **Step 6: Commit**

```bash
git add prompts/fase1-viral.md
git commit -m "viral: -pro vira direcao sem marca; regras de venda marcadas; duracao livre; binario exige opcoes na fala"
```

---

### Task 6: Cercas éticas do viral

Dois pontos na fronteira: vergonha sem contrapeso e marcação que rotula um
terceiro. A fronteira do dono é "a qualquer custo, mas sem enganar — e sem
humilhar".

**Files:**
- Modify: `prompts/fase1-viral.md` (somente)

- [ ] **Step 1: Contrapeso da vergonha**

Localizar o parágrafo das emoções:

```
medo de ficar para trás · vergonha de já ter percebido e não ter feito nada ·
injustiça ("estão decidindo por você") · perda do que já é seu · orgulho ferido ·
pertencimento ("os que entenderam já estão fazendo") · alívio negado (o conforto
que engana).
```

e acrescentar LOGO APÓS ele (parágrafo novo):

```

Vergonha e orgulho ferido são sempre AUTO-dirigidos — a pessoa consigo mesma,
nunca humilhada por quem fala. Incomodar sem humilhar: se a frase soa como
deboche de quem assiste, troque a emoção.
```

- [ ] **Step 2: Marcação convida, não rotula**

Trocar:

```
- **marcação com motivo** — "marca a pessoa que você sabe que está adiando";
```

por:

```
- **marcação com motivo** — "marca alguém que precisa ver isto". Convite, não
  rótulo: a marcação não pode expor o marcado como "o errado" da história;
```

- [ ] **Step 3: Verificar**

```bash
cd ~/projetos/promoavatar3
grep -c 'Incomodar sem humilhar' prompts/fase1-viral.md          # esperado: 1
grep -c 'que você sabe que está adiando' prompts/fase1-viral.md  # esperado: 0
```

- [ ] **Step 4: Commit**

```bash
git add prompts/fase1-viral.md
git commit -m "viral: vergonha so auto-dirigida; marcacao convida sem rotular o marcado"
```

---

### Task 7: Verificação final e push

**Files:** nenhum novo — só conferência e publicação.

- [ ] **Step 1: Rede de regressão**

```bash
cd ~/projetos/promoavatar3 && python3 -m pytest tests -q
```
Esperado: os 25 testes passando (nenhum testa prompts, mas pega estrago
acidental em `scripts/`/`templates/`).

- [ ] **Step 2: Conferências transversais**

```bash
cd ~/projetos/promoavatar3
# As regras 11/11b (motor do reel, exit 3) NÃO foram tocadas:
grep -c 'exit 3' prompts/fase1-3versoes.md prompts/fase1-promocao.md prompts/fase1-viral.md   # 2 em cada
# flow.json continua referenciando o prompt padrão pelo mesmo nome:
python3 -c "import json; d=json.load(open('flow.json')); assert d['fases'][0]['prompt']=='prompts/fase1-3versoes.md'; print('fase texto ok')"
# Portabilidade (regra do repo): caminho de máquina não entra versionado:
git grep -l "/home/$USER" -- . ; echo "esperado: nada acima"
```

- [ ] **Step 3: Revisão de diff pelo executor**

```bash
git log --oneline master@{u}..HEAD 2>/dev/null || git log --oneline -7
git diff master@{u}..HEAD --stat 2>/dev/null || true
```
Conferir: ~6 commits, tocando SOMENTE `prompts/fase1-*.md`,
`.claude/skills/inemaclub-textos/SKILL.md` e `flow.json`.

- [ ] **Step 4: Push (publicação = push, regra global do dono)**

```bash
git push
```
Se o push falhar por escopo `workflow` do gh (não deve — nada em
`.github/workflows` foi tocado), usar SSH:
`git push git@github.com:inematds/promoavatar3.git`.

---

## Fora do escopo desta rodada (decisões do dono, não fazer sem ele)

- **Renomear `fase1-promocao.md` → `fase1-manifesto.md`**: o nome atual não
  descreve o que a variante faz (estratégia de manifesto). Barato AGORA (nada a
  referencia até a flag `| prompt=` existir no bot), mas é escolha de nome do
  dono.
- **Flag `| prompt=promocao|viral` no bot** (inemaccbot, `resolverOpcoes` em
  `src/gateway/comandos-fluxo.ts`): já desenhada, deferida pelo dono.
- **Portar ao promoavatar (1 formato)**: linha PROVA nas sobreposições, "motivo
  para assistir agora", e as variantes manifesto/viral. A via inversa da
  divergência — caso a caso, como registrado na memória.
- **Alinhar o corpo da skill `inemaclub-textos` aos prompts** (a skill ainda
  descreve "3 versões num arquivo" e CTA comercial obrigatório em toda versão;
  os prompts a sobrescrevem explicitamente, então funciona — mas é dívida).
- **Deduplicar os 3 prompts** (~330 linhas idênticas): o runtime congela UM
  arquivo por fluxo; composição/include exigiria mudança no bot. Até lá, toda
  edição compartilhada é ×3 — este plano já obedece isso.
