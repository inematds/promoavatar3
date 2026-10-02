# PENDENTE — Imagem do topo trocando a cada 2–3 s

Anotado em 2026-10-02 a pedido do dono. **Ainda NÃO aplicado.** É mudança de visual, não correção de bug:
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
