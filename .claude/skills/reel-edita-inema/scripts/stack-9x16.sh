#!/usr/bin/env bash
# stack-9x16.sh — compoe o REEL EMPILHADO (1080x1920) da marca INEMA:
#   TOPO   (0..704)     : headline (imagem PNG com texto)  OU  cartao solido + --headline "texto"
#   MEIO   (704..1312)  : AVATAR   (video 16:9 -> 1080x608)
#   BASE   (1312..1920) : EXPLICATIVO (video 16:9 -> 1080x608)
# Audio = trilha do AVATAR (a fala manda). O explicativo faz loop ate a fala acabar.
# Este e o caminho RAPIDO/deterministico. O caminho COM MOVIMENTO (headline animado,
# legendas) e via Hyperframes — ver references/10-composicao-empilhada.md.
#
# Uso:
#   stack-9x16.sh --avatar av.mp4 --explainer ex.mp4 --out reel.mp4 \
#                 ( --top capa.png | --headline "TEXTO IMPACTANTE" )
set -euo pipefail
AV=""; EX=""; OUT=""; TOP=""; HEADLINE=""
BASE="#0E1116"; ACENTO="#F5A623"
FONT="${REEL_FONT:-/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf}"
while [ $# -gt 0 ]; do
  case "$1" in
    --avatar) AV="$2"; shift 2;;
    --explainer) EX="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --top) TOP="$2"; shift 2;;
    --headline) HEADLINE="$2"; shift 2;;
    *) echo "arg desconhecido: $1" >&2; exit 1;;
  esac
done
[ -n "$AV" ] && [ -n "$EX" ] && [ -n "$OUT" ] || { echo "uso: --avatar --explainer --out (--top|--headline)" >&2; exit 1; }
mkdir -p "$(dirname "$OUT")"

# Banda do topo: imagem dada, ou cartao solido + drawtext (headline quebrado)
TOPCLEAN=""
if [ -z "$TOP" ]; then
  [ -n "$HEADLINE" ] || { echo "de --top IMG ou --headline TEXTO" >&2; exit 1; }
  TOPCLEAN="$(dirname "$OUT")/.top-headline.png"
  # cartao 1080x704 base escura + texto em ambar, centralizado
  ESC=$(printf '%s' "$HEADLINE" | sed "s/:/\\\\:/g; s/'/\\\\'/g")
  ffmpeg -y -f lavfi -i "color=c=${BASE}:s=1080x704" \
    -vf "drawtext=fontfile='${FONT}':text='${ESC}':fontcolor=${ACENTO}:fontsize=76:\
x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=14:text_align=center" \
    -frames:v 1 "$TOPCLEAN" >/dev/null 2>&1
  TOP="$TOPCLEAN"
fi

ffmpeg -y \
  -loop 1 -i "$TOP" \
  -i "$AV" \
  -stream_loop -1 -i "$EX" \
  -filter_complex "\
[0:v]scale=1080:704:force_original_aspect_ratio=increase,crop=1080:704,setsar=1[top]; \
[1:v]scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608,setsar=1[av]; \
[2:v]scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608,setsar=1[ex]; \
[top][av][ex]vstack=inputs=3[v]" \
  -map "[v]" -map 1:a? -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -shortest "$OUT"

[ -n "$TOPCLEAN" ] && rm -f "$TOPCLEAN" || true
echo "OK reel empilhado -> $OUT"
