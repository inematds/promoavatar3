# Imagem do topo trocando a cada 2–3 s — OPÇÃO pronta, padrão pendente

Anotado em 2026-10-02 a pedido do dono. **Implementado como opção no mesmo dia (desligada por padrão)**; falta o dono decidir se vira padrão. É mudança de visual, não correção de bug:
muda o reel que o dono aprova e dobra o número de imagens por reel.

## O que foi medido

- A imagem do topo fica no ar ~6,3 s em mediana (1.996 manifestos, 01/10/2026).
- No C184-tecnicos-pro (`qa_short.py --layout empilhado` do makeshorts 1.2.0) ficou parada por 9,0 s, 5,5 s,
  **16,2 s** e 9,5 s.
- O "pulso de brilho" (`pulso_max_s`) evita quadro congelado, mas não é imagem nova. Medido: o pulso dá
  diferença de 4–5 na faixa de cima e a troca real dá 19–142.
- Pesquisa de 2026 (blogs, fonte fraca) e o pedido do dono para os virais: troca visual a cada 2–4 s.
- Relatórios: `~/projetos/wifi/MELHORIAS-VIRAIS-2026-10-01.md` e
  `~/projetos/makeshorts/.claude/skills/makeshorts/references/aprendizados-2026-10.md`.

## Onde mexer (quando aprovado)

1. **Prompt:** `prompts/fase1-3versoes.md:213`. Hoje são "6 a 10 segmentos" por roteiro; para 45–50 s a
   2–3 s, são ~15–20 imagens. Alternativa mais barata: cada segmento ganha 2–3 imagens (variações de
   ângulo/plano da mesma cena), em vez de dobrar os segmentos da fala.
2. **Tempos:** `scripts/preparar.py:83` (`MIN_CARD = 1.5`) e a distribuição dos cortes. Os cortes hoje
   seguem o início do segmento no transcript; seria preciso subdividir o segmento.
3. **Template:** `templates/empilhado-capa.json:62` (`pulso_max_s: 3.6`). Manter o pulso só como rede de
   segurança, não como a "troca".
4. **QC:** usar `qa_short.py --layout empilhado` do makeshorts (avisa a imagem do topo parada > 3,5 s) ou
   portar a mesma medição para `qc-frames.py`.

## Custo

- Imagens: o dobro de chamadas ao flux2-klein local (GPU, sem custo em dinheiro; ~2× o tempo de imagem por
  reel).
- Prova real: aproveitar para trocar 1 em cada 3 imagens por material real (print do curso no inema.club,
  tela da ferramenta), que é a outra melhoria pendente da mesma análise.

## Como validar antes de lote

1 reel de teste (mesmo roteiro, versão atual × versão 2–3 s) lado a lado para o dono escolher. Depende do
render do HyperFrames voltar a funcionar: em 2026-10-02 ele falhava com "socket hang up"
(`~/projetos/wifi/LIMITES.md`).

## Implementado (2026-10-02) — opção `--troca-s`

```
python3 scripts/montar-reel.py ... --troca-s 2.5
```

- `preparar.py`: cada segmento maior que N s ganha até 4 **variações da mesma cena** (mesmo prompt + outro
  enquadramento: "closer framing", "wide establishing shot", "detail shot"; seed `<alvo>#<n>v<j>`), repartindo o
  tempo do segmento; nenhuma fatia menor que 1,5 s. Imagem enviada pelo usuário não ganha variação.
  `plano_variantes()` tem testes em `tests/test_troca_rapida.py`.
- `montar.py`: as variações entram como cards extras no mesmo segmento (troca suave de 0,45 s, sem flash e sem
  headline nova); o pulso de brilho passa a valer por card.
- Sem `--troca-s` nada muda (0 = comportamento de sempre).

**Medido no C184-tecnicos-pro** (`qa_short.py --layout empilhado` do makeshorts):

| | Antes | Com `--troca-s 2.5` |
|---|---|---|
| Mediana da imagem do topo | 6,3 s (lote) / 5,5 s (C184) | **3,0 s** |
| Maior trecho parado | **16,2 s** | 4,8 s |
| Imagens geradas | 6 | 6 + 14 variações (flux2-klein local) |

Vídeos para comparar: `~/projetos/output/promoavatar3/teste-troca-imagem-2026-10-02/`
(`…-ANTES.mp4` × `…-DEPOIS-troca-2.5s.mp4`).

**Pendente:** o dono assistir os dois e decidir se `--troca-s 2.5` vira padrão no `flow.json`.
