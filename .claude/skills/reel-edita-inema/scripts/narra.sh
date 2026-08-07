#!/usr/bin/env bash
# narra.sh — wrapper do inemavox TTS (chatterbox) para a skill reel-edita-inema.
# Voz padrao: rachel (regra global). Para narracao do proprio Nei, passar --nei <N>
# (usa a ref de voz nei<N>.wav). Musica/SFX vem por outra via (inemavox/dlp).
#
# Uso:
#   scripts/narra.sh --text "roteiro..." --out narracao.wav [--lang pt] [--nei 2]
set -euo pipefail
VOX=~/projetos/inemavox
LANG_=pt; TEXT=""; OUT=""; NEI=""
while [ $# -gt 0 ]; do
  case "$1" in
    --text) TEXT="$2"; shift 2;;
    --out)  OUT="$2";  shift 2;;
    --lang) LANG_="$2"; shift 2;;
    --nei)  NEI="$2";  shift 2;;
    *) echo "arg desconhecido: $1" >&2; exit 1;;
  esac
done
[ -n "$TEXT" ] && [ -n "$OUT" ] || { echo "uso: narra.sh --text ... --out ..." >&2; exit 1; }
OUTDIR="$(dirname "$OUT")"; mkdir -p "$OUTDIR"

REF_ARGS=()
if [ -n "$NEI" ]; then
  REF="$HOME/projetos/timesmkt3/media/voice-refs/nei${NEI}.wav"
  [ -f "$REF" ] && REF_ARGS=(--ref "$REF") || echo "aviso: ref nei${NEI} nao achada, usando voz padrao" >&2
fi
# voz default = rachel (chatterbox); tts_direct.py resolve a voz pela config do inemavox
( cd "$VOX" && python3 tts_direct.py --text "$TEXT" --lang "$LANG_" --engine chatterbox "${REF_ARGS[@]}" --outdir "$OUTDIR" )
echo "OK narracao em $OUTDIR (voz: ${NEI:+nei$NEI}${NEI:-rachel})"
