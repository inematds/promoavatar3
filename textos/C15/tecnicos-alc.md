Tipo: alcance (alc)
Formato escolhido: erro comum

### FALA
Quanta gente já colocou um sistema inteiro em produção chamando a API de um modelo só, direto, sem camada nenhuma no meio? Aí o modelo muda de preço, de limite ou de comportamento — e o sistema quebra em produção, não em teste. Ferramenta open source, gratuita, fechada, não importa: se o seu código fala direto com um provedor só, você não construiu um sistema, construiu uma dependência disfarçada de arquitetura. Pare de apenas testar ferramentas. Aprenda a construir sistemas e agentes que sobrevivem à troca.

### SOBREPOSIÇÕES
ATENÇÃO (0–2s): "Seu sistema em produção pode quebrar porque fala direto com um modelo só"
RETENÇÃO: lacuna aberta em "não importa qual modelo" — fechada em "o problema é a arquitetura, não o provedor".
PROVA: tela comparando código com chamada direta à API (trava se muda) versus código com camada de abstração (troca o modelo sem quebrar).
ENGAJAMENTO: pergunta pros comentários — "seu código chama a API do modelo direto ou por uma camada no meio?"
CTA (fecho): nenhum CTA comercial — só o convite ao comentário.

## ESTRUTURA
Fórmula: erro comum (chamar a API do modelo direto, sem camada) → consequência (quebra em produção quando o modelo muda) → nomeação do risco real (dependência disfarçada de arquitetura) → convite ao comentário. Sem CTA comercial, conforme regra do tipo alcance.
