# estilo.md — Folha de marca INEMA (o coração da personalização)

O motor consulta este arquivo em CADA vídeo. É a identidade que substitui o estilo de referência do pacote.

## Paleta
| Papel | Hex |
|---|---|
| Base / fundo | `#0E1116` |
| **Acento** (destaques, palavra-chave, CTA) | `#F5A623` (âmbar) |
| Texto | `#F7F7F2` |
| Apoio frio (opcional, links/dados) | `#7FB0FF` |

O **acento âmbar** é a cor de destaque única. Nada de arco-íris — punch com uma cor só.

## Tipografia
- **Display** (headline do topo, números): grotesca **bold** (ex.: Inter Tight / Archivo / Anton — fonte livre). Peso alto, caixa alta curta.
- **Texto / legenda**: **Inter** (regular/medium).
- Fallback local do ffmpeg: `DejaVuSans-Bold.ttf`.

## Framing — o formato é EMPILHADO (não full/PiP/split comum)
Reel 9:16 (1080×1920) em 3 faixas fixas:
- **TOPO (≈704px):** headline grande impactante **ou** imagem com texto por cima (o gancho). É onde mora a mensagem forte.
- **MEIO (≈608px):** o **AVATAR** (recorte do HeyGen 16:9 → 1080×608).
- **BASE (≈608px):** o **EXPLICATIVO** (16:9 → 1080×608).
- Detalhes de montagem: `references/10-composicao-empilhada.md`.

## Estética e ritmo
- **Enérgica-punchy, ágil.** Cortes seco, sem gordura. Gancho nos primeiros 1-3s (o headline do topo já é o cold open).
- Ar só em conceito denso; no resto, ritmo alto.
- **Que NÃO pareça feito por IA:** sem pílulas "O PROBLEMA / A SOLUÇÃO", sem etiqueta-capítulo genérica, sem template repetido vídeo a vídeo.

## Música / SFX
- **Só SFX sutis** (whoosh/click discretos nos cortes e entradas de texto). Sem música por padrão.
- SFX e qualquer ámbito vêm de **inemavox/dlp** (não inventar fonte). Ver `references/03-sfx-e-qc.md`.

## Texto na tela — regra dura
- Todo texto/legenda/rótulo vai **na altura do peito/microfone**, NUNCA colado na borda inferior (a UI do Reels/TikTok cobre o terço de baixo). No formato empilhado, o corpo do texto do avatar fica sobre a faixa do meio, e o headline no topo.

## Logo
- Sem marca d'água por enquanto (`marca.logo.tiene = false`).

## CTA — fixo em todo reel
- Fecho sempre com: **"Saiba mais no inema.club"** (âmbar sobre base escura). Recurso gratuito, online. Curto, 1-1.5s.
