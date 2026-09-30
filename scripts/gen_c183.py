#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera os 36 roteiros (12 públicos x alc/aut/pro) de C#183 — OSWork: parar de
usar IA como chat e montar o ambiente onde ela trabalha. Variante viral."""
import os

BASE = "/home/nmaldaner/projetos/promoavatar3/textos/C183"
os.makedirs(BASE, exist_ok=True)

# gancho_alc (<=9 palavras), cena (2ª pessoa), reexplica (o que a pessoa repete),
# ganho (o que muda na vida), hook_aut (<=9), passo (1º passo do -pro),
# hook_pro (<=9), marca (marcação/lado), img (objeto concreto da cena, EN), chave
PUB = {
    "40mais": dict(
        alc="Sua experiência some a cada conversa nova.",
        cena="Você tem vinte e poucos anos de estrada. Abre a IA, e ela não sabe nada disso.",
        reexplica="quem você é, o que já resolveu, como você trabalha",
        ganho="o que você sabe deixa de morar só na sua cabeça e passa a trabalhar junto com você",
        aut="Você usa a IA como estagiário sem memória.",
        passo="escreve numa página o jeito que você resolve o problema que mais conhece — do seu jeito, com as suas regras",
        pro="Experiência que não está escrita, a IA não usa.",
        img="a worn leather work notebook full of handwritten notes, left closed beside a laptop showing an empty chat box",
        chave="experiência",
    ),
    "60mais": dict(
        alc="A IA esquece você toda vez que fecha.",
        cena="Você, aposentado, pede ajuda à IA pra organizar as contas. No dia seguinte, ela te trata como um estranho.",
        reexplica="quem você é, quais são as suas contas, como você gosta que explique",
        ganho="a IA deixa de ser uma novidade confusa e vira uma ajudante que já te conhece",
        aut="O segredo não está na pergunta que você faz.",
        passo="escreve num papel ou num arquivo três coisas: quem você é, no que precisa de ajuda e como gosta que te expliquem",
        pro="Você não precisa entender de tecnologia. Precisa disto.",
        img="an elderly person's reading glasses resting on a neatly organized household folder of bills, kitchen table, morning light",
        chave="memória",
    ),
    "criadores": dict(
        alc="Seu estilo morre cada vez que você abre chat.",
        cena="Você posta todo dia. E todo dia explica pra IA de novo o seu tom, o seu público e o que não pode dizer.",
        reexplica="o seu tom, o seu público, o formato do seu post",
        ganho="o seu estilo fica guardado num lugar onde a IA trabalha, e o ritmo deixa de te esgotar",
        aut="Criador que troca de ferramenta toda semana perde isto.",
        passo="escreve o manual do seu canal: tom, público, três posts que deram certo e o que você nunca faz",
        pro="Você não precisa de ferramenta nova. Precisa de manual.",
        img="a content creator's desk with a ring light switched off and a pile of crumpled sticky notes repeating the same instructions",
        chave="estilo",
    ),
    "educadores": dict(
        alc="Você ensina a IA do zero toda noite.",
        cena="São onze da noite. Você pede um plano de aula e, de novo, explica a turma, a série e o seu jeito de corrigir.",
        reexplica="a turma, a série, o seu critério de correção",
        ganho="as suas noites deixam de ir embora explicando o óbvio pra uma máquina",
        aut="Professor sabe disto melhor que ninguém. Só não aplicou.",
        passo="escreve o planejamento da sua turma como se fosse passar pra um substituto: série, ritmo, critério de correção",
        pro="O substituto perfeito precisa de um bom planejamento.",
        img="a teacher's desk at night, a lamp on, a tall stack of ungraded tests next to a cold cup of coffee",
        chave="planejamento",
    ),
    "empreendedores": dict(
        alc="Você paga funcionário que esquece tudo toda manhã.",
        cena="Você tem um negócio. Pede à IA um anúncio e ela não sabe o seu produto, o seu preço nem o seu cliente.",
        reexplica="o seu produto, o seu cliente, o jeito da sua marca falar",
        ganho="a IA deixa de ser um chat que você alimenta e vira uma parte da operação que já sabe o negócio",
        aut="Empresa não roda com instrução falada. IA também não.",
        passo="escreve o manual do seu negócio em uma página: o que você vende, pra quem, e como a sua marca fala",
        pro="Todo negócio que cresce tem um manual. O seu?",
        img="a small shop counter at opening time, a brand new employee's empty desk with a blank badge and no instructions",
        chave="manual",
    ),
    "familia": dict(
        alc="Seu filho usa IA como um brinquedo que esquece.",
        cena="Seu filho pede resposta pronta pra IA, copia e fecha. Amanhã, começa tudo do zero de novo.",
        reexplica="o que ele está estudando, onde parou, como ele aprende melhor",
        ganho="ele aprende a organizar o próprio trabalho — e isso vale pra qualquer ferramenta que vier",
        aut="Ninguém está ensinando isto pro seu filho na escola.",
        passo="senta com o seu filho e escrevam juntos um caderno de projeto: o que ele quer fazer, as regras e onde parou",
        pro="O que você pode ensinar hoje sem saber programar.",
        img="a child's school backpack spilling loose unnumbered pages across the floor, a parent's hand picking one up",
        chave="organizar",
    ),
    "jovens": dict(
        alc="Todo mundo usa IA. Pouca gente sabe montar isto.",
        cena="Você não tem experiência pra colocar no currículo. E usa a IA igual a todo mundo: pergunta e resposta.",
        reexplica="o seu projeto, o que já foi feito, o que falta",
        ganho="você passa a ter algo que mostra, e não só algo que usa",
        aut="Saber perguntar pra IA não é mais diferencial.",
        passo="escolhe um projeto pequeno seu e cria uma pasta com um arquivo dizendo o objetivo, as regras e onde você parou",
        pro="Sem experiência? Então comece a construir a sua.",
        img="a young person's nearly empty resume on a desk beside a single organized project folder, strong contrast",
        chave="construir",
    ),
    "mulheres": dict(
        alc="Você já trabalha dobrado. A IA te faz repetir.",
        cena="Você tem vinte minutos entre uma coisa e outra. Abre a IA e gasta dez explicando tudo de novo.",
        reexplica="o seu trabalho, o seu jeito, o que você já decidiu",
        ganho="os seus vinte minutos viram vinte minutos de trabalho, e não de repetição",
        aut="O tempo que você não tem vai embora aqui.",
        passo="escreve uma página com o que você faz, como gosta do resultado e o que está em andamento — e abre toda conversa com ela",
        pro="Vinte minutos por dia não podem ir pro lixo.",
        img="a kitchen timer ticking beside an open laptop and a child's lunchbox, split morning chaos, warm light",
        chave="tempo",
    ),
    "pessoacomum": dict(
        alc="Você trata a IA como um estranho. Toda vez.",
        cena="Você abre a IA, explica quem é, o que quer, como quer. Recebe a resposta. Fecha. Amanhã, repete tudo.",
        reexplica="quem você é, o que está fazendo, como quer o resultado",
        ganho="a IA para de começar do zero e passa a continuar de onde parou",
        aut="Quase todo mundo usa a IA pela metade.",
        passo="cria um arquivo de texto com três coisas: quem você é, o que está fazendo e como quer o resultado",
        pro="Um arquivo de texto muda o jeito que você usa IA.",
        img="the same sticky note rewritten and stuck again and again on a monitor, dozens of identical notes piling up",
        chave="contexto",
    ),
    "profissionais": dict(
        alc="Seu colega não é melhor. A IA dele lembra.",
        cena="Você vê o colega entregar mais rápido com a mesma IA que você usa. A diferença não está no prompt.",
        reexplica="o projeto, o cliente, o padrão da entrega",
        ganho="você amplia a sua profissão em vez de disputar com ela",
        aut="O problema não é o seu prompt. É o lugar.",
        passo="pega a tarefa que você mais repete no trabalho e escreve o procedimento dela: passos, regras e exemplo de entrega boa",
        pro="A tarefa que mais te consome pede um procedimento.",
        img="two identical office desks side by side, one buried in loose papers, the other with neatly labeled folders and a closed laptop",
        chave="procedimento",
    ),
    "recolocacao": dict(
        alc="Cada currículo novo, você recomeça do zero.",
        cena="Você está mandando currículo. E pra cada vaga pede ajuda à IA explicando de novo toda a sua história.",
        reexplica="a sua trajetória, as suas conquistas, a vaga que você busca",
        ganho="o recomeço deixa de começar do zero toda vez",
        aut="Quem procura emprego com IA erra isto.",
        passo="escreve a sua história profissional uma vez, completa, num arquivo — e usa ele como base de toda candidatura",
        pro="Sua história merece ser escrita uma vez só.",
        img="a stack of nearly identical printed resumes each with different handwritten corrections, scattered on a small table",
        chave="história",
    ),
    "tecnicos": dict(
        alc="Você coleciona prompt. Deveria construir o ambiente.",
        cena="Você tem uma pasta cheia de prompts salvos. E cada conversa ainda começa do zero.",
        reexplica="o projeto, as convenções, o que já foi decidido",
        ganho="você para de testar ferramenta e passa a ter um sistema seu, que continua o trabalho",
        aut="Agente bom não nasce do prompt. Nasce do ambiente.",
        passo="cria no seu projeto um arquivo de instruções pro agente: contexto, regras, comandos e o que já foi decidido",
        pro="Seu projeto ainda não tem este arquivo?",
        img="a developer's desk with a wall of printed prompt snippets taped up, and one clean repository folder on the screen",
        chave="ambiente",
    ),
}

ORDEM = ["40mais", "60mais", "criadores", "educadores", "empreendedores", "familia",
         "jovens", "mulheres", "pessoacomum", "profissionais", "recolocacao", "tecnicos"]


def primeiras(s, n=5):
    return " ".join(s.replace("\n", " ").split()[:n]).rstrip(".,?!—").lower()


def alc(k, p):
    fala = [
        p["alc"],
        p["cena"],
        f"Você chama isso de usar IA. Na prática, é recomeçar toda vez: {p['reexplica']}.",
        "O problema não é a pergunta. A IA não tem onde guardar o que você disse.",
        "Quem entendeu parou de caçar o prompt perfeito e montou o lugar onde a IA trabalha: arquivos, regras, histórico.",
        "Prompt é uma instrução do momento. O ambiente é o que fica.",
        "Responde 1 ou 2, sem ficar em cima do muro. 1: eu ainda explico tudo de novo toda vez. 2: a minha IA já sabe quem eu sou.",
    ]
    segs = [
        ("tensão", "O QUE VOCÊ PERDE | TODA VEZ", "cada conversa nova começa do {zero}", p["img"] + ", cold light, the loss is visible"),
        ("", "A CENA | QUE SE REPETE", "você é um {estranho} pra própria ferramenta", "the same morning scene repeated three times in a row like a film strip, a person opening a laptop, identical frames"),
        ("", "RECOMEÇAR | NÃO É USAR", "tudo que você disse ontem {sumiu}", "a whiteboard wiped clean overnight, faint ghost marks of yesterday's work still visible"),
        ("virada", "NÃO É A PERGUNTA | É O LUGAR", "a IA não tem onde {guardar} nada", "an empty office with no desk, no shelves, no drawers, a single chair in the middle"),
        ("prova", "ARQUIVOS REGRAS | HISTÓRICO", "o lugar onde a IA {trabalha}", "a tidy workspace with labeled folders, a rulebook, and a logbook open to yesterday's page, warm light"),
        ("engajamento", "1 OU 2 | SEM MURO", "comenta em qual {lado} você está hoje", "a road splitting into two clearly different paths, one looping back on itself, the other going forward"),
    ]
    return dict(tipo="alc", formato="consequência inesperada", fala=fala, segs=segs,
                sob=dict(at=p["alc"].upper().rstrip("."), ret="a cena de recomeçar se repete até a virada: não é a pergunta, é o lugar",
                         prova="antes/depois: chat vazio re-explicando x pasta com arquivos, regras e histórico",
                         eng="responde 1 (explico tudo de novo) ou 2 (minha IA já sabe quem eu sou)", cta="comenta 1 ou 2"),
                estr="Consequência inesperada: gancho de perda → cena do público → virada (não é a pergunta, é o lugar) → frase repetível → escolha binária nomeada.")


def aut(k, p):
    fala = [
        p["aut"],
        "Você acha que usar bem a IA é escrever o prompt certo. Isso é metade.",
        "Prompt acaba junto com a conversa. A outra metade é o ambiente, e ele tem quatro peças.",
        f"Um: um arquivo com o contexto — {p['reexplica']}.",
        "Dois: as regras. Três: o passo a passo do que se repete. Quatro: o histórico, onde parou.",
        f"Com isso, {p['ganho']}.",
        "A pergunta deixa de ser 'qual prompt eu uso' e vira 'onde a minha IA trabalha'. Salva pra montar as suas quatro peças.",
    ]
    segs = [
        ("tensão", "USANDO PELA | METADE", "o que falta não é a {pergunta}", p["img"]),
        ("", "PROMPT É | SÓ METADE", "acabou a conversa, acabou a {instrução}", "a sand timer running out next to a sheet of instructions that is fading away"),
        ("retenção", "QUATRO PEÇAS | DO AMBIENTE", "a outra metade é o {lugar} de trabalho", "four empty labeled drawers of a wooden cabinet, one slightly open, top view"),
        ("prova", "CONTEXTO | E REGRAS", "quem você é e o que {pode}", "a single typed page pinned above a desk next to a short list of do and don't marks drawn with check and cross symbols"),
        ("prova", "PROCEDIMENTOS | E HISTÓRICO", "o passo a passo e {onde parou}", "a recipe card clipped to a logbook with a bookmark ribbon marking the last page used"),
        ("virada", "DEPOIS DAS | QUATRO PEÇAS", "a IA {continua} em vez de recomeçar", "a work desk left mid-task at night and the same desk next morning with the work already moved forward"),
        ("engajamento", "ONDE A SUA IA | TRABALHA?", "salva e monta as suas {quatro peças}", "a hand placing the fourth labeled folder into a neat row of four, satisfying close-up"),
    ]
    return dict(tipo="aut", formato="conceito explicado", fala=fala, segs=segs,
                sob=dict(at=p["aut"].upper().rstrip("."), ret="contagem das quatro peças: contexto, regras, procedimentos, histórico",
                         prova="as quatro peças aparecendo como pastas/arquivos na tela",
                         eng="salva este vídeo pra montar as suas quatro peças", cta="salva"),
                estr="Conceito explicado: entendido pela metade (prompt) → a outra metade (ambiente) → contagem de 4 peças → ganho do público → princípio repetível.")


def pro(k, p):
    fala = [
        p["pro"],
        f"Toda vez que você abre a IA do zero, perde o mesmo tempo explicando {p['reexplica']}.",
        "E quanto mais você usa, mais você repete. Isso não melhora sozinho.",
        f"O primeiro passo é pequeno e é de hoje: {p['passo']}.",
        "Da próxima vez, a IA começa sabendo. O resto vem depois — mas começa aqui.",
        "Quem monta o lugar para de pedir e começa a continuar.",
        "Escreve nos comentários: qual é a primeira coisa que vai entrar nesse arquivo esta semana?",
    ]
    segs = [
        ("tensão", p["chave"].upper() + " | FORA DO PAPEL", "o que muda com {um arquivo}", p["img"]),
        ("", "O MESMO TEMPO | PERDIDO", "explicando tudo de {novo}", "a clock on a wall with the same hour circled in chalk again and again"),
        ("", "NÃO MELHORA | SOZINHO", "quanto mais usa, mais {repete}", "a treadmill in an empty room, running, going nowhere"),
        ("prova", "PRIMEIRO PASSO | DE HOJE", "uma página, escrita {uma vez}", "a single sheet of paper being written by hand with a pen, the first line already filled, calm light"),
        ("virada", "A IA COMEÇA | SABENDO", "depois vêm regras e {procedimentos}", "a key placed on top of a folded page on a clean desk, ready to use"),
        ("engajamento", "O QUE ENTRA | NO ARQUIVO?", "escreve o seu {compromisso} da semana", "an open notebook with an empty checklist and a pen resting across it, first box about to be ticked"),
    ]
    return dict(tipo="pro", formato="direção (dor → consequência → primeiro passo)", fala=fala, segs=segs,
                sob=dict(at=p["pro"].upper().rstrip(".?"), ret="a repetição que não melhora sozinha, até o passo de hoje",
                         prova="a página única sendo escrita — quem sou / o que faço / como quero",
                         eng="escreve o que vai entrar no seu arquivo esta semana", cta="comenta o seu compromisso"),
                estr="Direção: gancho → dor da repetição → consequência (não melhora sozinho) → primeiro passo nomeado de hoje → frase repetível → compromisso público.")


def render(d):
    L = [f"Tipo: {d['tipo']}", f"Formato escolhido: {d['formato']}", "", "### FALA"]
    for f in d["fala"]:
        L += [f, ""]
    s = d["sob"]
    L += ["### SOBREPOSIÇÕES",
          f'ATENÇÃO (0–2s): "{s["at"]}"',
          f"RETENÇÃO (miolo): {s['ret']}",
          f"PROVA: {s['prova']}",
          f'ENGAJAMENTO: "{s["eng"]}"',
          f'CTA (fecho): "{s["cta"]}"', "", "## IMAGENS"]
    # segmento i começa na frase correspondente (distribuição proporcional)
    n, m = len(d["segs"]), len(d["fala"])
    for i, (g, h, hk, img) in enumerate(d["segs"]):
        frase = d["fala"][round(i * (m - 1) / (n - 1))]
        tag = f" [{g}]" if g else ""
        L += [f'IMAGEM {i+1} — "{primeiras(frase)}"{tag}', f"headline: {h}", f"hook: {hk}",
              img + ", photographic, no text, no lettering", ""]
    L += ["## ESTRUTURA", d["estr"], ""]
    return "\n".join(L)


for k in ORDEM:
    p = PUB[k]
    for fn in (alc, aut, pro):
        d = fn(k, p)
        open(f"{BASE}/{k}-{d['tipo']}.md", "w").write(render(d))
print("ok")
