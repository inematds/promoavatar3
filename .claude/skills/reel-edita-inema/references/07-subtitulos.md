# 07-subtitulos.md — Legendas (OPCIONAIS neste perfil)

Legenda é **liga/desliga por vídeo** (`texto.subtitulos = "opcional"`). Pergunte/decida por reel; padrão: ligar quando a fala do avatar carrega a mensagem, desligar quando o visual já diz tudo.

## De onde vem o texto
- **Modo 1 (avatar já gravado):** se houver o roteiro do HeyGen, use-o (mais exato). Senão, transcreva o áudio com Groq (`scripts/captions.py` sobre o transcript) — `01-corte-e-limpeza.md`.
- **Modos 2/3 (texto conhecido):** legende a partir do roteiro; não precisa transcrever.

## Estilo
- Fonte Inter/grotesca, texto `#F7F7F2`, **palavra-chave destacada em âmbar `#F5A623`**.
- Passe as palavras a destacar via `--keywords` do `captions.py`, conforme `texto.keywords_tipo = [conceitos, cifras]` (nomes/números e conceitos fortes).
- **Posição: na altura do peito/microfone** — sobre a faixa do MEIO (avatar), **nunca** no terço inferior (a UI cobre). Este é o ponto mais importante.

## Como aplicar
```bash
python3 scripts/captions.py --transcript edicion/transcript-final.json \
  --keywords "palavra1,palavra2" --accent "#F5A623" --out motion/legendas.json
```
Depois integre as legendas como camada no Hyperframes na altura do peito.

## Modo 4 — legenda karaoke (palavra-a-palavra)
No Modo 4 (`09-modos.md`) a legenda não é por frase: é **uma palavra por vez**, trocando no ritmo da fala (estilo karaoke/caption viral), sempre na mesma posição na altura do peito. **Tamanho contido (pequeno):** a palavra deve ser legível mas discreta — NÃO dominar o frame nem cobrir o rosto do avatar. Mire uma altura de fonte de ~**3,5-4,5%** da altura do frame (≈**70-85px** num canvas de 1920) e largura máxima de ~**45%** do frame; se a palavra estourar essa largura, reduza a fonte para caber. Evite qualquer coisa próxima de "gigante" — a legenda é um apoio, não protagonista (as duas primeiras versões saíram grandes demais). Caixa/realce discretos, sem fundo pesado. Use os timestamps word-level do transcript (Groq) direto — cada palavra é seu próprio evento de entrada/saída na timeline do Hyperframes, sem agrupar em frase. Mantém o destaque de palavra-chave em âmbar (ou o acento livre escolhido pro card daquele segmento) só quando a palavra em cena for a palavra-chave; senão texto padrão. Isso é intencionalmente diferente dos Modos 1-3 — não aplicar retroativamente a eles.
