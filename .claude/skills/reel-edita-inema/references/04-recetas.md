# 04-recetas.md — Tratamentos (identidade INEMA)

Framework universal (não muda): **leia o vídeo → escolha/combine um tratamento → não repita molde fixo.** O esqueleto de 3 faixas (topo/meio/base) é fixo; o TRATAMENTO de cada faixa adapta ao conteúdo. Cores e framing sempre os de `estilo.md` (base `#0E1116`, acento `#F5A623`, texto `#F7F7F2`).

Cada receita: **nome · quando usar · camadas · ritmo · beat sheet exemplo.**

## R1 · Headline-choque (default)
- **Quando:** tese forte, opinião, "a verdade sobre X".
- **Camadas:** TOPO = headline curto caixa-alta em âmbar, animado (entra palavra-chave por último). MEIO = avatar falando. BASE = explicativo apoiando o ponto.
- **Ritmo:** punch alto; headline fecha em ~1.5s.
- **Beat:** 0-2s gancho (headline aparece) → 2-Xs avatar desenvolve, explicativo ilustra → CTA.

## R2 · Imagem-manchete
- **Quando:** o gancho é melhor mostrado (metáfora visual, "olha isso").
- **Camadas:** TOPO = imagem gerada (`gen-imagem.py`, flux2-klein) com um rótulo curto por cima. MEIO = avatar. BASE = explicativo.
- **Ritmo:** ágil; a imagem prende, o avatar explica.

## R3 · Explicativo-forte na base (Modo 2)
- **Quando:** o conteúdo pede um explicativo animado (dados, passo a passo).
- **Camadas:** BASE = vídeo gerado por `video-explicativo`/`hyperframes` (16:9). TOPO = headline. MEIO = avatar.
- **Ritmo:** ar nos trechos densos do explicativo; resto ágil.

## R4 · Painel visual (Modo 3, sem explicativo em vídeo)
- **Quando:** só avatar; sem segundo vídeo.
- **Camadas:** BASE = painel Hyperframes com as **imagens geradas** + rótulos cinéticos entrando no ritmo da fala. TOPO = headline. MEIO = avatar.
- **Ritmo:** cada imagem entra num beat da fala (≤4s por beat, `lint-timeline.py`).

## R5 · Números/dado
- **Quando:** tem uma estatística.
- **Camadas:** TOPO = número grande count-up em âmbar. MEIO = avatar. BASE = contexto do dado.

> O catálogo é aberto: se o vídeo pedir outra coisa, proponha um tratamento novo seguindo o esqueleto e a paleta. Nunca copie estilo de terceiros; nunca use paleta fora da folha de marca.
