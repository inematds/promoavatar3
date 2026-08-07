#!/usr/bin/env bash
# hyperframes SEM passar pelo registry — usa o que já está na máquina.
#
# Por que existe (2026-08-05): `npx --no-install hyperframes` resolve sempre a
# versão LATEST. O upstream publicou a 0.7.94, o cache local ia até a 0.7.92, e
# o `--no-install` recusou — corretamente, porque a regra desta máquina é não
# baixar nada no meio de um job. Cinco reels do A#25 morreram no lint por um
# erro que não tem nada a ver com reel.
#
# É o outro lado da moeda de 2026-08-03: SEM `--no-install`, o npx anuncia
# "package was not found and will be installed" e um agente que leva a sério a
# regra "NÃO MEXA NA MÁQUINA" aborta o job inteiro (A#18, job 237).
#
# Chamar o binário direto do cache resolve os dois: nunca baixa, e não depende
# do que o registry publicou hoje. É o que a regra sempre quis dizer.
#
# Uso: hf.sh <args do hyperframes>       (ex.: hf.sh lint . )
#      HF_VERBOSE=1 hf.sh ...            imprime a versão escolhida no stderr
set -uo pipefail

# A MAIS NOVA que existe no cache. `sort -V` ordena por versão, não por texto:
# sem isso a 0.7.9 ganharia da 0.7.92.
bin=$(ls -d "$HOME"/.npm/_npx/*/node_modules/hyperframes 2>/dev/null \
  | while read -r p; do
      v=$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$p/package.json" | head -1)
      b="${p%/hyperframes}/.bin/hyperframes"
      [ -n "$v" ] && [ -x "$b" ] && echo "$v $b"
    done | sort -V | tail -1 | cut -d' ' -f2-)

if [ -n "${bin:-}" ]; then
  [ -n "${HF_VERBOSE:-}" ] && echo "hf: $bin" >&2
  exec "$bin" "$@"
fi

# Sem nada em cache: mantém o comportamento antigo, que FALHA em vez de
# instalar. Se cair aqui, é problema de ambiente — reporte, não instale.
echo "hf: nenhum hyperframes no cache (~/.npm/_npx) — reporte, não instale" >&2
exec npx --no-install hyperframes "$@"
