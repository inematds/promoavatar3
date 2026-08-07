> ⚙️ DOC DE MOTOR (universal). Copiado tal como está pela forja-reel. As cores que você vir nos
> exemplos são PLACEHOLDERS: sua paleta real vive em `references/estilo.md` e sobrescreve o
> `:root`. Não há estilo de ninguém embutido aqui, só a técnica.

# Fases 2-3 — Motion graphics (Hyperframes)

Só se entra aqui com o corte APROVADO (comporta Fase 1). Re-transcreva o corte aprovado para ter os timestamps FINAIS exatos e mapeie cada animação a eles.

## Arranque

```bash
bash ~/.claude/skills/reel-edita-inema/scripts/hf.sh init motion --video corte-final.mp4 --non-interactive
```
Reescreva `motion/index.html` em vertical: root `data-width="1080" data-height="1920"`, `data-duration` = duração do corte. O scaffold sai em 1920×1080, mude isso.

Antes de escrever, leia (uma vez) a skill `hyperframes`: `house-style.md` e `references/video-composition.md` (regras de vídeo que atropelam os instintos de web: preencher o frame, escalas grandes, cor presente, movimento constante).

## Sistema de camadas (z-index)

- `#broll` (z:2): cenas B-roll em tela cheia, `opacity:0` por padrão.
- `#camera` (z:5): o vídeo. **Fica ACIMA do B-roll.**
- `#orbs` (z:9): glows ambientais que pulsam.
- `#ov` (z:10): overlays (tags, chips, stickers).
- `#br_teaser` (z:13) e `#flash` (z:14): hook e flashes de transição.

⚠️ **Gotcha crítico:** o B-roll está ABAIXO da câmera. Se a câmera está em tela cheia, **cobre o B-roll**. Para que um B-roll apareça, a câmera PRECISA estar em PiP (canto). Cada cena B-roll vem acompanhada de `camPiP()`. (Um diagrama pensado como "overlay full-frame" não vai aparecer se a câmera continuar full.)

## A câmera: animar layout, não transform

Para o PiP com borda nítida, **anime `width/height/top/left/borderWidth/borderRadius`** (não `transform: scale`, que escala também a borda e a sombra). O zoom interno (push-in/snap) vai em um wrapper filho `#vidzoom` com `transform: scale`.

```css
#camera { position:absolute; top:0; left:0; width:1080px; height:1920px;
  border:0 solid var(--violet); border-radius:0; overflow:hidden; z-index:5;
  box-shadow:0 28px 80px rgba(0,0,0,.6); }   /* sombra invisível em full-frame, visível em PiP */
#camera video { width:100%; height:100%; object-fit:cover; }
#vidzoom { width:100%; height:100%; transform-origin:50% 42%; }
```
```js
function camPiP(t){ tl.to("#camera",{top:1120,left:606,width:430,height:764,borderWidth:5,borderRadius:36,duration:0.5,ease:"power3.inOut"},t); }
function camFull(t){ tl.to("#camera",{top:0,left:0,width:1080,height:1920,borderWidth:0,borderRadius:0,y:0,duration:0.42,ease:"power3.inOut"},t); }
function floatPiP(t,dur){ tl.to("#camera",{y:"+=16",duration:1.7,yoyo:true,repeat:Math.max(1,Math.round(dur/1.7)),ease:"sine.inOut"},t); } // deriva suave do PiP
```
Snap-zoom em palavras-chave (em trechos full-frame), sobre `#vidzoom`, sem se sobrepor no tempo:
```js
function snap(t){ tl.to("#vidzoom",{scale:1.08,duration:0.18,ease:"power3.out"},t); tl.to("#vidzoom",{scale:1.0,duration:0.34,ease:"power2.inOut"},t+0.2); }
```
**O track de escala de `#vidzoom` é um só**: ordene reveal/push/snap por tempo e que NÃO se sobreponham (dois tweens sobre `scale` ao mesmo tempo = conflito). Durante PiP, deixe `#vidzoom` em 1.0.

## Sistema de estilo (INEMA punchy — paleta da marca, ver references/estilo.md)

```css
:root{ --violet:#F5A623; --blue:#7FB0FF; --amber:#F5A623; --green:#2FE0A2; --red:#FF5470; }
/* ↑ Paleta INEMA: acento = âmbar #F5A623 (--violet e --amber). --blue = apoio frio. */
/* base/fundo #0E1116, texto #F7F7F2. Punch com UMA cor de acento; green/red só status. */
/* fontes integradas: Inter (800/900 para punch) + JetBrains Mono (.mono, metadados/código/números) */
/* fundo B-roll: scene-bg com glows radiais na cor de acento/secundária + grid sutil 64px; nunca cor chapada */
```
- Chips: fundo escuro `rgba(20,16,31,.9)`, borda de acento 2.5px, sombra, peso 800/900, 52-80px. Sobre fundo em movimento precisam desse fundo+borda para legibilidade.
- **Posição de títulos/chips = altura do microfone, NÃO embaixo.** Nas redes a faixa inferior é comida pela descrição/UI. Ancore o contêiner em `top:1040px` (um pouco abaixo do centro, sobre o peito/microfone), nunca `bottom:180px`. O rosto (~y300-1000) fica livre.
- **NÃO coloque pílulas de seção no topo** ("O PROBLEMA / A SOLUÇÃO" com pontinho de cor). É um clichê de IA e denuncia que o vídeo foi feito com IA — o estilo de referência do pacote pede isso fora. Se precisar dar estrutura, faça com o ritmo e os chips de conteúdo, não com rótulos-capítulo genéricos.

## Texto cinético (chips palavra a palavra)

Envolva cada palavra em `<span class="w">` e a palavra-chave em `<span class="w em v">PALABRA<span class="ul"></span></span>` (sublinhado animado). O chip entra como caixa + as palavras em stagger + o sublinhado varre:
```js
function kpop(sel,tin,tout,opt={}){
  tl.fromTo(sel,{opacity:0,y:opt.fromY??52,scale:opt.fromScale??0.92},{opacity:1,y:0,scale:1,duration:0.32,ease:opt.ein??"back.out(1.7)"},tin);
  tl.fromTo(sel+" .w",{opacity:0,y:16},{opacity:1,y:0,duration:0.2,stagger:0.05,ease:"power2.out"},tin+0.07);
  tl.fromTo(sel+" .ul",{scaleX:0},{scaleX:1,duration:0.3,ease:"power3.out"},tin+0.3);
  tl.to(sel,{opacity:0,y:-26,scale:0.97,duration:0.26,ease:"power2.in"},tout);
}
```

## Helpers de motion ampliados (v10 — vocabulário estendido)

Todos esses helpers são deterministas, GPU-safe (`transform`/`opacity`/`filter`/`clip-path`) e são pensados para 1080×1920 com rótulos à altura do microfone.

### `wipe(sel, tin, tout)`
Revela um rótulo com máscara esquerda→direita e barra de luz; use para claims, títulos e nomes de ferramenta.

Markup opcional para a barra:
```html
<div id="title" class="wipe-title">TEXTO CLAVE <span class="sweep"></span></div>
```

```js
function wipe(sel, tin, tout){
  // técnica clássica de wipe, reescrita
  tl.set(sel,{opacity:1,clipPath:"inset(0 100% 0 0)"},tin);
  tl.to(sel,{clipPath:"inset(0 0% 0 0)",duration:0.42,ease:"power3.out"},tin);
  tl.fromTo(sel+" .sweep",{x:"-120%",opacity:0.95},{x:"120%",opacity:0,duration:0.42,ease:"power3.out"},tin);
  tl.to(sel,{opacity:0,duration:0.24,ease:"power2.in"},tout);
}
```

### `typeIn(sel, tin, opt)`
Digitação char a char sem reescrever conteúdo; use em terminais, comandos, URLs e frases curtas.

Markup obrigatório:
```html
<div id="cmd"><span class="ch">n</span><span class="ch">p</span><span class="ch">m</span><span class="caret">_</span></div>
```

```js
function typeIn(sel, tin, opt={}){
  // técnica clássica de typewriter, reescrita
  const step = opt.step ?? 0.04;
  const repeats = Math.max(0, Math.min(opt.repeat ?? 6, 24));
  const chars = gsap.utils.toArray(sel+" .ch");
  tl.set(sel+" .ch",{opacity:0},tin);
  chars.forEach((ch,i)=>tl.set(ch,{opacity:1},tin+i*step));
  tl.fromTo(sel+" .caret",{opacity:1},{opacity:0,duration:0.16,yoyo:true,repeat:repeats,ease:"none"},tin);
}
```

### `flashCut(t, fromSel, toSel)`
Muda de cena escondendo o corte sob um flash branco; use para passar de problema para solução ou de câmera para B-roll.

Requer o `#flash` padrão:
```html
<div id="flash"></div>
```

```js
function flashCut(t, fromSel, toSel){
  // técnica clássica de flash-cut, reescrita
  tl.set("#flash",{opacity:1},t);
  tl.set(fromSel,{opacity:0},t);
  tl.set(toSel,{opacity:1},t);
  tl.to("#flash",{opacity:0,duration:0.12,ease:"power2.out"},t+0.03);
}
```

### `whipOut(sel, t)`
Retira uma camada com whip-pan e blur; use em hypercuts ou para retirar um visual com energia.

```js
function whipOut(sel, t){
  // técnica clássica de hypercut-whip, reescrita
  tl.to(sel,{x:1300,filter:"blur(30px)",opacity:0,duration:0.18,ease:"power4.in"},t);
}
```

### `burstLines(t, opt)`
Linhas manga radiais para impactos; use só em beats fortes, punchlines e mudanças de seção energéticas.

Markup obrigatório (18 linhas, centradas à altura do microfone):
```html
<div id="burstlines">
  <i class="bl" style="--r:0deg"></i><i class="bl" style="--r:20deg"></i><i class="bl" style="--r:40deg"></i>
  <i class="bl" style="--r:60deg"></i><i class="bl" style="--r:80deg"></i><i class="bl" style="--r:100deg"></i>
  <i class="bl" style="--r:120deg"></i><i class="bl" style="--r:140deg"></i><i class="bl" style="--r:160deg"></i>
  <i class="bl" style="--r:180deg"></i><i class="bl" style="--r:200deg"></i><i class="bl" style="--r:220deg"></i>
  <i class="bl" style="--r:240deg"></i><i class="bl" style="--r:260deg"></i><i class="bl" style="--r:280deg"></i>
  <i class="bl" style="--r:300deg"></i><i class="bl" style="--r:320deg"></i><i class="bl" style="--r:340deg"></i>
</div>
```

```css
#burstlines{position:absolute;left:540px;top:1040px;width:1px;height:1px;z-index:12;pointer-events:none}
#burstlines .bl{position:absolute;left:-3px;top:-260px;width:6px;height:520px;background:linear-gradient(to top,rgba(255,194,61,0),rgba(255,194,61,.9));transform:rotate(var(--r)) scaleY(0);transform-origin:50% 100%;border-radius:999px}
```

```js
function burstLines(t, opt={}){
  // técnica clássica de radial-burst-lines, reescrita
  tl.fromTo("#burstlines .bl",{scaleY:0,opacity:opt.opacity ?? 0.9},{scaleY:1,opacity:0,duration:0.42,ease:"expo.out",stagger:0},t);
}
```

### `shake(t, opt)`
Tremida de impacto com amplitude decrescente sobre `#vidzoom`; use em trechos full-frame e não durante PiP.

```js
function shake(t, opt={}){
  // técnica clássica de screen-shake, reescrita
  const amps = opt.amps ?? [-24,20,-15,11,-7,4,-2,0];
  amps.forEach((a,i)=>tl.to("#vidzoom",{x:a,y:a*0.5,duration:0.05,ease:"none"},t+i*0.05));
  tl.to("#vidzoom",{x:0,y:0,duration:0.01,ease:"none"},t+amps.length*0.05);
}
```

### `slotReveal(sel, t, value, opt)`
Número/preço que assenta tipo caça-níquel; use para números de negócio, preços, métricas e comparativos.

Markup obrigatório:
```html
<div id="price"><span class="digit">0</span><span class="digit">0</span><span class="digit">0</span><span class="underline"></span></div>
```

```js
function slotReveal(sel, t, value, opt={}){
  // técnica clássica de slot-machine-reveal, reescrita
  const DIGITS = "0123456789";
  const chars = String(value).split("");
  const nodes = gsap.utils.toArray(sel+" .digit");
  const spins = opt.spins ?? 18;
  const proxy = {p:0};
  tl.to(proxy,{p:1,duration:opt.duration ?? 0.6,ease:"power3.out",onUpdate:()=>{
    nodes.forEach((node,i)=>{
      const finalChar = chars[i] ?? "";
      const lockAt = 0.62 + i*0.06;
      if (proxy.p >= lockAt || !/\d/.test(finalChar)) {
        node.textContent = finalChar;
      } else {
        node.textContent = DIGITS.charAt(Math.floor((proxy.p*spins+i*3)*10)%10);
      }
    });
  }},t);
  nodes.forEach((node,i)=>tl.fromTo(node,{scale:1},{scale:1.12,duration:0.08,yoyo:true,repeat:1,ease:"power2.out"},t+0.48+i*0.04));
  tl.fromTo(sel+" .underline",{scaleX:0,opacity:0.9},{scaleX:1,opacity:1,duration:0.28,ease:"power3.out"},t+0.48);
}
```

### `focusIn(sel, tin, tout)`
Entrada/saída blur-resolve tipo focus pull; use em rótulos sóbrios, citações e palavras-chave.

```js
function focusIn(sel, tin, tout){
  // técnica clássica de blur-resolve, reescrita
  tl.fromTo(sel,{filter:"blur(18px)",opacity:0,scale:1.06},{filter:"blur(0px)",opacity:1,scale:1,duration:0.4,ease:"power2.out"},tin);
  tl.to(sel,{filter:"blur(12px)",opacity:0,duration:0.3,ease:"power2.in"},tout);
}
```

### `fillWord(sel, tin)`
Preenche uma palavra do contorno até o sólido; use para a palavra-chave de uma frase.

Markup obrigatório:
```html
<span id="kw" class="fillword"><span class="outline">FUTURO</span><span class="fill">FUTURO</span></span>
```

```css
.fillword{position:relative;display:inline-block;font-family:Inter,sans-serif;font-weight:900}
.fillword .outline{color:transparent;-webkit-text-stroke:2px var(--violet)}
.fillword .fill{position:absolute;inset:0;color:var(--violet);clip-path:inset(100% 0 0 0)}
```

```js
function fillWord(sel, tin){
  // técnica clássica de outline-to-fill, reescrita
  tl.fromTo(sel+" .fill",{clipPath:"inset(100% 0 0 0)"},{clipPath:"inset(0% 0 0 0)",duration:0.5,ease:"power3.out"},tin);
}
```

### `iris(t, dir, opt)`
Abertura/fechamento circular para transição de seção; use sobre uma cena ou overlay, com anel opcional.

Markup opcional para o anel:
```html
<section id="scene"><span class="iris-ring"></span></section>
```

```js
function iris(t, dir, opt={}){
  // técnica clássica de iris-open, reescrita
  const sel = opt.sel ?? "#iris";
  const from = dir === "open" ? "circle(0% at 50% 50%)" : "circle(75% at 50% 50%)";
  const to = dir === "open" ? "circle(75% at 50% 50%)" : "circle(0% at 50% 50%)";
  tl.fromTo(sel,{clipPath:from},{clipPath:to,duration:opt.duration ?? 0.5,ease:"expo.out"},t);
  tl.fromTo(sel+" .iris-ring",{scale:0.2,opacity:0.85},{scale:1.35,opacity:0,duration:opt.duration ?? 0.5,ease:"expo.out"},t);
}
```

## Vocabulário de easings canônico (coerência entre reels)

Não invente curvas novas por reel; escolha desta paleta. É o equivalente ao dicionário de easings do motor.

| Intenção | GSAP ease | Duração típica | Uso |
|---|---|---|---|
| `snappy` | `back.out(1.7)` | 0.30-0.40s | entradas de chip/rótulo/selo com punch |
| `gentle` | `power2.out` | 0.30-0.50s | fades de cena, aparições suaves |
| `bouncy` | `back.out(2.4)` | 0.30-0.45s | stickers/badges brincalhões, números cravados |
| `glass` | `power3.inOut` | 0.42-0.50s | movimentos de câmera (PiP↔full), transições premium |
| `smooth` | `sine.inOut` | 1.5-3.0s | push-ins/scroll lentos de B-roll, floats |
| saída | `power2.in` | 0.26-0.30s | saídas de elementos (fade/blur out) |

## Hook (0-3s) — o mais importante

Os 3 primeiros segundos decidem o scroll. Movimento imediato. Padrão validado: **teaser do dado mais absurdo em tela cheia que explode e revela o rosto**:
- `#br_teaser` (z:13) full-frame com o dado gigante (ex. "100.000 ⭐ / em uma semana?") que entra com slam (`scale 1.32→1` em 0.16s) + glitch-shake (`x` yoyo) + a pergunta em pop.
- Em ~0.8s explode: `scale→1.5, opacity→0, filter:blur(22px)` + `flash()`, e a câmera se revela com zoom-out (`#vidzoom` `scale 1.3→1.0`).
Alternativas se encaixar melhor: slam tipográfico palavra a palavra, ou micro-trailer de 0.8s com flashes das melhores cenas. Decida conforme o estilo de referência do pacote se estiver em dúvida.

## B-roll desenhado (catálogo, adapte ao conteúdo)

Cada um full-frame com `scene-bg`+`grid`, **preenchido** (8-10 elementos; nada de meio frame vazio — adicione ghost glyph gigante em baixa opacidade, tokens mono de fundo, métricas), e a câmera em PiP. Exemplos usados:
- **Cartão de repo/dado**: card com contador animado (count-up via proxy `{v:0}`→objetivo + `onUpdate` `toLocaleString('es-ES')`), badge, barras `scaleY`, pills.
- **Chat de IA que falha**: balões (user/bot), pontos de "digitando", janela de app que dá glitch em vermelho (erros tipo `TypeError`, `build failed`, 💩). Bom recurso para o "problema".
- **Terminal ao vivo**: janela `spec-kit — zsh` que vai escrevendo comandos um a um (cada linha entra com slide + check verde + tick SFX, cursor que pisca com `repeat` finito). Peça central para enumerações/passos.
- **Reveal/sting**: logo gigante + kicker + badges.
- **Diagrama de fluxo**: nós + seta (A → B).
- **Grade**: grid 2×2 com checks que se encaixam.
- **Endcard CTA**: "EXPERIMENTE" + sua-url + @sua-marca.

Preencha o vão inicial de um B-roll com algo sincronizado ao áudio (ex. se nomeia ferramentas, que apareçam como chips enquanto ele as diz).

## J-cuts / L-cuts (não troque de cena "a machadadas")

O corte de áudio está colado sem pausas, mas as **cenas/B-roll não precisam mudar exatamente no limite da frase**. Para que flua:
- **J-cut** (visual entra ANTES do seu áudio): comece a revelar a cena/chip ~0.15-0.3s antes de a voz dizer a palavra que ilustra → o olho já está lá quando a voz chega.
- **L-cut** (visual sai DEPOIS): mantenha a cena anterior ~0.15-0.3s sobre o início da frase seguinte antes de transicionar.
- Sobreponha assim as entradas/saídas (`kpop` in um tiquinho antes do timestamp, out um tiquinho depois) em vez de alinhar tudo ao milissegundo do corte. Alinhar cada mudança exata ao limite da frase é o que faz um talking-head parecer picotado.

> **Gramática de cortes completa (Hard/J/Zoom/Action Cut):** ver `hyperframes-animation/transitions/cut-grammar.md` — receita de timeline concreta do J-Cut (áudio 0.2-0.5s antes do corte visual) e mapa de onde cada corte já vive no motor. O **Modo 4** (retenção, `09-modos.md`) deve usar ativamente o **J-Cut** na troca de card do topo e o **Zoom Cut** (`snap()` acima) em palavras-chave — não deixe as transições planas.

## Transições e ambiente

- `flash()` (overlay branco que pisca 0.05s) nos cortes fortes; glitch (shake `x` de `#camera`) ao entrar em uma cena tipo "erro".
- Orbs (`#orbs`): 2 glows nos cantos que pulsam (`scale`/`opacity` yoyo, `repeat` finito que cubra a duração).
- Stickers (👀🔥🥄): pop+bounce perto do chip, à altura do microfone.

## Regras Hyperframes (inegociáveis)

Determinista (sem `Math.random()`/`Date.now()`); `gsap.timeline({paused:true})` registrado em `window.__timelines["main"]`; nunca `repeat:-1` (calcule repetições finitas); vídeo `muted` + `<audio>` separado; não animar dimensões do `<video>` (anime o wrapper); overlays = divs normais (sem `class="clip"`) controlados pelo timeline (CSS `opacity:0` de base; `fromTo` para entrar, `to` para sair). Lint + inspect com 0 erros antes de renderizar.
