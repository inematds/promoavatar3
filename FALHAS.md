# FALHAS

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-10-02 | Legenda presa: `legendas.py` calculava duração "início da próxima − início desta" sem ordenar; ASR fora de ordem gerou duração ≤ 0 em 803 de 1.966 reels (C184: "APARECER" presa sob as palavras seguintes). Reel final saía a ~−20,5 LUFS (concat por cópia sem normalizar) | Ordenar palavras e garantir duração > 0 (2.486 transcripts re-montados: 0 casos); `normalizar_volume` (loudnorm 2 passadas, vídeo copiado) no entregável, conferido em −14 ±1 | prompt |
