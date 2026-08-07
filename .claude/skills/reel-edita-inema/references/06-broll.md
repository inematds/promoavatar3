# 06-broll.md — Imagens e assets (identidade INEMA)

B-roll real por captura de site (firecrawl) está **desligado** neste perfil. As fontes visuais são:

## 1. Imagens geradas — inemaimg (flux2-klein)
```bash
# imagem da FAIXA DO TOPO (a faixa é 1080x704 no stack-9x16.sh)
python3 scripts/gen-imagem.py --prompt "PROMPT visual, estetica escura, acento ambar" \
  --out motion/topo-2.png --seed-key "jovens#2" --width 1088 --height 704
```
- Servidor local: `http://localhost:8000` (checar `localhost:8000/health` antes).
- **Use `--seed-key "<alvo>#<segmento>"`, não `--seed` fixo.** Continua
  determinístico (mesma chave → mesma imagem, o reel re-renderiza igual), mas
  cada público/segmento ganha composição própria. Com `--seed 7` em tudo, dois
  públicos do mesmo assunto saem **gêmeos de composição** — medido em
  2026-08-03: mudou a pessoa, não a cena (mesmo enquadramento, mesmo HUD no
  mesmo lugar, mesmo gráfico no mesmo canto). É o oposto de "não repita molde".
- **Gere já na proporção do destino.** Sem `--width/--height` a imagem sai
  `1024x1024` e o `crop` central da faixa come ~35% da altura — pixels jogados
  fora e enquadramento entregue à sorte. Para o topo: `--width 1088 --height 704`
  (medido em 2026-08-03: 5,0s contra 6,7s do quadrado, porque são menos pixels).
  Limites do klein: 128–2048, múltiplos de 16.
- **NÃO mexa em `--steps`.** O flux2-klein é *step-distilled*: a doc do inemaimg
  diz "piora acima de 4". Subir para 24 não melhora, só troca a imagem e custa 5x
  o tempo — testado e descartado em 2026-08-03.
- **NÃO troque para `flux2-dev`.** Ele não sobe nesta máquina de propósito: dá
  500 (`PackageNotFoundError: bitsandbytes`) e carregá-lo atrapalha a GPU. É
  decisão do dono, não bug.
- Prompt no clima da marca: fundo escuro (`#0E1116`), destaque âmbar, sem texto embutido na imagem quando o texto for entrar por cima no Hyperframes (evita texto torto de IA). Se quiser "imagem COM texto", peça o texto no prompt curto e legível, ou (melhor) ponha o texto como camada no Hyperframes.

## 2. Assets próprios do usuário
- Se o usuário entregar imagens/clipes (pasta apontada), use-os direto — **assets reais têm prioridade** sobre gerados.
- Nunca inventar logo/print de marca; se precisar de um print real e não houver, peça ou omita.

## 3. Posicionamento
- Imagem no **TOPO** (faixa do gancho) ou como **painel na BASE** (Modo 3).
- Recorte para a faixa: `object-fit: cover` no Hyperframes, ou `crop` no ffmpeg.
