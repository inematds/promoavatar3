"""Volume do entregável — achado de 01/10/2026: os reels saíam a ~−20,5 LUFS (C184), abaixo do
~−14 em que Reels/TikTok/Shorts tocam; o concat por cópia nunca normalizava o áudio."""
import importlib.util
import json
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("montar_reel", RAIZ / "scripts" / "montar-reel.py")
mr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mr)


def baixo(tmp_path):
    v = tmp_path / "baixo.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30:d=6",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=6", "-af", "volume=-24dB",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-shortest", str(v)], check=True)
    return v


def streams(v):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,nb_frames",
                                   "-of", "json", str(v)])
    return {s["codec_type"]: s for s in json.loads(out)["streams"]}


def test_normaliza_para_menos_14_lufs_e_preserva_o_video(tmp_path):
    v = baixo(tmp_path)
    antes_lufs = mr.medir_lufs(str(v))
    antes = streams(v)["video"]
    assert antes_lufs < -20
    depois_lufs = mr.normalizar_volume(v)
    assert abs(depois_lufs - (-14)) <= 1
    assert abs(mr.medir_lufs(str(v)) - (-14)) <= 1
    depois = streams(v)["video"]
    assert depois["codec_name"] == antes["codec_name"] and depois["nb_frames"] == antes["nb_frames"]
