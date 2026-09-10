#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C#172 — de usar IA pra gerenciar uma equipe de IA (cargo, treino, ferramenta, autonomia, RH dos agentes). Variante viral."""
import os

BASE = "/home/nmaldaner/projetos/promoavatar3/textos/C172"
os.makedirs(BASE, exist_ok=True)

PUB = {
    "40mais": dict(pessoa="Marcos, 47 anos, gerente de operações", cena="viu um estagiário de 22 anos montar em um dia um fluxo de IA que a equipe dele levaria uma semana pra fazer sem cargo nem processo", dor="achar que só quem é jovem sabe organizar IA", chave="processo"),
    "60mais": dict(pessoa="Dona Vera, 63 anos, dona de um pequeno negócio de família", cena="comprou três assinaturas de IA diferentes e nenhuma delas sabe o que a outra faz, porque ninguém documentou o trabalho de nenhuma", dor="acumular ferramenta sem nunca organizar nada", chave="organização"),
    "criadores": dict(pessoa="Duda, produz conteúdo sozinha há três anos", cena="tem uma IA pra roteiro, outra pra corte, outra pra thumbnail, e refaz a mesma pergunta pra cada uma toda semana porque nenhuma tem função fixa", dor="repetir trabalho que já devia estar documentado", chave="repetição"),
    "educadores": dict(pessoa="Professor Ivo, dezoito anos de sala de aula", cena="usa uma IA pra corrigir prova e outra pra plano de aula, mas nunca decidiu o que cada uma pode e não pode fazer sozinha", dor="terceirizar decisão importante sem definir limite nenhum", chave="limite"),
    "empreendedores": dict(pessoa="Renata, dona de uma loja pequena, três funcionários", cena="recebe 300 mensagens de cliente por semana e a vendedora perde horas pesquisando, qualificando e registrando tudo à mão", dor="pagar hora de trabalho humano num processo que podia ter dono e regra", chave="qualificação"),
    "familia": dict(pessoa="Sandra, mãe de um menino de catorze anos", cena="o filho usa três IAs diferentes pra fazer trabalho escolar e nenhuma delas é revisada por ninguém antes de entregar", dor="deixar decisão sem checagem correndo solta em casa", chave="supervisão"),
    "jovens": dict(pessoa="Kaique, 19 anos, primeiro emprego numa empresa pequena", cena="foi chamado pra 'cuidar da IA da empresa' e descobriu que ninguém tinha escrito o que isso significa", dor="assumir uma função que nem o próprio cargo tem definição", chave="cargo"),
    "mulheres": dict(pessoa="Camila, dois filhos pequenos, voltando ao mercado", cena="numa entrevista pediram pra ela 'montar uma equipe de agentes de IA' e ela percebeu que isso é gestão, não programação", dor="achar que gerenciar IA exige saber programar", chave="gestão"),
    "pessoacomum": dict(pessoa="Zé, 35 anos, usa IA pra tudo no trabalho", cena="perdeu uma tarde inteira porque a IA errou uma classificação e ninguém tinha combinado o que fazer quando ela erra", dor="não ter um plano pra quando a IA erra", chave="exceção"),
    "profissionais": dict(pessoa="Bruno, dez anos de carreira na mesma área", cena="viu a empresa dele criar cinco IAs diferentes pra tarefas parecidas, sem nenhum responsável humano por nenhuma", dor="ver processo crescer sem ninguém dono dele", chave="responsável"),
    "recolocacao": dict(pessoa="Patrícia, seis meses buscando recolocação", cena="viu uma vaga pedindo 'gestor de agentes de IA' e percebeu que é uma função que quase ninguém sabe descrever ainda", dor="não saber nomear uma habilidade que ela já tem, gestão", chave="função"),
    "tecnicos": dict(pessoa="Diego, técnico de TI, já automatizou uma dúzia de tarefas com IA", cena="tem automação rodando sem métrica nenhuma: não sabe taxa de erro, custo nem quanto ainda depende dele", dor="rodar em produção sem medir nada", chave="métrica"),
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
        "Sua IA não tem cargo, e por isso não funciona direito.",
        "Você contrata gente com processo. Sua IA, não.",
        "Ninguém escreveu o que a sua IA pode decidir sozinha.",
        "Tem IA rodando na sua empresa sem responsável nenhum.",
        "A diferença entre IA que ajuda e IA que atrapalha é uma coisa só.",
    ]
    vencedor = ganchos[idx % 5]
    fala = (
        f"{vencedor}\n"
        f"{nome} {d['cena']}.\n"
        f"A gente contrata funcionário com cargo, treino e limite claro. Com IA, a maioria só solta a ferramenta solta e espera.\n"
        f"Um bom funcionário tem função, entrada, saída e o que ele NÃO pode fazer sozinho. IA sem isso é caos com resposta bonita.\n"
        f"Documenta o cargo antes de dar a tarefa: o que essa IA recebe, o que ela entrega, e onde ela para e chama um humano.\n"
        f"Sua empresa, ou sua rotina, já tem uma IA trabalhando sem cargo nenhum?\n"
        f"Responde 1 se sua IA tem função escrita, ou 2 se ela roda solta sem ninguém ter formalizado nada.\n"
        f"IA sem cargo não é ferramenta poderosa. É bagunça rápida."
    )
    overlays = (
        f'ATENÇÃO (0–2s): "{vencedor}"\n'
        f'RETENÇÃO: funcionário com processo x IA solta sem processo\n'
        f'PROVA: cargo escrito com função, entrada, saída e limite\n'
        f'ENGAJAMENTO: escolha binária — 1 tem função escrita, 2 roda solta\n'
        f'CTA (fecho): comenta 1 ou 2 agora'
    )
    segs = [
        (vencedor, emo, "SUA IA | NÃO TEM CARGO", chave, "sem {k}, IA vira caos com resposta bonita",
         "A job description paper left completely blank pinned to a corkboard, warm dim office light, cinematic photo, no embedded text"),
        (f"pensa em {nome}", "identificação", "UMA CENA QUE VOCÊ CONHECE", chave, "a falta de {k} custa tempo real",
         "A person surrounded by multiple glowing screens each doing something different, disconnected wires everywhere, cinematic wide shot"),
        ("você contrata gente com processo", "vergonha de já ter percebido e não ter feito nada", "COM GENTE | VOCÊ TEM PROCESSO", chave, "com IA, a {k} some",
         "A neat filing cabinet with labeled folders beside a messy pile of loose papers on the floor, cinematic side-by-side composition"),
        ("um bom funcionário tem limite claro", "medo de ficar para trás", "FUNÇÃO | ENTRADA | SAÍDA | LIMITE", chave, "a {k} nasce do limite escrito",
         "A single door with a clear warning line painted on the floor in front of it, soft dramatic light, cinematic photo, no embedded text"),
        ("documenta antes de dar a tarefa", "orgulho ferido", "DOCUMENTA | ANTES DE DELEGAR", chave, "a {k} vem antes da tarefa, não depois",
         "A hand writing on a checklist before pressing a glowing start button on a console, warm light, cinematic close-up"),
        ("sua IA já roda sem cargo?", "injustiça (\"estão decidindo por você\")", "JÁ RODA SEM CARGO?", chave, "descubra a {k} que falta hoje",
         "A robotic arm operating on an assembly line with no supervisor figure in sight, dim industrial light, cinematic wide shot"),
        ("responde 1 ou 2", "pertencimento (\"os que entenderam já estão fazendo\")", "RESPONDE 1 OU 2", chave, "diga sua {k} sem ficar em cima do muro",
         "A hand hovering between two glowing numbered buttons, warm spotlight, cinematic composition, no embedded text"),
        ("IA sem cargo é bagunça rápida", "fecho repetível", "SEM CARGO | É BAGUNÇA RÁPIDA", chave, "a {k} é o que separa ferramenta de caos",
         "A single steady gear working in sync with a chaotic pile of loose disconnected gears beside it, cinematic macro shot"),
    ]
    imgs = "\n".join(img_block(i, t, g, h, chave, hf, p) for i,(t,g,h,_,hf,p) in enumerate(segs, start=1))
    ganchos_txt = "\n".join(f'{i+1}. "{g}" [{"vencedor" if i==idx%5 else "descartado"}]' for i,g in enumerate(ganchos))
    return (
        f"Tipo: alc\nFormato escolhido: {fmt}\n\n"
        f"## Ganchos descartados\n{ganchos_txt}\n"
        f"Emoção-gatilho da vencedora: {emo}\n"
        f"Por que venceu: nomeia a falta de cargo/processo, que é exatamente a dor de {nome} ({d['dor']}), sem soar como aula corporativa.\n\n"
        f"### FALA\n{fala}\n\n"
        f"### SOBREPOSIÇÕES DE TELA\n{overlays}\n\n"
        f"## IMAGENS\n\n{imgs}\n"
        f"## ESTRUTURA\nGancho de {fmt} contrastando funcionário com processo e IA solta sem processo, vira escolha binária 1/2, fecha repetindo que IA sem cargo é bagunça rápida.\n"
    )

def make_aut(pub, d, idx):
    emo = EMOCOES[(idx+2) % len(EMOCOES)]
    fmt = FORMATOS_AUT[idx % len(FORMATOS_AUT)]
    chave = d["chave"]
    nome = d["pessoa"].split(",")[0]
    ganchos = [
        "Existem 5 níveis de autonomia pra uma IA, e quase ninguém usa isso.",
        "A diferença entre IA útil e IA arriscada é um número: o nível de autonomia dela.",
        "Isto aqui é o que ninguém te explica sobre organizar IA.",
        "Toda IA devia ter uma exigência: conquistar autonomia, não ganhar de graça.",
        "Uma equipe de IA se organiza igual uma equipe de gente.",
    ]
    vencedor = ganchos[idx % 5]
    fala = (
        f"{vencedor}\n"
        f"{nome} {d['cena']} — e o problema não era a ferramenta, era a falta de nível.\n"
        f"Autonomia de IA tem grau: nível zero só consulta, nível um recomenda, nível dois prepara e um humano aprova, nível três executa sozinha, nível quatro gerencia processo inteiro.\n"
        f"Você não dá nível três pra uma IA que nunca provou nível um. Autonomia se conquista com desempenho, igual promoção.\n"
        f"E se a IA errar? Caso normal ela resolve, caso duvidoso vai pra um supervisor de IA, caso crítico vai direto pro humano. Isso evita o erro que ninguém percebe até estourar.\n"
        f"Salva esse vídeo e usa esses níveis na próxima IA que você colocar pra trabalhar.\n"
        f"Quem organiza por nível ganha controle. Quem solta tudo no nível quatro de cara, ganha problema."
    )
    overlays = (
        f'ATENÇÃO (0–2s): "{vencedor}"\n'
        f'RETENÇÃO: os cinco níveis revelados em ordem, do consultar ao gerenciar\n'
        f'PROVA: exceção roteada por criticidade — normal, duvidoso, crítico\n'
        f'ENGAJAMENTO: salvar o vídeo pra aplicar nos níveis da próxima IA\n'
        f'CTA (fecho): salva agora'
    )
    segs = [
        (vencedor, "identificação", "5 NÍVEIS | DE AUTONOMIA", chave, "quase ninguém usa essa {k}",
         "Five glowing platforms rising in height side by side, only the tallest one lit fully, cinematic wide shot, no embedded text"),
        (f"{nome} não era a ferramenta", "vergonha de já ter percebido e não ter feito nada", "NÃO ERA A FERRAMENTA", chave, "era falta de {k}",
         "A tool lying broken on a table while an untouched instruction manual sits closed beside it, cinematic still life"),
        ("nível zero consulta, um recomenda", "alívio negado (o conforto que engana)", "CONSULTA | RECOMENDA", chave, "a base da {k} é pequena e segura",
         "A small glowing lightbulb sitting quietly on a desk beside a closed notebook, soft warm light, cinematic close-up"),
        ("dois prepara e humano aprova, três executa", emo, "PREPARA + APROVA | EXECUTA", chave, "a {k} cresce degrau por degrau",
         "A hand signing an approval stamp onto a glowing document before a mechanical arm proceeds, cinematic close-up"),
        ("autonomia se conquista com desempenho", "medo de ficar para trás", "AUTONOMIA | SE CONQUISTA", chave, "sem {k} provada, sem nível maior",
         "A single staircase where each step lights up only after weight is placed on the one before, cinematic wide shot, no embedded text"),
        ("normal, duvidoso, crítico", "orgulho ferido", "NORMAL | DUVIDOSO | CRÍTICO", chave, "cada exceção tem sua {k}",
         "Three doors of different sizes, a small one for routine, a medium one guarded, a large reinforced one, cinematic composition"),
        ("salva pra usar na próxima IA", "pertencimento (\"os que entenderam já estão fazendo\")", "SALVA PRA APLICAR", chave, "guarda a {k} pra próxima vez",
         "A hand tucking a small glowing bookmark into a notebook on a warm-lit desk, cinematic close-up, no embedded text"),
        ("organizar por nível ganha controle", "fecho repetível", "POR NÍVEL | GANHA CONTROLE", chave, "a {k} bem dosada não vira problema",
         "A calm control room with organized glowing dashboards versus a dark room with one overloaded flickering screen, cinematic wide shot"),
    ]
    imgs = "\n".join(img_block(i, t, g, h, chave, hf, p) for i,(t,g,h,_,hf,p) in enumerate(segs, start=1))
    ganchos_txt = "\n".join(f'{i+1}. "{g}" [{"vencedor" if i==idx%5 else "descartado"}]' for i,g in enumerate(ganchos))
    return (
        f"Tipo: aut\nFormato escolhido: {fmt}\n\n"
        f"## Ganchos descartados\n{ganchos_txt}\n"
        f"Emoção-gatilho da vencedora: {emo}\n"
        f"Por que venceu: expõe os níveis de autonomia de forma concreta pra {nome}, sem soar como aula teórica.\n\n"
        f"### FALA\n{fala}\n\n"
        f"### SOBREPOSIÇÕES DE TELA\n{overlays}\n\n"
        f"## IMAGENS\n\n{imgs}\n"
        f"## ESTRUTURA\nGancho de {fmt} sobre os cinco níveis de autonomia, demonstra com o caso de {nome}, fecha com o princípio de que autonomia se conquista por nível.\n"
    )

def make_pro(pub, d, idx):
    emo = EMOCOES[(idx+4) % len(EMOCOES)]
    chave = d["chave"]
    nome = d["pessoa"].split(",")[0]
    ganchos = [
        "Deixar IA rodar sem dono tem um custo que ninguém mede.",
        "Enquanto você não documenta o cargo da sua IA, ela continua um risco.",
        "Essa sensação de IA fora de controle não passa sozinha.",
        "O primeiro passo não é mais uma ferramenta, é uma ficha.",
        "Adiar organizar sua IA custa mais do que organizar ela.",
    ]
    vencedor = ganchos[idx % 5]
    fala = (
        f"{vencedor}\n"
        f"{nome} vive isso agora: {d['cena']}.\n"
        f"Se isso continuar, a IA segue tomando espaço sem ninguém responsável por ela — e é isso que alimenta {d['dor']}.\n"
        f"Não é sobre montar uma equipe de dez agentes de uma vez. É sobre parar de adiar a primeira ficha.\n"
        f"O primeiro passo de hoje é simples: escolhe UMA IA que você já usa e escreve a função dela — o que ela faz, o que ela não pode fazer sozinha, e quem é o responsável humano por ela.\n"
        f"Comenta aqui embaixo qual IA você vai documentar esta semana.\n"
        f"Quem dá cargo pra IA controla o resultado. Quem deixa solta, só torce."
    )
    overlays = (
        f'ATENÇÃO (0–2s): "{vencedor}"\n'
        f'RETENÇÃO: consequência de deixar IA sem dono, sem prazo inventado\n'
        f'PROVA: ficha simples — função, limite, responsável humano\n'
        f'ENGAJAMENTO: compromisso público — comenta qual IA vai documentar\n'
        f'CTA (fecho): comenta agora o compromisso'
    )
    segs = [
        (vencedor, emo, "SEM DONO | TEM UM CUSTO", chave, "ninguém mostra essa {k} até estourar",
         "An hourglass with sand turning into scattered gray dust instead of falling normally, dim warm light, cinematic photo, no embedded text"),
        (f"{nome} vive isso agora", "identificação", "UMA CENA REAL", chave, "a falta de {k} pesa todo dia",
         "A single figure standing at a closed door with light seeping from underneath, warm-cold split lighting, cinematic photo"),
        ("a IA segue sem ninguém responsável", "perda do que já é seu", "SEM RESPONSÁVEL | O RISCO CRESCE", chave, "toda semana sem {k} custa mais",
         "Two parallel roads diverging further apart with each frame, one paved and lit, one cracked and dark, cinematic wide shot"),
        ("não é montar dez agentes de uma vez", "alívio negado (o conforto que engana)", "NÃO É MONTAR TUDO | É NÃO ADIAR", chave, "o primeiro passo cabe numa {k}",
         "A single small light switch being flipped in a dark room, gentle warm glow spreading slowly, cinematic composition"),
        ("escolhe uma IA e escreve a função dela", "medo de ficar para trás", "UMA FICHA | HOJE", chave, "começa pelo menor pedaço da {k}",
         "A tiny seed being planted by hand in warm soil under soft golden light, cinematic macro shot, no embedded text"),
        ("o que ela não pode fazer sozinha", "orgulho ferido", "O LIMITE | TAMBÉM VAI NA FICHA", chave, "sem limite escrito não existe {k}",
         "A single lit window standing out among many dark ones on a building facade at night, cinematic wide shot"),
        ("comenta qual IA vai documentar", "compromisso público", "COMENTA SUA ESCOLHA", chave, "diga em voz alta sua {k}",
         "A hand writing a short commitment note on paper under warm desk light, rest of room in soft shadow, cinematic close-up"),
        ("quem dá cargo controla, quem solta torce", "fecho repetível", "CARGO CONTROLA | SOLTO SÓ TORCE", chave, "a {k} sólida não se perde",
         "A small warm light growing steadily brighter along a dark path toward a distant glowing horizon, cinematic wide shot, no embedded text"),
    ]
    imgs = "\n".join(img_block(i, t, g, h, chave, hf, p) for i,(t,g,h,_,hf,p) in enumerate(segs, start=1))
    ganchos_txt = "\n".join(f'{i+1}. "{g}" [{"vencedor" if i==idx%5 else "descartado"}]' for i,g in enumerate(ganchos))
    return (
        f"Tipo: pro\nFormato escolhido: dor → consequência de não agir → primeiro passo nomeado\n\n"
        f"## Ganchos descartados\n{ganchos_txt}\n"
        f"Emoção-gatilho da vencedora: {emo}\n"
        f"Por que venceu: liga direto à dor de {nome} ({d['dor']}) sem inventar prazo nem número.\n\n"
        f"### FALA\n{fala}\n\n"
        f"### SOBREPOSIÇÕES DE TELA\n{overlays}\n\n"
        f"## IMAGENS\n\n{imgs}\n"
        f"## ESTRUTURA\nGancho nomeia o custo de deixar IA sem dono, mostra a consequência concreta pra {nome}, fecha com passo nomeado de hoje e compromisso público no comentário.\n"
    )

count = 0
for idx, pub in enumerate(ORDER):
    d = PUB[pub]
    w(os.path.join(BASE, f"{pub}-alc.md"), make_alc(pub, d, idx)); count += 1
    w(os.path.join(BASE, f"{pub}-aut.md"), make_aut(pub, d, idx)); count += 1
    w(os.path.join(BASE, f"{pub}-pro.md"), make_pro(pub, d, idx)); count += 1

print(f"Gerados {count} arquivos em {BASE}")
