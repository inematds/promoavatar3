# 09-modos.md — Os 4 modos de operação

A skill sempre entrega um **reel empilhado** (topo headline/imagem · meio avatar · base explicativo). O que muda é **de onde vêm as peças**. Detecte o modo pelo que o usuário fornecer; na dúvida, pergunte.

## Entrada (origem das peças)
Flexível, nesta ordem de precedência:
1. **Caminho apontado** pelo usuário (pasta/arquivo).
2. **Diretório atual** (procura o(s) MP4 16:9).
3. **Job do worker** (openpcbot → `mkivideos`): o input chega como caminho no job. Ver `references/11-worker-mkivideos.md`.

Saída SEMPRE em `~/projetos/output/reels/<slug-do-reel>/` (nunca toca no bruto).

---

## Modo 1 — COMPOR (você dá as duas peças)
Entrada: **avatar 16:9** + **explicativo 16:9**.
1. (Opcional) Limpar o corte do avatar se tiver silêncios/erros — motor FASE 1 (`01-corte-e-limpeza.md`). Renders HeyGen limpos geralmente pulam isso.
2. Gerar o **headline do topo**: texto forte OU imagem-com-texto (`references/08-cold-open.md` + `06-broll.md`).
3. Compor empilhado (`references/10-composicao-empilhada.md`).
4. Legenda opcional (`07-subtitulos.md`), SFX sutis, CTA. QC + revisor.

## Modo 2 — GERAR O EXPLICATIVO (você dá só o avatar)
Entrada: **avatar 16:9** (a fala/narrativa).
1. Extrair o **texto narrado** do avatar: se você tem o roteiro original, use-o; senão transcreva (Groq) — `01-corte-e-limpeza.md`.
2. Gerar o **vídeo explicativo** a partir desse conteúdo **reusando as skills existentes**:
   - `video-explicativo` (PT-BR, cenas animadas) — caminho preferido para explicativo narrado; ou
   - `hyperframes` diretamente para motion mais custom.
   > A skill-filha **chama** essas skills (não reimplementa um gerador). O explicativo sai 16:9 para encaixar na faixa de baixo.
3. Depois: mesmo caminho do Modo 1 (headline + compor + legenda + SFX + CTA).

## Modo 3 — GERAR OS VISUAIS (você dá o avatar, eu crio imagens+textos)
Entrada: **avatar 16:9**.
1. Ler o conteúdo do avatar (roteiro/transcrição).
2. Gerar **imagens** (`scripts/gen-imagem.py` → inemaimg/flux2-klein) e **textos/rótulos** para o topo e para a base (quando não houver explicativo em vídeo, a base pode ser um painel visual animado no Hyperframes com as imagens geradas).
3. Compor empilhado, legenda opcional, SFX, CTA. QC + revisor.

## Modo 4 — CAPA DE IMPACTO (retenção/engajamento)
Entrada: **avatar 16:9** (o mesmo ponto de partida do Modo 3), mas o objetivo muda: aqui o alvo **não é consistência de marca — é gatilho de atenção, retenção e engajamento**. É o modo a usar quando o reel precisa parar o scroll e prender até o fim, mais do que "parecer INEMA".

**Princípio-guia (não negociável neste modo): mais importante do que as cores da marca é o gatilho de atenção/retenção/engajamento.** Isso muda duas coisas em relação ao Modo 3:
- **Cores são LIVRES.** Não trave em âmbar/`#0E1116` (`estilo.md` permanece a referência default para os outros 3 modos, mas aqui é ponto de partida, não regra). Escolha a paleta que maximiza impacto visual PARA ESTE conteúdo (ex.: azul/ciano + amarelo, vermelho/preto, o que o gancho pedir) — decida por vídeo, não fixe uma paleta única do canal.
- **A imagem do topo TROCA por segmento** — como o Modo 3 já faz para tracking de conteúdo, mas aqui ela é a CAPA (imagem impactante + headline-choque sobreposta em cima dela), não um painel neutro.

Passo a passo:
1. Extrair o **texto narrado** do avatar (roteiro original se houver; senão transcreva — `01-corte-e-limpeza.md`).
2. **Segmentar a narração** pelos pontos onde o assunto/ângulo muda (igual ao rastreamento de conteúdo do Modo 3). Cada segmento vira **um card de topo**: uma imagem impactante (`scripts/gen-imagem.py`, seed fixo, prompt sem texto embutido — texto entra como camada no Hyperframes) + uma **headline curta e forte sobreposta na imagem** (pergunta, tensão ou gap de curiosidade — ex.: "SITES VÃO MORRER?" — ver estilo de gancho em `08-cold-open.md`, estilo 1/2). A imagem TROCA a cada novo segmento — é o motor de re-hook contínuo, não só do 0-3s.
3. **Avatar (faixa do meio):** igual aos outros modos (recorte 16:9→1080×608, áudio mestre), mas as **legendas são PALAVRA-A-PALAVRA (karaoke)** — uma palavra grande na tela por vez, sincronizada à fala — em vez das legendas por frase dos Modos 1-3. Ver nota em `07-subtitulos.md` ("Modo 4 — legenda karaoke").
4. **Base (faixa de baixo):** um **hook curto em texto** (a "isca" que sustenta a curiosidade aberta pelo headline do topo — não repete o headline, empurra pra frente: o porquê de continuar assistindo).
5. **Fecho:** CTA fixo "Saiba mais no inema.club" (igual a todos os modos, `estilo.md`).
6. Compor empilhado (`references/10-composicao-empilhada.md`, nota "Modo 4 — capa de impacto"), SFX sutis (`03-sfx-e-qc.md`), QC + revisor (`05-revisor.md`) — aplique o reviser normalmente, mas ao avaliar "clichê de IA" e "cores fora da marca", lembre que neste modo cor livre e headline-choque são **intencionais**, não defeito; o revisor deve seguir travando repetição/silêncio/dessincronia/dado inventado, não a paleta.

**Gatilho de detecção do modo:** ver `SKILL.md`/`11-worker-mkivideos.md` — palavras como **capa, impacto, viral, retenção, gancho** no input do job, ou a flag `capa` do bot. Não muda a detecção dos Modos 1-3 (essas continuam por peças fornecidas: avatar+explicativo = Modo 1; só avatar sem sinal de Modo 4 = Modo 2 ou 3 conforme o pedido).

---

## Regras comuns a todos os modos
- Avatar 16:9 é sempre recortado para a faixa do meio (1080×608); a fala do avatar é o **áudio mestre** do reel.
- Voz gerada (modos 2/3, quando precisar narrar algo novo) = **inemavox** (`scripts/narra.sh`, voz `rachel`; `--nei N` se for a persona do Nei).
- Imagens = **inemaimg** (`scripts/gen-imagem.py`). Nunca fal/agnes.
- Tratamento proposto conforme o conteúdo — não aplicar molde fixo (só o esqueleto de 3 faixas é fixo).
- **Exceção:** no Modo 4 a paleta de `estilo.md` é ponto de partida, não regra — cor é livre em nome do gatilho de atenção/retenção (ver Modo 4 acima). Os outros 3 modos seguem `estilo.md` à risca.
