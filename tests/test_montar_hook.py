"""Posição e corpo do texto da faixa de BASE (o `hook`) no reel empilhado.

Pedido do dono em 2026-08-13, olhando reels prontos: o texto da base ficava
centralizado na vertical, no meio de 608 px — parecia solto, longe do avatar.
Ele quer o texto "quase no topo do quadro inferior", com respiro de 2 linhas, e
letra maior. Continua centralizado na HORIZONTAL.
"""
import importlib.util
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

spec = importlib.util.spec_from_file_location("montar", RAIZ / "scripts" / "montar.py")
montar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(montar)

CAPA = json.loads((RAIZ / "templates" / "empilhado-capa.json").read_text())
HOOK = CAPA["faixas"]["base"]["hook"]


class TestTopoDoHook:
    def test_respiro_de_duas_linhas(self):
        # 2 linhas de respiro = 2 x (tamanho x entrelinha). Com 66/1.2 dá 158px,
        # que é onde o texto começa — nao mais no meio dos 608.
        hk = {"tamanho": 66, "entrelinha": 1.2, "respiro_linhas": 2}
        assert montar.topo_do_hook(hk) == round(2 * 66 * 1.2)

    def test_sem_respiro_declarado_o_default_e_duas_linhas(self):
        # O default vale para qualquer template que ganhe hook depois: o pedido
        # foi de posicao, nao de excecao de um arquivo.
        assert montar.topo_do_hook({"tamanho": 50, "entrelinha": 1.0}) == 100

    def test_respiro_zero_encosta_no_topo_da_faixa(self):
        assert montar.topo_do_hook({"tamanho": 66, "entrelinha": 1.2, "respiro_linhas": 0}) == 0

    def test_nunca_empurra_o_texto_para_fora_da_faixa(self):
        # Teto: respiro absurdo nao pode jogar o texto para fora dos 608px de
        # base — sairia do quadro sem erro nenhum, so um reel com base vazia.
        alto = montar.topo_do_hook({"tamanho": 66, "entrelinha": 1.2, "respiro_linhas": 99})
        assert alto <= montar.ALTURA_BASE_PADRAO // 2


class TestTemplateCapa:
    def test_a_letra_ficou_maior(self):
        # Era 56. "Letras maiores" foi pedido explicito.
        assert HOOK["tamanho"] > 56

    def test_o_respiro_esta_declarado_no_template(self):
        assert HOOK["respiro_linhas"] == 2

    def test_cabe_pelo_menos_tres_linhas_depois_do_respiro(self):
        # Com respiro + 3 linhas o texto tem que caber nos 608 da faixa, senao a
        # terceira linha some no corte e ninguem ve o fim da frase.
        altura_linha = HOOK["tamanho"] * HOOK["entrelinha"]
        usado = montar.topo_do_hook(HOOK) + 3 * altura_linha
        assert usado <= CAPA["faixas"]["base"]["altura"]

    def test_continua_centralizado_na_horizontal(self):
        # A margem lateral e simetrica: e ela que centra o bloco, com o
        # text-align:center centrando as linhas dentro dele.
        assert HOOK["margem_lateral"] > 0

    def test_so_o_empilhado_capa_tem_hook(self):
        # A mudanca vale so para este template — foi a restricao do dono.
        outros = [p for p in (RAIZ / "templates").glob("*.json")
                  if p.name != "empilhado-capa.json"]
        for p in outros:
            base = json.loads(p.read_text()).get("faixas", {}).get("base", {})
            assert "hook" not in base, f"{p.name} ganhou hook — revise a mudanca"
