# Como acrescentar um público

Cinco arquivos, **nenhuma linha de código no bot** e **sem restart** — o
`flow.json` e a `SKILL.md` são lidos do disco a cada fluxo novo.

Escrito em 2026-08-15, quando o sistema tinha 12 públicos e 36 alvos.

## Antes da mecânica: é UM público ou vários?

O que faz o roteiro acertar não é o rótulo, é a **coluna Dor** da tabela da
skill — a regra 2 do prompt manda usá-la antes da solução.

Exemplo real da dúvida: "consultor (contador, financeiro, consultor, mentor)".
A dor do contador ("o cliente acha que meu trabalho é digitar nota, e agora acha
que a IA faz") não é a do mentor ("meu conhecimento não escala além da minha
agenda").

**O teste:** dá para escrever UMA frase de dor que todos reconheçam como sua no
primeiro segundo? Se sim, é um público. Se não, são dois ou mais — e juntá-los
produz exatamente o "genérico não dói" que o prompt existe para evitar.

## 1. O slug

Minúsculas, sem acento, sem espaço e **sem hífen**. Não é estilo: a chave do
alvo vira o nome do arquivo em `textos/`, o título do vídeo no estúdio (por onde
o download casa), o `--alvo` do reel e o `seed-key` das imagens. Foi por isso que
`pessoa-comum` virou `pessoacomum`.

## 2. O canal

Precisa existir a pasta `~/projetos/yt-pub-livesN`. Sem ela o `resolverDestino`
do bot devolve nulo: o reel monta e **não é entregue**. A pasta
`imports/videos` dentro dela não precisa existir — a entrega a cria.

Para ver o que está livre:

```bash
python3 - <<'PY'
import json, os, re
H = os.path.expanduser('~/projetos')
usados = set()
for r in ('promoavatar', 'promoavatar3'):
    usados |= {v.get('canal') for v in json.load(open(f'{H}/{r}/flow.json'))['alvos'].values()}
existe = sorted(int(m.group(1)) for d in os.listdir(H) if (m := re.match(r'^yt-pub-lives(\d+)$', d)))
print('livres:', [f'lives{n}' for n in existe if f'lives{n}' not in usados])
PY
```

## 3. `flow.json` — três alvos

Um por tipo. O `gatilho` é o MESMO nos três (é do público); o que muda entre
eles é o tipo de vídeo. Os `fecho` são padronizados — copie de outro público.

```json
"consultor-alc": {
  "canal": "lives5",
  "gatilho": "<a promessa deste público>",
  "fecho": "ALCANCE — feche com o convite a comentar, marcar alguém ou compartilhar. NÃO use CTA comercial e NÃO cite o inema.club na FALA."
},
"consultor-aut": {
  "canal": "lives5",
  "gatilho": "<a mesma>",
  "fecho": "AUTORIDADE — feche com o princípio do roteiro mais um convite a salvar, seguir ou testar. A marca pode aparecer de leve na FALA."
},
"consultor-pro": {
  "canal": "lives5",
  "gatilho": "<a mesma>",
  "fecho": "PROMOCIONAL — este é o vídeo de conversão: use o CTA comercial completo."
}
```

## 4. `.claude/skills/inemaclub-textos/SKILL.md` — a linha da tabela

`| slug | Público | Dor (usar ANTES da solução) | Gatilho / promessa |`

É a parte que dá trabalho de verdade, e a que decide a qualidade: desde
2026-08-13 a dor sai DESTA tabela e o prompt proíbe inventar outra.

Ajustar também o "(11 slugs porque…)" no fim da tabela.

## 5. `HELP.md` — a lista e os números

Acrescentar o slug na lista dos públicos e corrigir as contagens (12 públicos,
36 alvos) — elas aparecem em mais de um ponto do arquivo.

## 6. O único toque no repo do bot

`src/integracao/promoavatar3.test.ts` crava
`expect(Object.keys(def.alvos)).toHaveLength(36)`. Vira 39, senão a suíte
quebra. **Nenhum código do bot muda.**

## Conferir sem gastar

```
/promoavatar3 assunto qualquer | alvos=consultor-alc | sombra
```

O `| sombra` imprime fase × alvo × fila × tarefa e não enfileira nada. Alvo
inexistente ou canal que não resolve aparecem aqui, de graça. Depois, um alvo
real com `| estudio` antes de rodar em lote.

## No promoavatar (o de 1 formato)

Mesmo desenho, sem os sufixos: um alvo `consultor` no `flow.json` dele e a
linha correspondente na `SKILL.md` dele. Os dois repos são sistemas separados —
acrescentar num não acrescenta no outro.

## O que NÃO acontece

Fluxos já criados seguem com os alvos antigos: a definição é **congelada** na
criação, e é isso que impede um público novo de mudar as regras de um fluxo em
andamento.
