#!/bin/bash
# Sintetiza a paleta de SFX do reel (sem baixar nada) no diretório de destino.
# Uso: make-sfx.sh <dir-destino>   (por padrão: ./sfx)
# Sutis, sem música. São misturados em pós com mix-sfx.py.
set -euo pipefail
DIR="${1:-sfx}"
mkdir -p "$DIR"

# whoosh — varredura de ruído para transições
ffmpeg -y -f lavfi -i "anoisesrc=d=0.5:c=pink:a=0.7" \
  -af "highpass=f=350,lowpass=f=5000,afade=t=in:st=0:d=0.18,afade=t=out:st=0.28:d=0.22,volume=0.9" \
  -ar 48000 -ac 2 "$DIR/whoosh.wav" -loglevel error

# pop — blip curto para chips
ffmpeg -y -f lavfi -i "sine=frequency=760:duration=0.14" \
  -af "afade=t=out:st=0.03:d=0.11,volume=0.7" -ar 48000 -ac 2 "$DIR/pop.wav" -loglevel error

# type — tique de digitação (terminal)
ffmpeg -y -f lavfi -i "anoisesrc=d=0.045:c=white:a=0.6" \
  -af "highpass=f=1800,afade=t=out:st=0.006:d=0.035,volume=0.7" -ar 48000 -ac 2 "$DIR/type.wav" -loglevel error

# buzz — erro
ffmpeg -y -f lavfi -i "sine=frequency=150:duration=0.35" \
  -af "tremolo=f=28:d=0.85,afade=t=out:st=0.18:d=0.16,volume=0.6" -ar 48000 -ac 2 "$DIR/buzz.wav" -loglevel error

# boom — impacto grave (reveal / transição forte)
ffmpeg -y -f lavfi -i "sine=frequency=68:duration=0.55" \
  -af "afade=t=out:st=0.08:d=0.45,volume=1.0" -ar 48000 -ac 2 "$DIR/boom.wav" -loglevel error

# ding — check / número cravado
ffmpeg -y -f lavfi -i "sine=frequency=1180:duration=0.32" \
  -af "afade=t=out:st=0.05:d=0.27,volume=0.8" -ar 48000 -ac 2 "$DIR/ding.wav" -loglevel error

# riser — subida antes de um reveal (chirp ascendente)
ffmpeg -y -f lavfi -i "aevalsrc='0.5*sin(2*PI*t*(280+780*t))':d=0.65:s=48000" \
  -af "afade=t=in:st=0:d=0.1,afade=t=out:st=0.5:d=0.15,volume=0.5" -ar 48000 -ac 2 "$DIR/riser.wav" -loglevel error

echo "SFX gerados em $DIR:"; ls "$DIR"
