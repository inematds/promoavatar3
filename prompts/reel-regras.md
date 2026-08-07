# Regras do reel do promoavatar

Estas regras nasceram na skill global `reel-edita-inema` em 2026-08-03 e foram
movidas para cá em 2026-08-04, a pedido do dono. O motivo importa: a skill é
**lida ao vivo** e vale para TODOS os domínios na hora — mexer nela mudava o
comportamento de fluxos em andamento e do `promoavatar3`, que a gente decidiu
não tocar ainda. Aqui elas são versionadas, viram snapshot por fluxo e são
revisáveis no portão.

A skill continua responsável pelo que é mecânica de reel (corte, SFX, render).
O que está abaixo é decisão editorial DESTE pipeline.

---

## 1. A imagem 1 é gatilho de atenção, não ilustração

A primeira imagem do topo **é a capa que aparece no feed**: vista pequena,
parada e ANTES de qualquer texto ser lido. Ela carrega a **provocação** — a
tensão, o custo, o absurdo ou a consequência concreta.

**Ilustrar o tema é o erro padrão.** "Pessoa olhando para uma interface azul
brilhante" é o TEMA (IA), não a provocação. Medido em 2026-08-03: cinco imagens
com prompts diferentes caíram todas no mesmo clichê.

Três testes antes de aceitar:

1. **Transferência** — serviria para qualquer outro reel sobre o tema? Então
   está errada. Tem de ser presa a ESTE assunto e ao gatilho DESTE público.
2. **Polegar** — reduzida a 1/4 e sem a headline, ainda provoca uma pergunta?
3. **Tensão** — mostra o que se PERDE, o que QUEBRA, o que fica absurdo? Ou só
   mostra o objeto do assunto? Só o objeto = ilustração = refazer.

**Clichês proibidos:** pessoa de perfil diante de tela/holograma brilhante · HUD
circular · chuva de código estilo matrix · cérebro de circuitos · robô apertando
mão de humano · lâmpada de ideia.

**Prefira:** a consequência concreta, o objeto fora de lugar, a escala
inesperada, o antes/depois no mesmo quadro, o detalhe humano que denuncia a
mudança.

## 2. A faixa da BASE é um PAINEL, não uma legenda

Conferido no reel 229 (2026-08-03): a faixa de 608px estava ~500px vazia, com
uma linha de texto colada no rodapé e um traço solto no meio — leitura de
legenda, não de bloco de design, enquanto o topo parecia pôster. A base é **1/3
da tela**.

- **Ocupe a faixa.** O bloco se distribui na altura, centrado — nunca ancorado
  no rodapé.
- **Duas linhas, tipografia grande**, no peso da manchete do topo. Se o texto
  não enche duas linhas, reescreva o hook — não diminua a fonte.
- **Dê corpo ao bloco:** caixa com fundo, faixa de cor ou imagem esmaecida. O
  topo tem a imagem para dar peso; a base precisa do equivalente.
- **O acento é o MESMO do card do topo daquele segmento.** No 229 o topo era
  âmbar e a base ciano — dois acentos brigando no mesmo quadro.

> Nos templates `diptico` e `imagem-plena` não existe faixa de base: o vazio
> some por estrutura, e esta regra não se aplica.

## 3. Imagens: proporção, seed e modelo

- **O tamanho sai do template** (`preparar.py` resolve): `empilhado-capa` 1088×704 ·
  `diptico` 1088×960 · `imagem-plena` 1088×1920. Gerar fora da proporção e
  deixar o `object-fit` cortar deforma a cena — e nenhum lint pega isso.
- **`--seed-key "<publico>#<N>"`, nunca `--seed` fixo.** Com seed 7 em tudo,
  dois públicos do mesmo assunto saem **gêmeos de composição** (medido: mudou a
  pessoa, não a cena — mesmo enquadramento, mesmo HUD, mesmo gráfico no mesmo
  canto). O `--seed-key` mantém o determinismo e dá composição própria a cada um.
- **NÃO mexa em `--steps`.** O flux2-klein é *step-distilled*; a doc do inemaimg
  diz "piora acima de 4". Testado e descartado.
- **NÃO troque para `flux2-dev`.** Não sobe nesta máquina de propósito; o erro
  500 (`bitsandbytes`) é esperado, não é bug.
- **Imagem enviada pelo dono nunca é cortada** (`arquivo:` na seção IMAGENS):
  cabe inteira, com fundo borrado no resto. `modo: cover` pede o contrário.

## 0. O caminho é UM comando

```
python3 <repo>/scripts/montar-reel.py --avatar <mp4> --ws <workspace> \
    --alvo <publico> --textos <repo>/textos/<REF>/<publico>.md
```

Faz a sequência inteira: preparar → portão 1 → render → revisor → CTA → QC.
Nomes de saída **fixos**: `<ws>/motion/corpo.mp4`, `<ws>/final/reel.mp4`,
`<ws>/qc/mosaico.png`. Exit 0 pronto · 3 algum portão reprovou · 2 erro de
arquivo.

Levantados 7 workspaces do A#22: saíram **7 estruturas diferentes**, a mesma
coisa com três nomes e listas de concat escritas à mão. Não era variação
editorial, era improviso — por isso os nomes agora são do script.

As seções abaixo descrevem o que ele faz por dentro, e os comandos avulsos que
você usa **quando algo reprova**. No caminho feliz você não os chama.

## 4. QC: o determinístico PRIMEIRO, o olho depois

Frame é o item mais caro do job: cada um entra no contexto e é **relido em toda
mensagem seguinte** até o fim. Medido em outra fase do mesmo sistema: um loop de
verificação por imagem levou uma tarefa de 3 min para 13 min e 13,5M tokens.

- **Portão 1, antes de renderizar (~zero):** `lint` + `lint-timeline.py` +
  `verify-cut.py`. Renderizar para descobrir com o olho o que o lint diria de
  graça é o desperdício mais caro da fase.
- **Portões 2 e 3, depois do render, UM comando:**

  ```
  python3 <repo>/scripts/qc-frames.py --video <ws>/motion/out.mp4 --ws <ws>
  ```

  Ele faz o portão 2 inteiro (duração, 1080×1920, os dois streams — não rode
  `ffprobe` à parte, é a mesma checagem duas vezes), escolhe os frames a partir
  do `segmentos.json` (t=0, cada corte depois da transição, o fecho) e verifica
  sozinho o que não precisa de olho: **a imagem do topo trocou em cada corte**
  (medido só na faixa do topo — no quadro inteiro o avatar se mexe e o teste
  passa sempre), nenhum frame preto, nenhum par congelado.

  Exit **0** passou · **3** alguma checagem falhou (a linha `FALHA` diz qual) ·
  **2** erro de arquivo.

- **O que sobra para o olho:** abra **`<out>/mosaico.png`** — uma imagem, não
  dez. `<out>/headline-t0.png` só se precisar julgar legibilidade da manchete.
  **Não use `/watch` nesta fase e não extraia frames com `ffmpeg` na mão**: são
  os dois caminhos caros que o script substitui, e cada frame solto é relido em
  toda mensagem seguinte até o fim do job. Três perguntas, e só elas: a imagem 1
  provoca? a headline lê de relance? o fecho tem o CTA?
- **Rode uma vez só.** Rever a mesma imagem duas vezes não vê nada novo.
- **Portão 4, o revisor — script, não subagente:**

  ```
  python3 <repo>/scripts/revisor.py --video <ws>/motion/<render-final>.mp4 --ws <ws>
  ```

  Re-transcreve o áudio do **render final** (é a única forma de pegar áudio
  perdido ou dessincronizado na montagem), roda `verify-cut.py` e
  `lint-timeline.py`. Exit 0 passa · 3 reprova. **Não spawne subagente revisor**
  — a FASE 5 da skill global não vale aqui (ver `docs/decisoes-reel.md`).

## 5. O que NÃO entra neste pipeline

Três coisas que a skill global manda fazer e que aqui estão fora. Estão
registradas com evidência e caminho de volta em `docs/decisoes-reel.md` — se for
mudar alguma, leia lá antes: as três se apoiam no mesmo pressuposto (o avatar é
**TTS do HeyGen**, não gravação humana) e caem juntas se ele mudar.

- **SFX não entram.** Não gere, não mixe, não crie `sfx/`. Estava na receita e
  não aconteceu em 18 de 18 reels.
- **Legenda: default SEM.** Quem decide é o estúdio. Não inverta por conta
  própria — já se inverteu por acidente uma vez e inutilizou uma medição de
  custo inteira.
- **Corte de repetições não se aplica.** `islands.py` / `cut.py` são para bruto
  gravado por pessoa. `repeticoes=0` em 18 de 18. TTS não tem falso começo,
  blooper nem tomada repetida — e por isso o `revisor.py` trata repetição de
  n-grama como informativa, não como defeito.
