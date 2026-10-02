"""Opcao --troca-s (2026-10-02): imagem do topo trocando a cada ~2-3 s com variacoes da mesma cena.
Desligada por padrao. Pendencia: docs/pendente-troca-imagem.md."""
import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
spec = importlib.util.spec_from_file_location("preparar", RAIZ / "scripts" / "preparar.py")
prep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prep)


def test_desligado_nao_cria_variacao():
    assert prep.plano_variantes([0, 6.3, 15], 20, 0) == [[], [], []]


def test_segmento_longo_ganha_variacoes_repartidas():
    # C184: imagem parada de 18,8 s a 35 s (16,2 s)
    plano = prep.plano_variantes([0.0, 18.8], 35.0, 2.5)
    assert plano[1] == [round(18.8 + 16.2 * j / 5, 3) for j in range(1, 5)]   # no maximo 4 extras: fatias de 3,24 s
    assert prep.plano_variantes([0.0], 16.2, 2.5, max_extra=2)[0] == [5.4, 10.8]


def test_segmento_curto_nao_ganha_variacao():
    # 2,4 s cabe numa imagem; 2,6 s pediria 1 variacao, mas cada fatia ficaria com 1,3 s < MIN_CARD
    assert prep.plano_variantes([0.0, 2.4], 5.0, 2.5) == [[], []]


def test_nenhuma_fatia_menor_que_o_minimo():
    for ini, fim in [(0, 3.2), (0, 4.0), (0, 9.0), (0, 16.2)]:
        plano = prep.plano_variantes([ini], fim, 2.5)[0]
        marcos = [ini] + plano + [fim]
        assert all(b - a >= prep.MIN_CARD - 1e-9 for a, b in zip(marcos, marcos[1:]))
