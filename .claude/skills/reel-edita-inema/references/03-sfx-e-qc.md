# Fase 4 — SFX, QC e entrega

## SFX (sintéticos, sem baixar nada)

o motor de referência quer SFX sutis, **sem música**. São sintetizados com ffmpeg e mixados em POST (não dentro do Hyperframes — mais simples e desacoplado).

Gere a paleta uma vez por projeto:
```bash
bash ~/.claude/skills/reel-edita-inema/scripts/make-sfx.sh motion/sfx
```
Cria: `whoosh` (transições), `pop` (chips), `type` (digitação no terminal), `buzz` (erro), `boom` (impacto/reveal), `ding` (check / número certeiro), `riser` (subida antes de um reveal).

Mixe os SFX no render com uma lista de eventos `[ [sfx, tempo], ... ]`:
```bash
python3 ~/.claude/skills/reel-edita-inema/scripts/mix-sfx.py \
  --base motion/renders/reel-full.mp4 \
  --sfx-dir motion/sfx \
  --out motion/renders/REEL-FINAL.mp4 \
  --events '[["boom",0.0],["riser",0.2],["whoosh",0.8],["pop",0.98],["whoosh",6.5],["ding",8.6], ...]'
```
Ponha um evento onde houver uma entrada/transição/impacto. Os volumes já vêm baixos (acentos por baixo da voz) e a mixagem aplica um `alimiter` para não saturar. Se você recortar ou ressincronizar, **re-temporize também os eventos** (seus tempos mudam com a duração).

**Impact-landing nas mudanças de seção (v9):** uma transição soa "produzida" quando o whoosh **aterrissa** num golpe curto exatamente no corte. Nas mudanças de seção fortes (e no corte do cold open para o corpo) encadeie `riser`/`whoosh` que sobe → `boom`/`ding` que cai EXATO no frame da mudança: `[["whoosh",t-0.4],["boom",t]]`. Não em cada corte (cansa); só nos beats que marcam seção. SFX sempre por baixo da voz.

## QC: o determinístico PRIMEIRO, o olho depois

**Frame é a coisa mais cara do processo.** Cada frame que você `Read` entra no
contexto e é **relido em toda mensagem seguinte** até o fim do job — 30 frames
não custam 30 leituras, custam 30 × o número de idas ao modelo que ainda faltam.
Medido em outra fase deste mesmo sistema em 2026-08-03: um loop de verificação
por imagem levou uma tarefa de 3 min para 13 min e 13,5M tokens. O gasto não
aparece na hora em que você tira o frame; aparece depois, diluído em tudo.

Por isso a ordem é fixa: **o que uma máquina consegue afirmar, ela afirma antes
de você olhar.**

**PORTÃO 1 — antes de renderizar (custo ~zero):**
```bash
bash ~/.claude/skills/reel-edita-inema/scripts/hf.sh lint motion/index.html          # 0 erros
python3 scripts/lint-timeline.py motion/index.html   # nenhum beat > 4s
python3 scripts/verify-cut.py --media edicion/corte-final.mp4 \
        --transcript edicion/transcript-final.json   # exit 0, quando houve corte
```
Render só depois destes. Renderizar para descobrir com o olho o que o `lint`
diria de graça é o desperdício mais caro da fase.

**PORTÃO 2 — depois do render `standard` (custo ~zero):**
```bash
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate,codec_type \
        -of default=nw=1 motion/renders/reel-full.mp4
```
Duração bate com a fala? 1080x1920? Tem stream de áudio E de vídeo? Um render
truncado ou mudo se descobre aqui, sem olhar nada.

**PORTÃO 3 — só agora o olho, e DIRIGIDO.** Não extraia 30 frames no atacado:
extraia os que decidem alguma coisa.
```bash
python3 ~/projetos/claude-video/skills/watch/scripts/watch.py motion/renders/reel-full.mp4 \
  --no-whisper --max-frames 10 --out-dir motion/qc/watch
```
Os frames que valem: **t=0** (é a capa do feed — regra dura de `08-cold-open.md`),
**cada troca de imagem do topo**, o **fecho/CTA**, e qualquer ponto que o PORTÃO 1
tenha acusado. Se depois de corrigir você precisar reconferir, extraia **só o
frame do ponto corrigido** — nunca a série inteira de novo.
Depois `Read` os frames e revise: **lacunas vazias** no B-roll (preencha-as), **sobreposições** de texto, **sincronia** (cada chip/cena com o que se diz naquele momento), **legibilidade**, que o rosto não fique tapado e que os títulos estejam na altura do micro. Isso revelou na época que as cenas B-roll ficavam meio vazias.

**Checagem de ritmo mensurável (v9):** conte as mudanças visuais (corte, movimento de câmera, aparição de chip, zoom, cena B-roll, reveal) a cada 10s. Alvo: **5-7 mudanças/10s** nos trechos ágeis. <4 = lê-se lento (meta movimento/B-roll); >8 = ruído (tire). **Exceção deliberada:** os trechos "denso → ar" (ver `04-recetas.md`) ficam abaixo de propósito — não os infle à força de cortes.

**🔴 REGRA DURA DE RITMO (o motor de referência, sim ou sim, 2026-06-23): nunca mais de 3-4 s sem que aconteça algo visual.** A cada ≤4 s tem que entrar um beat: animação, B-roll, zoom/punch (`snap`), chip/rótulo cinético, selo, movimento de câmera (PiP/full), reveal ou um float contínuo perceptível. **As legendas NÃO contam** como beat — são base permanente do vídeo, estão sempre presentes, então um trecho com só talking-head + captions = trecho morto mesmo que haja texto na tela. QC obrigatório: percorra a timeline listando os beats não-legenda e meça as lacunas; qualquer lacuna >4 s se preenche (um `snap` ou um selo cinético sincronizado com uma palavra-âncora basta). Caso real: o trecho 59-65 s do reel SpecKit (pós-terminal, só falando) foi preenchido com `snap` + selo "ABISMAL". Ver [[feedback_reel_beat_cada_4s]].

Se você ressincronizou após um recorte, verifique com frames exatos os pontos que se deslocaram:
```bash
for t in 62 75 90 93.4; do ffmpeg -ss $t -i render.mp4 -frames:v 1 -y qc/chk_$t.jpg -loglevel error; done
```

## Render

```bash
bash ~/.claude/skills/reel-edita-inema/scripts/hf.sh render --quality standard --output renders/reel-full.mp4   # para QC
bash ~/.claude/skills/reel-edita-inema/scripts/hf.sh render --quality high     --output renders/reel-full-hi.mp4 # entrega final
```
`draft` para iterar rápido um pedaço; `standard` para revisar; `high` para entregar. O render de ~100s leva ~2 min. Verifique a duração com `ffprobe`.

**Truque de eficiência:** para validar um look novo, renderize só os primeiros ~20s (baixe `data-duration` temporariamente) como proof-of-concept antes de renderizar o minuto e meio inteiro.

## Ordem final da Fase 4

1. `make-sfx.sh` (uma vez).
2. PORTÃO 1 (lint + lint-timeline + verify-cut) → render `standard` → PORTÃO 2
   (`ffprobe`) → PORTÃO 3 (`/watch` dirigido) → corrigir → re-render até polido.
3. Render `high` final.
4. `mix-sfx.py` sobre o render high → `REEL-FINAL.mp4`.
5. **Conferência final: ÁUDIO, não frames.**
   ```bash
   ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name \
           -of default=nw=1 REEL-FINAL.mp4
   ```
   Duração igual à do render `high`, e os dois streams presentes (vídeo + aac).

   **NÃO refaça `/watch` aqui.** `mix-sfx.py` roda com `-c:v copy`: o stream de
   vídeo sai **bit a bit idêntico** ao do render `high` que você já revisou. Uma
   passada visual sobre o final examina pixels que não podem ter mudado, e paga
   por isso o preço de frame descrito no topo desta seção. O que muda é só o
   áudio — e áudio não se confere com imagem.

## Entrega

Deixe `REEL-<slug>-FINAL.mp4` (alta qualidade, 1080×1920) em `motion/renders/`. Avise o motor de referência com o caminho.

**🔴 Ao APROVAR (o motor de referência diz "isso já está bom" / "serve pra mim"): mover o BRUTO para editados.** As pastas de brutos são `Empresa/Videos/Sin Editar/` e `Empresa/Videos/Editados/`. Assim que o motor de referência der o OK final a um reel, mova seu vídeo bruto de `Sin Editar/` → `Editados/` (`mv`, não cópia — é a forma dele de saber o que falta editar). Só ao aprovar, não antes. Ver [[feedback_reel_bruto_a_editados]].

**WhatsApp (só se o motor de referência pedir e confirmar explicitamente — é comunicação externa):**

**Enviar como DOCUMENTO, não como vídeo.** Se enviar como vídeo (`mediatype:"video"`), o WhatsApp recomprime e baixa a resolução (um 2K cai para Full HD). Como documento (`mediatype:"document"`) o arquivo chega intacto. o motor de referência quer máxima qualidade.

Limite de documento no WhatsApp ≈ 100MB. Se o final pesar mais, gere uma versão documento de alta qualidade (visualmente quase sem perda) abaixo do limite, mantendo a resolução do bruto:
```bash
ffmpeg -y -i REEL-FINAL.mp4 -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart REEL-DOC.mp4
# confira o tamanho; se >~95MB suba o crf (20-22). Mantém a resolução original (não reescalar).
```
## Loop de retenção (pós-publicação, v9)

O reel não acaba ao entregá-lo: feche o loop com os dados. Quando o motor de referência publicar, lembre-o (ou revise se ele compartilhou captura de Insights) da **retenção a 3s**:
- Queda no **segundo 1** → o cold open visual/sonoro é fraco (primeiro frame mais forte, mais contraste/impacto).
- Queda no **segundo 3** → parou o scroll mas a **promessa é fraca** (reescrever a frase-gancho do cold open).
- Queda na metade → meta uma mudança visual forte (B-roll, punch-in, rótulo grande) no segundo onde cai.

Isso alimenta o cold open e o ritmo do PRÓXIMO reel. É o mecanismo que sobe o teto a médio prazo. Ver `08-cold-open.md`.

## Entrega por WhatsApp (detalhe)

Envie com a skill `/whatsapp` via Evolution API `sendMedia`, mas com `"mediatype":"document"`, `"mimetype":"video/mp4"` e `"fileName":"REEL-....mp4"`. O base64 do arquivo é enorme: **escreva-o num arquivo temporário e construa o payload JSON em Python**; NÃO passe o base64 como argumento de shell (quebra por comprimento "argument list too long"). Padrão que funciona:
```bash
base64 -i REEL-DOC.mp4 | tr -d '\n' > /tmp/b64.txt
NUM="$EVOLUTION_MY_NUMBER" python3 -c "import json,os;b=open('/tmp/b64.txt').read().strip();json.dump({'number':os.environ['NUM'],'mediatype':'document','mimetype':'video/mp4','fileName':'REEL.mp4','caption':'...','media':b},open('/tmp/wa.json','w'))"
curl -s -X POST \"$EVOLUTION_API_URL/message/sendMedia/$EVOLUTION_INSTANCE\" -H \"apikey: $EVOLUTION_API_KEY\" -H 'Content-Type: application/json' -d @/tmp/wa.json
```
Credenciais em `Empresa/.env.local` (EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE, EVOLUTION_MY_NUMBER).
