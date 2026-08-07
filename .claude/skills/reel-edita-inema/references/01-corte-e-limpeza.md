# Fase 1 — Bloquear o corte (determinístico por silencedetect)

Meta: corte ágil (≈60-90s), **sem silêncios no corpo, sem erros, sem uma única repetição**, validado por `verify-cut.py` (exit 0) antes de animar qualquer coisa.

## MÉTODO CANÔNICO (2026-06-21) — scripts, não na mão

Os timestamps do Whisper são imprecisos → cortar por eles deixa silêncios e repetições (falhou 3 vezes). O corte é feito por **ilhas de voz do `silencedetect`** + **última tomada** + **concat sem pausas**, com três scripts:

```bash
# 0) transcrever o bruto UMA vez (word-level). Reutilizar para tudo.
ffmpeg -i bruto.mp4 -vn -ac 1 -b:a 64k -y edicion/bruto-audio.m4a
bash ~/.claude/skills/reel-edita-inema/scripts/transcribe-groq.sh edicion/bruto-audio.m4a edicion/bruto-word.json

# 1) ilhas + proposta última-tomada (silencedetect)
python3 ~/.claude/skills/reel-edita-inema/scripts/islands.py \
  --media bruto.mp4 --transcript edicion/bruto-word.json --out edicion/islands.json
#    -> revise a tabela KEEP/DROP. Corrija na mão em islands.json os DROP que
#       a heurística não pega: bloopers ("droga"), falsas partidas, tangentes, fragmentos.

# 2) montar o corte (cola ilhas sem pausas; pad para dentro do silêncio)
python3 ~/.claude/skills/reel-edita-inema/scripts/cut.py \
  --islands edicion/islands.json --out edicion/corte-final.mp4

# 3) COMPORTA DURA (bloqueante): re-transcrever o corte e verificar
ffmpeg -i edicion/corte-final.mp4 -vn -ac 1 -b:a 64k -y edicion/cf.m4a
bash ~/.claude/skills/reel-edita-inema/scripts/transcribe-groq.sh edicion/cf.m4a edicion/transcript-final.json
python3 ~/.claude/skills/reel-edita-inema/scripts/verify-cut.py \
  --media edicion/corte-final.mp4 --transcript edicion/transcript-final.json
#    exit 0 = PASSA. exit 1 = corrige islands.json (silêncio/repetição que indicar),
#    re-cut.py, re-verifica. ITERA até exit 0. Não anime sem PASS.
```

**Por que funciona:** silencedetect dá limites exatos (sem jitter), colar ilhas elimina as pausas internas de 5-9s (os "muitos silêncios"), e ficar com a última tomada elimina as repetições. A comporta caça o que o olho deixa passar (p.ex. "pronto, aqui está" dobrado após uma pausa longa).

---

## Apoio: conhecimento de padrões (para o ajuste semântico do passo 1)

O abaixo é o detector antigo (`detect-repeats.py`) e os padrões de repetição observados. Útil para decidir os DROP semânticos em `islands.json`, mas o fluxo canônico é islands→cut→verify.

## 1. Transcrição word-level

```bash
ffmpeg -i bruto.mp4 -vn -ac 1 -b:a 64k -y edicion/audio.m4a
bash ~/.claude/skills/reel-edita-inema/scripts/transcribe-groq.sh edicion/audio.m4a edicion/transcript.json
```
(Groq `whisper-large-v3-turbo`, `GROQ_API_KEY` de `Empresa/.env.local`, espanhol, granularidade palavra+segmento. Se o áudio >24MB, fatiar com `ffmpeg -f segment` e concatenar.)

## 2. Detectar repetições, falsas partidas e tomadas dobradas

```bash
python3 ~/.claude/skills/reel-edita-inema/scripts/detect-repeats.py edicion/transcript.json
```
Imprime três coisas:
- **Segmentos quase-duplicados** (near-dup, sim≥0.5) — tomadas repetidas óbvias.
- **Trigramas word-level repetidos** — capturam repetições DENTRO da frase que o nível de segmento não vê. Ignore os que são contexto diferente de propósito (ex.: "github acaba de" em "te dizer" vs "publicar"; "com inteligência artificial" em duas frases). O resto costuma ser repetição real.
- **Palavras arrastadas** (duração >1.5s) — candidatas a tomada dobrada: uma palavra que dura 3-7s quase sempre esconde um silêncio ou que foi dita duas vezes. Confirme com silencedetect.

Para uma palavra arrastada ou uma zona suspeita, olhe a estrutura fala/silêncio:
```bash
ffmpeg -i corte.mp4 -af "silencedetect=noise=-30dB:d=0.18" -f null - 2>&1 | grep silence_start
```
Se você vê fala–silêncio–fala dentro do que o transcript marca como uma palavra/frase → foi dita duas vezes (tomada dobrada) ou reiniciou a frase (falsa partida).

**Padrões reais vistos** (para você saber o que procurar):
- *Tomada dobrada de palavra*: "mastigadinho" dito 2 vezes com um micro-silêncio no meio.
- *Falsa partida*: "O que agora o GitHub te dá bem bastante…" (incompleto) e reinicia "O que agora simplesmente o GitHub te dá bem mastigadinho para que…" (completa).
- *Restatement redundante*: "5 tasks, ou seja, **tarefas**, te faz uma lista programada de **tarefas**" → "tarefas" duas vezes.
- *Tomada com/sem detalhe*: "Grátis, licença MIT…" vs "Grátis e com licença MIT" → fique com a última.
- *Eco no final*: "Faz sentido, né?" … "Né?" repetido.

## 3. Regra de decisão: ÚLTIMA tomada

Diante de qualquer repetição, **conserve a ÚLTIMA tomada completa** e elimine as anteriores (é a heurística que vem no pacote: "normalmente a boa é a final"). Exceção de bom senso: se a última está incompleta e a anterior é a completa, fique com a completa — o critério real é *que não soe repetido e tenha coerência ao ler tudo seguido*.

## 4. Executar o corte

Construa uma lista de **keep-ranges** (segundos sobre o bruto) que exclua as tomadas ruins. Corte com ffmpeg `filter_complex` (trim+concat, re-encode, precisão de frame). Padrão:

```python
# keeps = [(start,end), ...]  em segundos
parts=[f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS[a{i}]" for i,(s,e) in enumerate(keeps)]
concat="".join(f"[v{i}][a{i}]" for i in range(len(keeps)))+f"concat=n={len(keeps)}:v=1:a=1[v][a]"
# ffmpeg -y -i bruto -filter_complex "<parts;concat>" -map [v] -map [a] -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k corte-content.mp4
```

Depois varra os silêncios (inclui pausas internas e mortos longos):
```bash
auto-editor edicion/corte-content.mp4 --margin 0.18s --no-open -o edicion/corte-final.mp4
```

**Cortes no meio da frase (tirar uma repetição dentro de uma frase):** os timestamps do whisper são imprecisos (±0.2-0.3s). NÃO corte às cegas pelo timestamp do whisper — use `silencedetect` para encontrar os limites de silêncio reais em volta do que você quer tirar e corte entre silêncios. Verifique SEMPRE re-transcrevendo (passo 5).

## 5. RE-VERIFICAR (sobre o corte já feito)

```bash
ffmpeg -i edicion/corte-final.mp4 -vn -ac 1 -b:a 64k -y edicion/audio-final.m4a
bash ~/.claude/skills/reel-edita-inema/scripts/transcribe-groq.sh edicion/audio-final.m4a edicion/transcript-final.json
python3 ~/.claude/skills/reel-edita-inema/scripts/detect-repeats.py edicion/transcript-final.json
```
Leia o texto completo do corte do começo ao fim procurando frases reiniciadas ou conceitos repetidos. **Se aparecer qualquer repetição, recorte-a (sobre o corte atual) e volte a re-verificar.** Itera até que `detect-repeats.py` só deixe os falsos positivos de contexto diferente. Só então o corte está limpo.

> Confira a duração: objetivo 1–3 min. Se ficou <1 min, avise (talvez tenha cortado demais).

## 6. COMPORTA — aprovação

Apresente: duração final, nº de cortes, **lista do que foi eliminado e por quê** (cada repetição/erro). Abra o corte para revisão. **Espere o OK explícito.** Não comece a Fase 2 até que o corte seja aprovado. Este é o ponto onde se evita o re-trabalho caro: uma vez que você anima, recortar obriga a re-sincronizar tudo.
