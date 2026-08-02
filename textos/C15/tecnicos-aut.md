Tipo: autoridade (aut)
Formato escolhido: desmontagem de um erro

### FALA
Todo agente ou sistema que você constrói chamando um modelo direto no código tem o mesmo bug escondido: acoplamento. Não é acoplamento de módulo, é acoplamento de fornecedor. O prompt, o parser da resposta, o tratamento de erro — tudo fica amarrado ao formato específico daquele modelo. Troque o modelo e você não troca uma linha, você reescreve o sistema. A correção é simples de nomear e chata de fazer: uma camada de abstração entre seu sistema e o provedor. O agente fala com a camada. A camada fala com o modelo, seja ele qual for. Pare de apenas testar ferramentas. Aprenda a construir sistemas e agentes que trocam de modelo por design, não por acidente.

### SOBREPOSIÇÕES
ATENÇÃO (0–2s): "Todo sistema acoplado direto a um modelo tem o mesmo bug escondido"
RETENÇÃO: contagem — "acoplamento em três lugares: prompt, parser, tratamento de erro".
PROVA: tela comparando diagrama "agente → modelo direto" versus "agente → camada de abstração → modelo".
ENGAJAMENTO: "salva isto pra revisar onde seu sistema está acoplado ao provedor."
CTA (fecho): convite leve a seguir/testar — sem venda direta.

## ESTRUTURA
Fórmula: erro técnico (acoplamento disfarçado de integração) → desmontagem (onde ele mora: prompt, parser, erro) → correção nomeada (camada de abstração) → princípio reaplicável (trocar modelo por design, não por acidente) → convite a salvar. CTA leve, sem venda direta, conforme regra do tipo autoridade.
