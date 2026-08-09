"""Partes puras do gen-imagem.py — sem rede, sem chave, sem GPU.

O que a rede prova (que a Agnes responde, que o inemaimg gera) esta verificado a
mao e anotado no README. O que ESTE arquivo protege e o que quebra em silencio:
o tamanho exato do PNG, de que o preparar.py depende para reaproveitar imagem.
"""
import base64
import importlib.util
import io
import struct
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parent
ALVO = AQUI.parent / "scripts" / "gen-imagem.py"

spec = importlib.util.spec_from_file_location("gen_imagem", ALVO)
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)


def png_de(largura, altura):
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", (largura, altura), (10, 20, 30)).save(buf, format="PNG")
    return buf.getvalue()


class TestDimensoes:
    def test_le_do_cabecalho_ihdr(self):
        assert gen.dimensoes(png_de(1088, 704)) == (1088, 704)

    def test_lixo_nao_explode(self):
        assert gen.dimensoes(b"nao sou png") == (0, 0)


class TestNormalizar:
    def test_no_tamanho_certo_devolve_intacto(self):
        # Nao reescrever importa: reescrever mudaria os bytes e o hash a toa.
        original = png_de(1088, 704)
        saida, nota = gen.normalizar(original, 1088, 704)
        assert saida is original
        assert nota == ""

    def test_tamanho_diferente_vira_o_exato(self):
        # E o caso REAL da Agnes: pedimos 1088x704, ela devolveu 1248x832.
        saida, nota = gen.normalizar(png_de(1248, 832), 1088, 704)
        assert gen.dimensoes(saida) == (1088, 704)
        assert "1248x832 -> 1088x704" in nota

    def test_corta_pelo_centro_em_vez_de_esticar(self):
        # Proporcao bem diferente: 1:1 para 3:2. Esticar deformaria rosto, e a
        # faixa do topo do reel e quase sempre uma pessoa.
        from PIL import Image
        buf = io.BytesIO()
        im = Image.new("RGB", (800, 800), (0, 0, 0))
        # marca so a faixa central horizontal: ela tem que sobreviver ao corte
        for y in range(360, 440):
            for x in range(800):
                im.putpixel((x, y), (255, 0, 0))
        im.save(buf, format="PNG")

        saida, _ = gen.normalizar(buf.getvalue(), 1088, 704)
        assert gen.dimensoes(saida) == (1088, 704)
        fora = Image.open(io.BytesIO(saida))
        # o centro continua vermelho — o corte pegou o meio, nao um canto
        assert fora.getpixel((544, 352))[0] > 200

    def test_menor_que_o_pedido_tambem_e_corrigido(self):
        saida, nota = gen.normalizar(png_de(512, 512), 1088, 704)
        assert gen.dimensoes(saida) == (1088, 704)
        assert "512x512" in nota


class TestExtrairB64:
    def test_formato_do_inemaimg(self):
        assert gen.extrair_b64({"image_base64": "x" * 200}) == "x" * 200

    def test_formato_da_agnes_data_b64_json(self):
        j = {"data": [{"b64_json": "y" * 200, "url": "http://tmp", "revised_prompt": "..."}]}
        assert gen.extrair_b64(j) == "y" * 200

    def test_lista_images_de_strings(self):
        assert gen.extrair_b64({"images": ["z" * 200]}) == "z" * 200

    def test_resposta_sem_imagem_devolve_none(self):
        # Devolver None (e nao explodir) e o que deixa o chamador dar erro claro
        # com as chaves que vieram — o diagnostico caro de provedor novo.
        assert gen.extrair_b64({"erro": "cota"}) is None

    def test_campo_curto_nao_conta_como_imagem(self):
        assert gen.extrair_b64({"image": "abc"}) is None


class TestBytesDe:
    def test_base64_puro(self):
        assert gen.bytes_de(base64.b64encode(b"ola").decode()) == b"ola"

    def test_data_uri_tem_o_prefixo_removido(self):
        uri = "data:image/png;base64," + base64.b64encode(b"ola").decode()
        assert gen.bytes_de(uri) == b"ola"


class TestChave:
    def test_ambiente_vence(self, monkeypatch):
        monkeypatch.setenv("MINHA_CHAVE", "do-ambiente")
        assert gen.chave("MINHA_CHAVE") == "do-ambiente"

    def test_le_do_arquivo_apontado(self, monkeypatch, tmp_path):
        arq = tmp_path / "seg.env"
        arq.write_text('# comentario\nMINHA_CHAVE="do-arquivo"\nOUTRA=1\n')
        monkeypatch.delenv("MINHA_CHAVE", raising=False)
        monkeypatch.setenv("IMG_ENV_PATH", str(arq))
        assert gen.chave("MINHA_CHAVE") == "do-arquivo"

    def test_sem_nenhum_dos_dois_sai_com_erro_claro(self, monkeypatch, capsys):
        monkeypatch.delenv("MINHA_CHAVE", raising=False)
        monkeypatch.setenv("IMG_ENV_PATH", "/nao/existe")
        with pytest.raises(SystemExit) as e:
            gen.chave("MINHA_CHAVE")
        assert e.value.code == 5
        assert "MINHA_CHAVE" in capsys.readouterr().err
