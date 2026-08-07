# 11-worker-mkivideos.md — Rodar/entregar pelo worker (mkivideos)

**mkivideos** (`~/projetos/mkivideos`) é a **fila/worker** de vídeos: recebe um job (via openpcbot/Telegram ou CLI), sobe um agente Claude headless (`claude -p`) que roda a skill, notifica e **entrega no Telegram**. Ele NÃO é uma skill nem um agente em `~/.claude/agents` — é o runner.

## Como esta skill se encaixa
`reel-edita-inema` é uma **skill que o worker roda**, igual a `video-explicativo`. O input do job é o caminho do avatar (e/ou explicativo).

## Enfileirar um reel
```bash
# submete um job que roda esta skill; --enviar entrega o MP4 final no Telegram
mkivideos add reel-edita-inema "/caminho/avatar.mp4" --enviar
```
(Ajuste ao contrato real do `mkivideos add` — ver `~/projetos/mkivideos/README.md`. Se a versão do CLI exigir `--vertical`/`--dest`, passe `--dest ~/projetos/output/reels/<slug>`.)

## Entrada "pelo bot"
Quando o job nasce no **openpcbot**, o vídeo enviado no Telegram já chega como arquivo local; o worker passa esse caminho como input da skill. Trate igual ao "caminho apontado" do `09-modos.md`.

## Entrega
- Preferir a entrega do próprio worker (`--enviar` → Telegram).
- Sempre gravar o resultado em `~/projetos/output/reels/<slug-do-reel>/` também (regra global de output).

## Pré-requisitos do worker (já verificados na Fase B)
`claude` CLI logado · skills em `~/.claude/skills/` · stack de render (Hyperframes/FFmpeg/Chrome/TTS). GROQ e demais keys em `~/projetos/openpcbotv2/.env` (carregar em runtime).
