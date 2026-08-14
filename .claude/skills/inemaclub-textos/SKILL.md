---
name: inemaclub-textos
description: Fase 1 do pipeline inemaclubpromover — a partir de um ASSUNTO, gera os textos falados (roteiros de short ~35-40s) personalizados por PÚBLICO, 3 versões (ângulos/ganchos) por público, prontos para o HeyGen (fase 2, heygen-avatar-nei-III). Use SEMPRE que o usuário passar um assunto e pedir "gera os textos", "texto para os públicos", "fase 1", "roteiros do assunto X", ou disser "/inemaclub-textos <assunto>". Saída em textos/<slug-do-assunto>/<publico>.md com seções FALA / SOBREPOSIÇÕES / ESTRUTURA.
---

# inemaclub-textos — Fase 1: texto por público

Gera roteiros falados de vídeo curto (TikTok/Reels/Shorts, ~35-40s) sobre um assunto,
personalizados para cada público do INEMA.CLUB. O conteúdo é o mesmo; **o gancho, a
linguagem, o exemplo e a promessa mudam por público**.

## Entrada

- **Assunto** (obrigatório): tema do vídeo (ex.: "loop de auto-correção da IA").
- **Públicos** (opcional): lista de públicos da tabela abaixo, ou "todos". Default se
  não informado: `pessoa-comum` (perguntar em texto livre se quiser mais — NUNCA usar
  AskUserQuestion).
- **Versões**: 3 por público (3 ângulos/ganchos diferentes do MESMO assunto), salvo
  pedido diferente.

## Os 10 públicos (gatilho de atenção de cada um)

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

(11 slugs porque `pessoa-comum` é o público base além dos 10 segmentados; "todos" = todos os slugs.)

## Fórmula obrigatória de cada versão

**Dor → possibilidade → demonstração → trilha gratuita (CTA inema.club).**

Estrutura falada: identificação → promessa → mecânica em até 3 passos → prova →
caso de uso DO PÚBLICO → nome da técnica → CTA.

Regras (método INEMA / roteirista-inema):
- Gancho nos 3 primeiros segundos, com a dor/promessa DO público (usar o gatilho da tabela).
- UMA tese por vídeo. ~35-40s falados (máx ~110 palavras na FALA).
- Linguagem falada, ZERO jargão para públicos leigos (nada de "rubrica", "agente",
  "workflow" fora do público `tecnicos`); "IA" nunca "ÍA".
- Exemplos do cotidiano DO público (ex.: `40mais` → currículo/experiência;
  `empreendedores` → anúncio/vendas; `educadores` → prova/plano de aula).
- Não prometer autonomia total "no próprio ChatGPT"; não afirmar "única do Brasil" —
  usar "uma das mais completas do Brasil" se citar a plataforma.
- CTA único, nomeando um artefato **REAL** que está no inema.club (trilha/curso/
  projeto), nunca "material completo" genérico. Sempre gratuito.
  - **NUNCA invente nome de trilha/curso.** Consulte `catalogo-inema.md` (ao lado
    desta skill) e cite só o que existe lá. Se nada encaixar bem no assunto, use o
    CTA genérico-seguro: "a trilha de IA do seu perfil no inema.club".
- Frase-mãe disponível como fechamento alternativo: "Não importa sua idade ou
  profissão. Existe uma trilha de IA para você no INEMA.club."

## O que é o INEMA.club (usar como base da promessa/CTA)

Três pilares que o roteiro pode explorar (escolher o que servir ao assunto/público):

1. **Fundamentos que valem pra vida.** Muito do conteúdo é FUNDAMENTO — entender
   IA de verdade, não só a ferramenta da moda. Aprendeu uma vez, vale pra sempre:
   como falar, escrever ou andar de bicicleta. A ferramenta muda, o modelo muda —
   quem domina o fundamento se adapta a qualquer novidade. (Ótimo pra públicos com
   medo de "não alcançar" a corrida da IA: `pessoa-comum`, `40mais`, `60mais`,
   `recolocacao`, `educadores`.)
2. **Passo a passo, mão na massa.** Muito conteúdo é prático e guiado — do zero,
   sem pular etapa. Bom pra prometer "você consegue fazer, mesmo começando agora".
3. **Projetos prontos pra copiar.** Vários projetos/ferramentas são só **clonar do
   repositório** e usar — resultado rápido, sem construir do zero. Bom pra
   `empreendedores`, `tecnicos`, `criadores`, `profissionais` (entrega concreta já).

Sempre gratuito; "uma das plataformas gratuitas de formação prática em IA mais
completas do Brasil" (nunca "a única").

## Saída

Um arquivo por público: `textos/<slug-do-assunto>/<slug-publico>.md`, contendo as
3 versões. Cada versão tem:

```
## Versão N — <nome do ângulo>
### FALA (texto para o HeyGen — falar exatamente isto)
<somente o texto falado, limpo>
### SOBREPOSIÇÕES DE TELA (fase do reel — NÃO falar)
<headline do gancho, cards de prova, palavra-chave, CTA fixo "Saiba mais no inema.club">
```

No fim do arquivo, seção `## ESTRUTURA` com a fórmula usada. Ao terminar, listar os
arquivos gerados e indicar que a fase 2 é o `heygen-avatar-nei-III`.

## Não fazer

- Não gerar o vídeo/avatar aqui (isso é fase 2+ do pipeline — ver memória
  `pipeline-inemaclubpromover`).
- Não usar AskUserQuestion (regra global). Perguntas em texto livre.
- Não misturar públicos num mesmo texto.
