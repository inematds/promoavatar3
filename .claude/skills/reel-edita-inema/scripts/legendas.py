#!/usr/bin/env python3
"""Legenda palavra a palavra do reel — ver docs/legenda.md.

Le o transcript com tempo por palavra (`edicion/transcript.json`, produzido
pelo transcribe-groq.sh) e o .md do publico, e emite `edicion/legendas.json`:

    [{"start": 1.0, "dur": 0.4, "palavra": "PRODUCAO", "kw": true}, ...]

Uma entrada por palavra. `kw` marca as que acendem no acento (ambar); as demais
saem na cor base (branca). As keywords vem das `## SOBREPOSICOES` do .md — a
fase 1 ja escreveu ali as frases que importam.

NAO existe fallback de "destaca a palavra mais longa" (o captions.py da skill
global tem, porque agrupa em blocos de 3). Em formato de uma palavra por vez
aquela regra degenera para "tudo ambar". Sem keyword, legenda toda branca e um
resultado valido.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# Palavras de funcao nunca viram acento: aparecem em toda frase e destacariam
# o nada. A regra de tamanho sozinha nao pega "nao"/"que"/"seu".
VAZIAS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas", "de", "do", "da", "dos",
    "das", "em", "no", "na", "nos", "nas", "por", "para", "pra", "com", "sem",
    "e", "ou", "mas", "que", "se", "ao", "aos", "as", "ja", "so", "nao", "sim",
    "seu", "sua", "seus", "suas", "meu", "minha", "ele", "ela", "voce", "isso",
    "este", "esta", "esse", "essa", "aquilo", "quem", "qual", "quanto",
    "quantas", "quantos", "hoje", "agora", "mais", "menos", "muito", "tem",
    "ter", "foi", "era", "ser", "esta", "estao", "sao", "vai", "vao", "faz",
    "fazer", "todo", "toda", "todos", "todas", "cada", "entre", "sobre",
}
MIN_LETRAS = 4

# Rotulos das linhas de SOBREPOSICOES — sao estrutura, nao conteudo. A fase de
# texto ja escreveu isto de duas formas:
#   ATENCAO: o nivel mais perigoso...            (A#35 e anteriores)
#   - **ATENÇÃO (0–2s)** — ELE ACHOU A IA...     (A#49 em diante)
# Os dois precisam ser aparados, senao "atencao"/"engajamento" viram acento.
MARCADOR = re.compile(r"^\s*[-*+•]\s*")
ROTULO = re.compile(
    r"^\s*(?:\*\*)?[A-ZÀ-Ú][A-ZÀ-Ú\s]{2,}(?:\s*\([^)]*\))?(?:\*\*)?\s*(?::|[—–-])\s*"
)
# Mesmo aparados, os nomes dos gatilhos aparecem soltos no meio do texto.
ESTRUTURA = {"atencao", "retencao", "engajamento", "cta", "gancho", "fecho",
             "miolo", "reel", "tela", "falar", "fase"}


def norm(s: str) -> str:
    """minuscula, sem acento, sem pontuacao — para comparar palavras."""
    s = unicodedata.normalize("NFD", (s or "").strip().lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


def _e_cabecalho_sobreposicoes(linha: str) -> bool:
    return linha.lstrip("#").strip().lower().startswith("sobreposi")


def keywords_do_md(texto: str) -> set:
    """Palavras fortes das `## SOBREPOSICOES` — o acento ambar da legenda.

    So essa secao conta: headline e hook (secao IMAGENS) ja tem acento proprio
    no topo e na base do reel, e reaproveita-los aqui espalharia o ambar pelas
    tres faixas ao mesmo tempo.
    """
    dentro, kws = False, set()
    for linha in (texto or "").splitlines():
        if linha.startswith("#"):
            dentro = _e_cabecalho_sobreposicoes(linha)
            continue
        if not dentro or not linha.strip():
            continue
        conteudo = ROTULO.sub("", MARCADOR.sub("", linha))
        for bruto in re.split(r"[\s—–-]+", conteudo):
            p = norm(bruto)
            if len(p) >= MIN_LETRAS and p not in VAZIAS and p not in ESTRUTURA:
                kws.add(p)
    return kws


def _limpar(bruto: str) -> str:
    """Tira pontuação das pontas e sobe para caixa alta.

    `ANOS,` vira `ANOS`: em legenda de uma palavra a virgula nao separa nada,
    so suja. Um token que era so pontuacao vira "" e o chamador descarta.
    """
    return re.sub(r"^\W+|\W+$", "", (bruto or ""), flags=re.UNICODE).upper()


def montar(transcript: dict, kws: set) -> list:
    """Uma entrada por palavra, sem buraco entre elas."""
    ws = transcript.get("words") or []
    ws = [w for w in ws if w.get("start") is not None]

    limpas = []
    for w in ws:
        palavra = _limpar(w.get("word", ""))
        if palavra:
            limpas.append((palavra, float(w["start"]), float(w.get("end") or w["start"])))

    saida = []
    for i, (palavra, ini, fim) in enumerate(limpas):
        # Ate o inicio da proxima: sem lacuna, a legenda nao pisca entre
        # palavras. Na ultima, a duracao propria mais um respiro.
        # Sem piso de duracao quando ha proxima: o ASR devolve palavras de 40ms
        # e um piso as empurraria por cima da seguinte — duas na tela de uma vez.
        prox = limpas[i + 1][1] if i + 1 < len(limpas) else None
        dur = (prox - ini) if prox is not None else max(fim - ini, 0.05) + 0.15
        saida.append({
            "start": round(ini, 3),
            "dur": round(dur, 3),
            "palavra": palavra,
            "kw": norm(palavra) in kws,
        })
    return saida


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="legenda palavra a palavra do reel")
    p.add_argument("--transcript", required=True,
                   help="edicion/transcript.json (words[{word,start,end}])")
    p.add_argument("--md", help="texto do publico; as SOBREPOSICOES viram o acento")
    p.add_argument("--out", default="legendas.json")
    a = p.parse_args(argv)

    tr_arq = Path(a.transcript)
    if not tr_arq.exists() or tr_arq.stat().st_size == 0:
        print(f"legendas: sem transcript em {tr_arq} — reel sai sem legenda",
              file=sys.stderr)
        return 2

    transcript = json.loads(tr_arq.read_text(encoding="utf-8"))
    kws = keywords_do_md(Path(a.md).read_text(encoding="utf-8")) if a.md else set()
    dados = montar(transcript, kws)

    saida = Path(a.out)
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")

    acesas = sum(1 for d in dados if d["kw"])
    print(f"legendas   {len(dados)} palavras · {acesas} no acento · {saida}")
    if not kws:
        print("           sem keywords nas SOBREPOSICOES — legenda toda branca")
    return 0


if __name__ == "__main__":
    sys.exit(main())
