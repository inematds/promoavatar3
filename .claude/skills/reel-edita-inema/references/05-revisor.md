# Fase 5 — REVISOR (subagente independente, OBRIGATÓRIO antes de entregar)

Objetivo: que o reel **nunca seja entregue** sem que um revisor independente o tenha validado. Historicamente as falhas (silêncios, repetições, dessincronia) chegavam ao motor de referência porque quem monta é o mesmo que revisa. Este passo quebra isso: um subagente que NÃO montou o reel o audita com olhos frescos e dados, e a entrega é bloqueada se não passar.

## Quando

Logo antes da entrega (WhatsApp/master), sobre o **render final** (`renders/REEL-FINAL.mp4`), seu corte (`edicion/corte-final.mp4`) e o `motion/index.html`. Nada é enviado até ter um veredito **PASS**.

## Como disparar

Faça o spawn de um subagente (tool `Agent`, tipo `general-purpose`) com o prompt abaixo. Passe a ele os caminhos reais. O subagente devolve o JSON `{"verdict":"PASS|FAIL","scores":{...},"blockers":[],"warnings":[],"notes":"..."}`. Se `verdict != "PASS"`, **não entregue**: conserte os `blockers` e dispare o revisor novamente. Itere até PASS.

## Prompt do subagente (modelo)

> Você é o REVISOR final de um reel vertical. Você NÃO o montou: seu trabalho é encontrar falhas antes que ele chegue ao motor de referência. Seja estrito; na dúvida, marque BLOCKER.
>
> Arquivos:
> - Render final: `<caminho REEL-FINAL.mp4>`
> - Corte (áudio): `<caminho corte-final.mp4>`
> - Transcript do corte (word-level): `<caminho transcript-final.json>`
> - Timeline Hyperframes: `<caminho motion/index.html>`
>
> Execute e raciocine:
> 1. **Cortes (comporta dura):** rode
>    `python3 ~/.claude/skills/reel-edita-inema/scripts/verify-cut.py --media <corte-final.mp4> --transcript <transcript-final.json>`
>    Se sair com exit≠0 → BLOCKER com o detalhe (silêncios/repetições).
> 2. **Ritmo estático (comporta dura):** rode
>    `python3 ~/.claude/skills/reel-edita-inema/scripts/lint-timeline.py <motion/index.html> --json`
>    Se `errors` não estiver vazio ou reportar algum gap>4s → BLOCKER: "Buraco de ritmo >4s em [a,b] — viola a regra dura; preencha-o antes de entregar".
> 3. **Áudio real:** rode `/watch` (`~/projetos/claude-video/skills/watch/scripts/watch.py`) sobre o render final. Leia sua transcrição independente: a fala flui natural?, há alguma repetição ou frase cortada que o verify-cut não pegou? Qualquer repetição audível → BLOCKER.
> 4. **Sincronia visual:** com os frames do `/watch`, verifique que cada gráfico/cena aparece quando se diz aquilo que ele ilustra (nem antes nem depois). Defasagens notáveis (>0.5s) → BLOCKER.
> 5. **Cold open (0-3s):** o payoff/gancho é compreensível e legível **desde o frame 1**? O titular-hook em cima só é permitido durante o cold open (≤2s); se houver texto em cima DEPOIS de entrar o corpo → BLOCKER. Se o cold open levar imagem IA, ela parece tosca (texto lixo, mãos/olhos estranhos, render hiperbrilhante)? → BLOCKER.
> 6. **Ritmo:** além do lint, nos trechos ágeis há ~5-7 mudanças visuais/10s (nem lento <4, nem ruído >8)? os trechos densos respiram com ar em vez de se atropelarem em cortes? Descompasso claro → WARNING.
> 7. **Legibilidade e sobreposições:** textos que saem, se pisam, ilegíveis, ou duas cenas ao mesmo tempo → BLOCKER.
> 8. **Zero fumaça / dados:** há números/dados na tela (incluído o titular do cold open) que o áudio NÃO diz (inventados)? → BLOCKER. (regra dura do motor de referência)
> 9. **Clichês IA:** pílulas de seção genéricas em cima ("O PROBLEMA/A SOLUÇÃO" com bolinha), etc. → WARNING.
>
> Calcule também um radar `scores` 0-10 (inteiros). Mantenha PASS/FAIL como comporta dura: o radar é informativo e alimenta o Loop de retenção (correlacionar score com retenção-3s), não substitui os blockers.
> - `corte`: 10 se `verify-cut.py` sai com exit 0 e a leitura real flui limpa; baixa a cada repetição, silêncio ou corte estranho.
> - `ritmo`: `10 - nº de gaps>4s*4 - (1 se densidade média <4)`, limitado a 0-10.
> - `sincronia`: baixa com defasagens visual/áudio >0.5s.
> - `legibilidade`: baixa por textos fora de lugar, sobreposições ou safe zone quebrada.
> - `antihumo`: baixa por dados inventados, clichês IA ou afirmações que o áudio não sustenta.
>
> Devolva SOMENTE este JSON:
> `{"verdict":"PASS|FAIL","scores":{"corte":N,"ritmo":N,"sincronia":N,"legibilidade":N,"antihumo":N},"blockers":["..."],"warnings":["..."],"notes":"resumo 1-2 frases"}`

## Regra de entrega

- `verdict == "PASS"` e `blockers == []` → pode entregar.
- Qualquer outra coisa → consertar e re-revisar. Não mandar ao motor de referência um reel com blockers.
- Qualquer gap>4s do `lint-timeline.py` é blocker de ritmo mesmo que o radar tenha boa nota.
- Os `warnings` são comunicados ao motor de referência na mensagem de entrega (não bloqueiam, mas são ditos).
