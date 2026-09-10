#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera os 36 roteiros (12 públicos x alc/aut/pro) de C#171 — gestão de IA
(pessoas + processos + agentes, o novo gestor híbrido), variante viral."""
import os

BASE = "/home/nmaldaner/projetos/promoavatar3/textos/C171"
os.makedirs(BASE, exist_ok=True)

# essência (tese central desta rodada, usada em todas as versões):
# "Quem só USA ferramenta de IA vai ficar para trás de quem aprende a
#  GERENCIAR agentes de IA como parte de uma equipe — pessoas + agentes +
#  processos + ferramentas + dados. Gestão de IA vira uma competência nova,
#  parecida com gestão de pessoas e de processos, mas não é nenhuma das duas."

PUB = {
    "40mais": dict(
        pessoa="Marcos, 47 anos, gerente de área há doze",
        cena="viu um colega mais novo, sem cargo de chefia, entregando o resultado de uma equipe inteira sozinho, com ajuda de agentes de IA",
        dor="ver a experiência de gestão virar peso e não vantagem diante de quem 'orquestra' em vez de mandar",
        chave="experiência de gestão",
    ),
    "60mais": dict(
        pessoa="Dona Vera, 63 anos, foi supervisora a vida toda",
        cena="o neto comentou que hoje 'gerente também gerencia robô', e ela ficou sem saber se aquilo valia pra ela",
        dor="achar que gerir algo com IA é assunto de gente nova, não de quem já geriu gente a vida toda",
        chave="experiência",
    ),
    "criadores": dict(
        pessoa="Duda, cria conteúdo sozinha há três anos",
        cena="percebeu que passa o dia fazendo tarefa que um agente de IA bem orientado faria em minutos, porque nunca aprendeu a delegar pra um",
        dor="trabalhar como um funcionário da própria produção, em vez de gerir uma equipe de agentes",
        chave="produção",
    ),
    "educadores": dict(
        pessoa="Professor Ivo, dezoito anos de sala de aula",
        cena="viu a coordenação pedir pra 'usar mais IA' sem nunca explicar o que muda em como ele organiza o próprio trabalho",
        dor="receber a ordem de usar IA sem entender que o papel dele virou outro: orientar, não só operar",
        chave="orientação",
    ),
    "empreendedores": dict(
        pessoa="Renata, dona de uma loja pequena, três funcionários",
        cena="contratou mais uma pessoa pra dar conta da demanda, quando um agente de IA bem definido resolvia a mesma fila de tarefas",
        dor="contratar gente pra função que já dá pra orquestrar com agentes, gastando o que não precisava gastar",
        chave="equipe",
    ),
    "familia": dict(
        pessoa="Sandra, mãe de um menino de catorze anos",
        cena="ouviu o filho falar em 'ter uma equipe de agentes de IA' um dia, e não fazia ideia do que isso realmente quer dizer",
        dor="não saber orientar o filho pra uma competência que nem o mercado de hoje nomeou direito ainda",
        chave="futuro",
    ),
    "jovens": dict(
        pessoa="Kaique, 19 anos, ainda sem o primeiro emprego",
        cena="viu uma vaga júnior pedindo pra 'coordenar fluxos com agentes de IA', e não sabia nem o que aquilo significava",
        dor="competir por uma vaga júnior que já exige um tipo de gestão que ninguém explicou pra ele",
        chave="coordenação",
    ),
    "mulheres": dict(
        pessoa="Camila, dois filhos pequenos, voltando ao mercado",
        cena="leu 'gerenciar fluxos híbridos de trabalho' numa vaga que antes só pedia organização, e sentiu que o alvo mudou de lugar",
        dor="achar que gerir algo com IA exige um curso longo, quando o que falta é aprender a lógica",
        chave="autonomia",
    ),
    "pessoacomum": dict(
        pessoa="Zé, 35 anos, usa IA só pra escrever mensagem",
        cena="ouviu um amigo dizer que 'administra três agentes de IA' no trabalho, e não entendeu se isso era força de expressão",
        dor="sentir que enquanto ele só pede coisa pra IA, tem gente já dirigindo um time inteiro dela",
        chave="direção",
    ),
    "profissionais": dict(
        pessoa="Bruno, dez anos de carreira na mesma área",
        cena="foi chamado numa reunião onde o chefe descreveu 'gerenciar agentes' como se todo mundo ali já soubesse fazer isso",
        dor="perceber que o cargo dele mudou de conteúdo sem ninguém avisar formalmente",
        chave="cargo",
    ),
    "recolocacao": dict(
        pessoa="Patrícia, seis meses desempregada, currículo em todo lugar",
        cena="leu numa entrevista que a empresa procura quem 'coordena pessoas e agentes de IA juntos', e não sabia nem por onde começar a mostrar isso",
        dor="a renda acabando enquanto o mercado já pede uma competência que ela nunca teve chance de aprender",
        chave="recomeço",
    ),
    "tecnicos": dict(
        pessoa="Diego, técnico de TI, monta automação há anos",
        cena="percebeu que sabe configurar ferramenta de IA uma por uma, mas nunca orquestrou várias delas como uma equipe com papéis definidos",
        dor="dominar a peça técnica e nunca ter montado o time inteiro",
        chave="orquestração",
    ),
}

ORDER = ["40mais","60mais","criadores","educadores","empreendedores","familia",
         "jovens","mulheres","pessoacomum","profissionais","recolocacao","tecnicos"]

EMOCOES = ["medo de ficar para trás","vergonha de já ter percebido e não ter feito nada",
           "injustiça (\"estão decidindo por você\")","perda do que já é seu",
           "orgulho ferido","pertencimento (\"os que entenderam já estão fazendo\")",
           "alívio negado (o conforto que engana)"]

FORMATOS_ALC = ["afirmação provocativa","pergunta incômoda","mito versus realidade",
                "erro comum","previsão","descoberta","comparação",
                "consequência inesperada","opinião contrária","notícia explicada de forma simples"]

FORMATOS_AUT = ["explicação prática","demonstração","comparação técnica","passo a passo curto",
                "desmontagem de um erro","conceito explicado","análise de ferramenta","causa e consequência"]

ENGAJ = ["escolha binária com lado declarado","auto-classificação","confronto amistoso",
         "marcação com motivo","compromisso público"]

def w(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def img_block(n, trecho, gatilho, headline, hook_word, hook_text, prompt):
    return (f'IMAGEM {n} — "{trecho}" [{gatilho}]\n'
            f'headline: {headline}\n'
            f'hook: {hook_text.format(k="{"+hook_word+"}")}\n'
            f'{prompt}\n')

def make_alc(pub, d, idx):
    emo = EMOCOES[idx % len(EMOCOES)]
    fmt = FORMATOS_ALC[idx % len(FORMATOS_ALC)]
    chave = d["chave"]
    nome = d["pessoa"].split(",")[0]
    ganchos = [
        "Gerenciar IA virou parecido com gerenciar gente.",
        "Você usa IA. Alguém já está gerenciando uma equipe dela.",
        "Ninguém te avisou que o cargo de gestor mudou.",
        "Tem gente comandando agentes, não só usando ferramenta.",
        "A diferença não é usar IA, é dirigir um time com ela.",
    ]
    vencedor = ganchos[idx % 5]
    fala = (
        f"{vencedor}\n"
        f"Pensa em {nome}: {d['cena']}.\n"
        f"Quem só usa IA pede uma coisa de cada vez e espera a resposta.\n"
        f"Quem gerencia IA define o papel de cada agente, dá o contexto certo e acompanha o resultado — do jeito que se gerencia gente.\n"
        f"A diferença não é saber mais ferramenta, é saber dirigir um time que agora tem pessoas e agentes juntos.\n"
        f"Você já pensa como quem usa IA ou como quem gerencia uma equipe com ela?\n"
        f"Responde 1 se você ainda só usa, ou 2 se já pensa em gerenciar — sem ficar em cima do muro.\n"
        f"Usar resolve uma tarefa. Gerenciar resolve o resto da carreira."
    )
    overlays = (
        f'ATENÇÃO (0–2s): "{vencedor}"\n'
        f'RETENÇÃO: usar IA x gerenciar uma equipe com IA, a virada que expõe a diferença\n'
        f'PROVA: a mesma tabela de gestão de pessoas aplicada a agentes de IA\n'
        f'ENGAJAMENTO: escolha binária — 1 só usa, 2 já gerencia\n'
        f'CTA (fecho): comenta 1 ou 2 agora'
    )
    segs = [
        (vencedor, emo, "GERENCIAR IA | É COMO GERENCIAR GENTE", chave,
         "a {k} que ninguém te ensinou ainda",
         "A cracked org-chart made of glowing glass shattering mid-air above an empty desk, warm dim light, cinematic photo, no embedded text"),
        (f"pensa em alguém como {nome}", "identificação", "UMA CENA QUE VOCÊ CONHECE", chave,
         "o momento em que a {k} de outro alguém aparece na sua frente",
         "A single figure sitting alone at a desk staring at a glowing screen with a confused expression, warm-cold split lighting, cinematic photo"),
        ("quem só usa pede uma coisa de cada vez", "vergonha de já ter percebido e não ter feito nada", "PEDIR UMA COISA | NÃO É GERIR", chave,
         "um pedido isolado não constrói {k}",
         "A single hand pressing one button on a large silent control panel full of unused switches, dim cinematic light"),
        ("quem gerencia define papel, dá contexto, acompanha", "medo de ficar para trás", "DEFINIR PAPEL | DAR CONTEXTO | ACOMPANHAR", chave,
         "sem {k}, cada agente trabalha sozinho, perdido",
         "Multiple small robotic figures suddenly aligning into organized formation as a warm light sweeps over them, cinematic wide shot"),
        ("é dirigir um time, não só usar ferramenta", "orgulho ferido", "DIRIGIR UM TIME | NÃO SÓ USAR", chave,
         "{k} sólida atravessa qualquer ferramenta nova",
         "A conductor's hand raised before an orchestra of glowing instruments playing without human musicians, dramatic cinematic wide shot"),
        ("você usa ou você gerencia?", "injustiça (\"estão decidindo por você\")", "VOCÊ USA | OU VOCÊ GERENCIA?", chave,
         "responde com {k}, não com desculpa",
         "Two identical doors side by side, one opening smoothly into light, one jammed half-open into darkness, cinematic photo"),
        ("responde 1 ou 2", "pertencimento (\"os que entenderam já estão fazendo\")", "RESPONDE 1 OU 2", chave,
         "sem ficar em cima do muro, com {k}",
         "A hand hovering between two glowing buttons numbered subtly by shape, warm spotlight, cinematic composition, no embedded text"),
        ("usar resolve uma tarefa, gerenciar resolve a carreira", "fecho repetível", "USAR RESOLVE HOJE | GERENCIAR RESOLVE SEMPRE", chave,
         "a {k} é o que fica quando a ferramenta muda",
         "A small candle flame steady inside a glass globe while wind blows uselessly around it outside, cinematic macro shot"),
    ]
    imgs = "\n".join(img_block(i, t, g, h, chave, hf, p) for i,(t,g,h,_,hf,p) in enumerate(segs, start=1))
    ganchos_txt = "\n".join(
        f'{i+1}. "{g}" [{"vencedor" if i==idx%5 else "descartado"}]' for i,g in enumerate(ganchos)
    )
    content = (
        f"Tipo: alc\n"
        f"Formato escolhido: {fmt}\n\n"
        f"## Ganchos descartados\n{ganchos_txt}\n"
        f"Emoção-gatilho da vencedora: {emo}\n"
        f"Por que venceu: nomeia a diferença entre usar IA e gerenciar uma equipe com IA, que é exatamente a dor de {nome} ({d['dor']}), sem soar como aula.\n\n"
        f"### FALA\n{fala}\n\n"
        f"### SOBREPOSIÇÕES DE TELA\n{overlays}\n\n"
        f"## IMAGENS\n\n{imgs}\n"
        f"## ESTRUTURA\nGancho de {fmt} contrastando usar IA com gerenciar uma equipe de agentes, vira escolha binária 1/2, fecha repetindo que gerenciar é o que sustenta a carreira.\n"
    )
    return content

def make_aut(pub, d, idx):
    emo = EMOCOES[(idx+2) % len(EMOCOES)]
    fmt = FORMATOS_AUT[idx % len(FORMATOS_AUT)]
    chave = d["chave"]
    nome = d["pessoa"].split(",")[0]
    ganchos = [
        "A maioria confunde usar IA com gerenciar IA.",
        "Gerenciar agente de IA copia um passo da gestão de gente.",
        "Isto aqui é o que ninguém te explica sobre gestão de IA.",
        "Tem uma etapa da gestão de pessoas que virou etapa da IA.",
        "Você sabe qual etapa de gerir gente vira gerir agente?",
    ]
    vencedor = ganchos[idx % 5]
    fala = (
        f"{vencedor}\n"
        f"{nome} {d['cena']} — e achou que o problema era não saber mais ferramenta.\n"
        f"Não era. Gerenciar IA copia etapas de gerenciar gente: no lugar de contratar, você escolhe o agente; no lugar de treinar, você dá contexto e instrução; no lugar de delegar tarefa, você delega objetivo.\n"
        f"E tem uma etapa que ninguém pula: acompanhar. Assim como você acompanha um funcionário, você observa a execução do agente antes de confiar cegamente.\n"
        f"É a mesma lógica de sempre, aplicada a um tipo novo de time.\n"
        f"Salva esse vídeo pra comparar com o próximo agente que você for configurar.\n"
        f"Quem entende que é gestão, não é só configuração, monta um time que funciona de verdade."
    )
    overlays = (
        f'ATENÇÃO (0–2s): "{vencedor}"\n'
        f'RETENÇÃO: cada etapa da gestão de pessoas revelada como etapa da gestão de IA\n'
        f'PROVA: contratar→escolher agente, treinar→dar contexto, delegar tarefa→delegar objetivo\n'
        f'ENGAJAMENTO: salvar o vídeo pra comparar no próximo agente configurado\n'
        f'CTA (fecho): salva agora'
    )
    segs = [
        (vencedor, "identificação", "USAR IA | GERENCIAR IA", chave, "a distância entre os dois é a {k}",
         "A person's hand pressing a glowing button without seeing the mechanism behind the wall, dim warm light, cinematic photo"),
        (f"{nome} achou que era falta de ferramenta", "vergonha de já ter percebido e não ter feito nada", "ACHOU QUE ERA A FERRAMENTA", chave,
         "quase sempre é falta de {k}",
         "A tool lying broken on a table while an untouched instruction manual sits closed beside it, cinematic still life, no embedded text"),
        ("no lugar de contratar, você escolhe o agente", "alívio negado (o conforto que engana)", "CONTRATAR | VIRA ESCOLHER O AGENTE", chave, "a {k} muda de forma, não de lógica",
         "A hand selecting one glowing card from several floating options above a desk, cinematic close-up, no embedded text"),
        ("no lugar de treinar, você dá contexto", emo, "TREINAR | VIRA DAR CONTEXTO", chave, "sem {k}, o agente trabalha às cegas",
         "A lantern being handed from one figure to a robotic figure standing in the dark, warm light spreading, cinematic wide shot"),
        ("no lugar de delegar tarefa, você delega objetivo", "medo de ficar para trás", "DELEGAR TAREFA | VIRA DELEGAR OBJETIVO", chave, "a {k} amplia o alcance de cada pedido",
         "A single arrow released from a bow splitting into several glowing arrows mid-flight toward the same target, cinematic wide shot"),
        ("acompanhar continua sendo etapa obrigatória", "orgulho ferido", "ACOMPANHAR | NUNCA SAI DA LISTA", chave, "a {k} não dispensa supervisão",
         "A supervisor figure watching several glowing screens of activity from behind, calm cinematic wide shot"),
        ("salva pra comparar no próximo agente", "pertencimento (\"os que entenderam já estão fazendo\")", "SALVA PRA COMPARAR DEPOIS", chave, "guarda a {k} pra próxima vez",
         "A hand tucking a small glowing bookmark into a notebook on a warm-lit desk, cinematic close-up, no embedded text"),
        ("gestão, não só configuração, monta o time que funciona", "fecho repetível", "GESTÃO | NÃO SÓ CONFIGURAÇÃO", chave, "a {k} sustenta o time inteiro",
         "Multiple small lights arranging themselves into a steady formation across a dark room, cinematic wide shot, no embedded text"),
    ]
    imgs = "\n".join(img_block(i, t, g, h, chave, hf, p) for i,(t,g,h,_,hf,p) in enumerate(segs, start=1))
    ganchos_txt = "\n".join(
        f'{i+1}. "{g}" [{"vencedor" if i==idx%5 else "descartado"}]' for i,g in enumerate(ganchos)
    )
    content = (
        f"Tipo: aut\n"
        f"Formato escolhido: {fmt}\n\n"
        f"## Ganchos descartados\n{ganchos_txt}\n"
        f"Emoção-gatilho da vencedora: {emo}\n"
        f"Por que venceu: demonstra a tradução gestão-de-gente → gestão-de-agente de forma concreta pra {nome}, sem soar como aula teórica.\n\n"
        f"### FALA\n{fala}\n\n"
        f"### SOBREPOSIÇÕES DE TELA\n{overlays}\n\n"
        f"## IMAGENS\n\n{imgs}\n"
        f"## ESTRUTURA\nGancho de {fmt} traduzindo etapas da gestão de pessoas para a gestão de agentes de IA, demonstra com o caso de {nome}, fecha com o princípio repetível de que é gestão, não configuração.\n"
    )
    return content

def make_pro(pub, d, idx):
    emo = EMOCOES[(idx+4) % len(EMOCOES)]
    chave = d["chave"]
    nome = d["pessoa"].split(",")[0]
    ganchos = [
        "Ficar só usando IA de longe tem um preço.",
        "Enquanto você só usa, alguém já está gerenciando.",
        "Essa sensação de estar atrás do novo gestor não passa sozinha.",
        "O primeiro passo não é ferramenta nova, é papel novo.",
        "Adiar aprender a gerenciar IA custa mais do que aprender.",
    ]
    vencedor = ganchos[idx % 5]
    fala = (
        f"{vencedor}\n"
        f"{nome} vive isso agora: {d['cena']}.\n"
        f"Se isso continuar, a distância entre quem só usa IA e quem já gerencia um time com ela aumenta toda semana — e é isso que alimenta {d['dor']}.\n"
        f"Não é sobre virar especialista da noite pro dia. É sobre parar de adiar o primeiro passo de pensar como gestor, não como usuário.\n"
        f"O primeiro passo de hoje é simples: escolhe uma tarefa que você repete toda semana e pergunta: eu estou usando IA nela, ou estou gerenciando ela pra fazer isso por mim?\n"
        f"Comenta aqui embaixo qual tarefa você vai repensar essa semana.\n"
        f"Quem começa a pensar como gestor chega mais longe do que quem só aprende mais um atalho."
    )
    overlays = (
        f'ATENÇÃO (0–2s): "{vencedor}"\n'
        f'RETENÇÃO: consequência de adiar o papel de gestor, sem prazo inventado\n'
        f'PROVA: a distância crescente entre quem usa e quem gerencia\n'
        f'ENGAJAMENTO: compromisso público — comenta a tarefa que vai repensar\n'
        f'CTA (fecho): comenta agora o compromisso'
    )
    segs = [
        (vencedor, emo, "SÓ USAR | TEM UM PREÇO", chave, "ninguém te mostra essa {k}",
         "An hourglass with sand turning into scattered gray dust instead of falling normally, dim warm light, cinematic photo, no embedded text"),
        (f"{nome} vive isso agora", "identificação", "UMA CENA REAL", chave, "a {k} que falta pesa todo dia",
         "A single figure standing at a closed door with light seeping from underneath, warm-cold split lighting, cinematic photo"),
        ("se continuar, a distância aumenta", "perda do que já é seu", "A DISTÂNCIA | SÓ AUMENTA", chave, "toda semana sem {k} custa mais",
         "Two parallel roads diverging further apart with each frame, one paved and lit, one cracked and dark, cinematic wide shot"),
        ("não é virar especialista da noite pro dia", "alívio negado (o conforto que engana)", "NÃO É VIRAR EXPERT | É NÃO ADIAR", chave, "o primeiro passo cabe {k}",
         "A single small light switch being flipped in a dark room, gentle warm glow spreading slowly, cinematic composition"),
        ("escolhe uma tarefa que se repete", "medo de ficar para trás", "UMA TAREFA REAL | HOJE", chave, "começa pelo menor pedaço da {k}",
         "A tiny seed being planted by hand in warm soil under soft golden light, cinematic macro shot, no embedded text"),
        ("usando IA ou gerenciando IA nela?", "orgulho ferido", "USANDO | OU GERENCIANDO?", chave, "a pergunta certa já é {k}",
         "A single lit window standing out among many dark ones on a building facade at night, cinematic wide shot"),
        ("comenta a tarefa que vai repensar", "compromisso público", "COMENTA SUA TAREFA", chave, "diga em voz alta sua {k}",
         "A hand writing a short commitment note on paper under warm desk light, rest of room in soft shadow, cinematic close-up"),
        ("pensar como gestor chega mais longe", "fecho repetível", "PENSAR COMO GESTOR | CHEGA MAIS LONGE", chave, "a {k} sólida não se perde",
         "A small warm light growing steadily brighter along a dark path toward a distant glowing horizon, cinematic wide shot, no embedded text"),
    ]
    imgs = "\n".join(img_block(i, t, g, h, chave, hf, p) for i,(t,g,h,_,hf,p) in enumerate(segs, start=1))
    ganchos_txt = "\n".join(
        f'{i+1}. "{g}" [{"vencedor" if i==idx%5 else "descartado"}]' for i,g in enumerate(ganchos)
    )
    content = (
        f"Tipo: pro\n"
        f"Formato escolhido: dor → consequência de não agir → primeiro passo nomeado\n\n"
        f"## Ganchos descartados\n{ganchos_txt}\n"
        f"Emoção-gatilho da vencedora: {emo}\n"
        f"Por que venceu: liga direto à dor de {nome} ({d['dor']}) sem inventar prazo nem número.\n\n"
        f"### FALA\n{fala}\n\n"
        f"### SOBREPOSIÇÕES DE TELA\n{overlays}\n\n"
        f"## IMAGENS\n\n{imgs}\n"
        f"## ESTRUTURA\nGancho nomeia o custo de adiar o papel de gestor de IA, mostra a consequência concreta pra {nome}, fecha com passo nomeado de hoje e compromisso público no comentário.\n"
    )
    return content

count = 0
for idx, pub in enumerate(ORDER):
    d = PUB[pub]
    w(os.path.join(BASE, f"{pub}-alc.md"), make_alc(pub, d, idx)); count += 1
    w(os.path.join(BASE, f"{pub}-aut.md"), make_aut(pub, d, idx)); count += 1
    w(os.path.join(BASE, f"{pub}-pro.md"), make_pro(pub, d, idx)); count += 1

print(f"Gerados {count} arquivos em {BASE}")
