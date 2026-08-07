#!/usr/bin/env bash
# transcribe-groq.sh <audio_in> <json_out>  — word-level via Groq whisper-large-v3-turbo (pt)
set -euo pipefail
IN="$1"; OUT="$2"
# carrega GROQ_API_KEY em runtime (nunca imprime)
set -a; . /home/nmaldaner/projetos/openpcbotv2/.env; set +a
python3 - "$IN" "$OUT" <<'PY'
import sys, os, json, urllib.request, mimetypes, uuid
inp, out = sys.argv[1], sys.argv[2]
key = os.environ["GROQ_API_KEY"]
url = "https://api.groq.com/openai/v1/audio/transcriptions"
boundary = "----gq" + uuid.uuid4().hex
def part(name, value):
    return (f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n').encode()
data = open(inp, "rb").read()
fn = os.path.basename(inp)
body = b""
body += part("model", "whisper-large-v3-turbo")
body += part("language", "pt")
body += part("response_format", "verbose_json")
body += (f'--{boundary}\r\nContent-Disposition: form-data; name="timestamp_granularities[]"\r\n\r\nword\r\n').encode()
body += (f'--{boundary}\r\nContent-Disposition: form-data; name="timestamp_granularities[]"\r\n\r\nsegment\r\n').encode()
body += (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{fn}"\r\n'
         f'Content-Type: application/octet-stream\r\n\r\n').encode() + data + b"\r\n"
body += (f'--{boundary}--\r\n').encode()
req = urllib.request.Request(url, data=body, headers={
    "Authorization": f"Bearer {key}",
    "Content-Type": f"multipart/form-data; boundary={boundary}",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
})
with urllib.request.urlopen(req, timeout=300) as r:
    j = json.loads(r.read())
# normaliza para {"text":..., "words":[{word,start,end}], "segments":[...]}
words = j.get("words", []) or []
norm = {"text": j.get("text",""), "words": words, "segments": j.get("segments", [])}
json.dump(norm, open(out,"w"), ensure_ascii=False, indent=2)
print(f"OK transcript -> {out} · {len(words)} words · dur~{(words[-1]['end'] if words else 0):.1f}s")
PY
