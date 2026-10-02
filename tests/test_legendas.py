"""Testes do scripts/legendas.py — ver docs/legenda.md."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "legendas", AQUI.parent / "scripts" / "legendas.py")
legendas = importlib.util.module_from_spec(spec)
sys.modules["legendas"] = legendas
spec.loader.exec_module(legendas)


# ---------- keywords vindas das SOBREPOSICOES ----------

MD = """Formato escolhido: opiniao contraria

### FALA
O nivel mais perigoso nao e o do leigo.

## SOBREPOSICOES
ATENCAO: o nivel mais perigoso nao e o do leigo — e o seu
RETENCAO: vinte assinaturas e nenhum sistema em producao
ENGAJAMENTO: comenta quantas assinaturas de IA voce paga hoje
CTA: trilha FEA-IA — Engenharia de Agentes, no inema.club

## IMAGENS
IMAGEM 1 — "algo" [ATENCAO]
headline: NAO ENTRA | NA LEGENDA
"""


def test_keywords_saem_das_sobreposicoes():
    kws = legendas.keywords_do_md(MD)
    assert "perigoso" in kws
    assert "assinaturas" in kws
    assert "producao" in kws


def test_keywords_ignoram_palavras_de_funcao_e_curtas():
    kws = legendas.keywords_do_md(MD)
    for fraca in ("o", "e", "de", "no", "nao", "que", "seu"):
        assert fraca not in kws, f"{fraca!r} nao devia virar keyword"


def test_keywords_ignoram_secoes_fora_de_sobreposicoes():
    """A secao IMAGENS tem headline/hook; nada dali pode virar acento."""
    kws = legendas.keywords_do_md(MD)
    assert "entra" not in kws
    assert "legenda" not in kws


def test_keywords_ignoram_o_rotulo_da_linha():
    """ATENCAO/RETENCAO/ENGAJAMENTO/CTA sao rotulos, nao conteudo."""
    kws = legendas.keywords_do_md(MD)
    for rotulo in ("atencao", "retencao", "engajamento", "cta"):
        assert rotulo not in kws


def test_md_sem_sobreposicoes_nao_quebra():
    assert legendas.keywords_do_md("### FALA\nnada aqui\n") == set()


# ---------- normalizacao ----------

@pytest.mark.parametrize("bruto,esperado", [
    ("Produção", "producao"),
    ("ANOS,", "anos"),
    ("inema.club", "inemaclub"),
    ("  Arquitetura!  ", "arquitetura"),
])
def test_norm(bruto, esperado):
    assert legendas.norm(bruto) == esperado


# ---------- montagem das palavras ----------

def tr(*trios):
    return {"words": [{"word": w, "start": s, "end": e} for w, s, e in trios]}


def test_palavra_vira_caixa_alta_sem_pontuacao():
    r = legendas.montar(tr(("anos,", 1.0, 1.4)), set())
    assert r[0]["palavra"] == "ANOS"


def test_duracao_vai_ate_o_inicio_da_proxima_sem_buraco():
    r = legendas.montar(tr(("um", 1.0, 1.2), ("dois", 1.5, 1.9)), set())
    assert r[0]["start"] == pytest.approx(1.0)
    assert r[0]["start"] + r[0]["dur"] == pytest.approx(r[1]["start"])


def test_palavra_curtissima_nao_invade_a_proxima():
    """ASR devolve palavras de 40ms. Um piso de duracao as empurraria por cima
    da seguinte — duas palavras na tela ao mesmo tempo."""
    r = legendas.montar(tr(("um", 3.22, 3.25), ("para", 3.26, 3.5)), set())
    assert r[0]["start"] + r[0]["dur"] == pytest.approx(r[1]["start"])


def test_asr_fora_de_ordem_nao_gera_duracao_negativa():
    """Bug de 01/10/2026: 803 de 1.966 reels tinham palavra com dur <= 0 (o ASR devolve
    palavras fora de ordem ou com o mesmo inicio). No C184 'APARECER' ficou presa na
    tela e as palavras seguintes foram desenhadas por cima dela."""
    r = legendas.montar(tr(("aparecer", 24.70, 24.9), ("seu", 24.64, 24.7),
                           ("agente", 25.0, 25.4)), set())
    assert [p["palavra"] for p in r] == ["SEU", "APARECER", "AGENTE"]
    assert all(p["dur"] > 0 for p in r)
    for a, b in zip(r, r[1:]):
        assert a["start"] + a["dur"] <= b["start"] + 1e-9


def test_mesmo_inicio_empurra_a_seguinte_sem_sobrepor():
    r = legendas.montar(tr(("um", 1.0, 1.2), ("dois", 1.0, 1.3), ("tres", 1.5, 1.8)), set())
    assert all(p["dur"] > 0 for p in r)
    for a, b in zip(r, r[1:]):
        assert a["start"] + a["dur"] <= b["start"] + 1e-9


def test_ultima_palavra_tem_duracao_propria():
    r = legendas.montar(tr(("fim", 2.0, 2.6)), set())
    assert r[-1]["dur"] > 0


def test_keyword_marca_kw():
    r = legendas.montar(tr(("Produção", 1.0, 1.4), ("e", 1.4, 1.5)), {"producao"})
    assert r[0]["kw"] is True
    assert r[1]["kw"] is False


def test_sem_keyword_nenhuma_acende():
    """Sem fallback de 'palavra mais longa' — legenda toda branca e valida."""
    r = legendas.montar(tr(("arquitetura", 1.0, 1.6), ("um", 1.6, 1.7)), set())
    assert [p["kw"] for p in r] == [False, False]


def test_palavra_sem_start_e_descartada():
    t = {"words": [{"word": "a", "start": None, "end": 1.0},
                   {"word": "b", "start": 1.0, "end": 1.4}]}
    r = legendas.montar(t, set())
    assert [p["palavra"] for p in r] == ["B"]


def test_palavra_que_vira_vazia_e_descartada():
    """Um token so de pontuacao nao pode virar um quadro em branco."""
    r = legendas.montar(tr(("—", 1.0, 1.1), ("ok", 1.1, 1.4)), set())
    assert [p["palavra"] for p in r] == ["OK"]


def test_transcript_vazio_devolve_lista_vazia():
    assert legendas.montar({"words": []}, set()) == []


# ---------- fim a fim ----------

def test_cli_grava_json(tmp_path):
    t = tmp_path / "transcript.json"
    t.write_text(json.dumps(tr(("Produção", 1.0, 1.5), ("importa", 1.5, 2.0))))
    md = tmp_path / "pub.md"
    md.write_text(MD.replace("nenhum sistema em producao",
                             "nenhum sistema em produção"), encoding="utf-8")
    out = tmp_path / "legendas.json"
    assert legendas.main(["--transcript", str(t), "--md", str(md),
                          "--out", str(out)]) == 0
    dados = json.loads(out.read_text())
    assert [p["palavra"] for p in dados] == ["PRODUÇÃO", "IMPORTA"]
    assert dados[0]["kw"] is True


# Formato NOVO das sobreposicoes (visto em A#49-A#52): lista com negrito e o
# rotulo entre asteriscos, com faixa de tempo. O parser antigo so tirava rotulo
# no formato "ATENCAO: texto", entao "atencao"/"engajamento" vazavam como
# keyword e o ambar acendia em meio texto.
MD_LISTA = """### FALA
tanto faz

### SOBREPOSICOES DE TELA (fase do reel — NAO falar)
- **ATENCAO (0-2s)** — ELE ACHOU A IA | QUE DAVA DINHEIRO
- **RETENCAO (miolo)** — o erro nao foi a ferramenta, foi confundir ferramenta com ativo
- **ENGAJAMENTO** — "Comenta quantos anos voce tem de profissao"
- **CTA (fecho)** — INEMA.CLUB | O CAMINHO CERTO DA IA

### IMAGENS
IMAGEM 1 — "algo"
headline: NAO ENTRA
"""


def test_lista_com_negrito_tambem_da_keywords():
    kws = legendas.keywords_do_md(MD_LISTA)
    assert "ferramenta" in kws
    assert "ativo" in kws


def test_rotulos_do_formato_lista_nao_viram_keyword():
    kws = legendas.keywords_do_md(MD_LISTA)
    for rotulo in ("atencao", "retencao", "engajamento", "cta"):
        assert rotulo not in kws, f"{rotulo!r} e estrutura, nao conteudo"


def test_marcacao_de_negrito_nao_gruda_na_palavra():
    kws = legendas.keywords_do_md(MD_LISTA)
    assert not any("*" in k for k in kws)


def test_secao_com_titulo_longo_ainda_e_reconhecida():
    """`### SOBREPOSICOES DE TELA (fase do reel — NAO falar)` conta."""
    assert legendas.keywords_do_md(MD_LISTA)


def test_acento_fica_escasso():
    """O ambar precisa ser raro para significar algo."""
    kws = legendas.keywords_do_md(MD_LISTA)
    assert len(kws) <= 18, f"{len(kws)} keywords e acento demais: {sorted(kws)}"
