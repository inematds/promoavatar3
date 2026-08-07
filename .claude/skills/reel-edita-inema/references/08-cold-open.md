# 08-cold-open.md — Gancho dos primeiros 1-3s

No formato empilhado, **o gancho é o TOPO** (headline/imagem) que aparece já no frame 0 — não precisa antepor um clipe separado, o gancho está na faixa de cima desde o início. Ainda assim, dê um **movimento de entrada** forte nos 1-3s.

> **REGRA DURA — o frame 0 é a CAPA.** No **`t=0` o vídeo NÃO pode começar com o topo ou a base vazios/pretos.** A primeira imagem do card do topo E o texto (headline no topo, hook na base) já têm de estar **totalmente visíveis e posicionados no frame 0** — porque esse primeiro frame é o poster/thumbnail que aparece na página/feed antes de dar play, e um reel que abre com faixas vazias parece quebrado. O "movimento de entrada" é um **realce sobre algo já presente** (zoom/pan/scale suave da imagem, um pop na headline que já está na tela) — **nunca um fade/slide a partir do nada** que deixe o topo ou a base em branco nos primeiros instantes. Se você usa animação de entrada, ela parte do elemento JÁ renderizado em 100% de opacidade no frame 0, não de opacidade 0. Vale para todos os modos, e é crítico no Modo 4 (capa de impacto).

## Estilos (escolha pelo conteúdo)
1. **Headline-hook (default):** frase-choque curta em âmbar entra no topo com a palavra-chave por último. Ex.: "ISSO **QUEBRA** SEU REEL".
2. **Imagem-hook:** imagem gerada (`gen-imagem.py`) com um rótulo curto. Bom quando a metáfora visual prende.
3. **Número-hook:** estatística grande count-up (R5 das receitas).
4. **Resultado-primeiro:** mostra o "depois" (o reel pronto/efeito) e o avatar explica como chegou lá.

## A IMAGEM 1 é gatilho de atenção, não ilustração

A primeira imagem do topo **é a capa que aparece no feed**. Ela é vista pequena,
parada e ANTES de qualquer texto ser lido. Então ela não ilustra o assunto: ela
carrega a **provocação** do conteúdo — a tensão, o custo, o absurdo ou a
consequência concreta do que o reel diz.

**Ilustrar o tema é o erro padrão.** "Pessoa olhando para uma interface azul
brilhante" é o TEMA (IA), não a provocação. Medido em 2026-08-03: cinco imagens
geradas com prompts diferentes para este pipeline caíram todas no mesmo clichê —
pessoa de perfil diante de holograma ciano, HUD circular, névoa azul. Bonito,
intercambiável, e por isso morto no feed.

Três testes antes de aceitar a imagem 1:

1. **Teste da transferência.** Se essa imagem serviria para qualquer outro reel
   sobre IA, está errada. Ela tem de ser intransferível: presa a ESTE assunto e
   ao **gatilho deste público**.
2. **Teste do polegar.** Reduza mentalmente a 1/4 do tamanho e tire a headline.
   Ainda provoca uma pergunta? Se sem o texto ela vira papel de parede, refaça.
3. **Teste da tensão.** A imagem mostra o que se PERDE, o que QUEBRA, o que fica
   absurdo ou o "depois" chocante? Ou só mostra o objeto do assunto? Só o objeto
   = ilustração = descartar.

**Clichês proibidos na imagem 1:** pessoa de perfil diante de tela/holograma
brilhante; HUD circular; chuva de código estilo matrix; cérebro de circuitos;
robô apertando mão de humano; lâmpada de ideia.

Prefira: a consequência concreta, o objeto fora de lugar, a escala inesperada, o
antes/depois no mesmo quadro, o detalhe humano que denuncia a mudança.

## Regras
- 0-3s TÊM que fisgar: sem "oi, hoje eu vou falar de…". Vai direto no gancho.
- Se antepor um clipe separado (raro aqui), use `ffmpeg concat` **fora** do timeline do Hyperframes (não quebra a sincronia).
- Fecho oposto ao gancho: **CTA "Saiba mais no inema.club"** nos últimos ~1.5s.
- Evite clichê de IA (nada de "O PROBLEMA/A SOLUÇÃO" como pílula).
