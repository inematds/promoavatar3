#!/usr/bin/env python3
"""Lint estático do ritmo visual em timelines Hyperframes.

Regra dura do motor: não pode haver mais de 4s sem um beat visual real.
Este script é uma rede de segurança automática para detectar buracos de ritmo
em `motion/index.html`; não substitui olhar frames nem fazer QC a olho.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from statistics import mean


NUM_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*$")
CAPTION_RE = re.compile(r"(#cb\d+\b|#captions\b|caption)", re.IGNORECASE)
REPEAT_RE = re.compile(r"repeat\s*:\s*(-?\d+(?:\.\d+)?)")
DURATION_RE = re.compile(r"duration\s*:\s*(\d+(?:\.\d+)?)")


def fail_usage(message: str) -> int:
    print(f"lint-timeline: {message}", file=sys.stderr)
    return 2


def extract_attr(text: str, name: str) -> str | None:
    match = re.search(rf'\b{name}\s*=\s*"([^"]+)"', text)
    return match.group(1) if match else None


def line_for_index(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def strip_comments(text: str) -> str:
    # Evita que invocações comentadas contem como beats reais.
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//.*", "", text)


def find_matching(text: str, start: int, opener: str, closer: str) -> int:
    depth = 0
    quote = ""
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = ""
            continue
        if ch in ('"', "'", "`"):
            quote = ch
        elif ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return i
    return -1


def split_args(args: str) -> list[str]:
    parts: list[str] = []
    start = 0
    stack: list[str] = []
    quote = ""
    escape = False
    pairs = {"(": ")", "{": "}", "[": "]"}
    closers = set(pairs.values())
    for i, ch in enumerate(args):
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = ""
            continue
        if ch in ('"', "'", "`"):
            quote = ch
        elif ch in pairs:
            stack.append(pairs[ch])
        elif ch in closers and stack and ch == stack[-1]:
            stack.pop()
        elif ch == "," and not stack:
            parts.append(args[start:i].strip())
            start = i + 1
    tail = args[start:].strip()
    if tail:
        parts.append(tail)
    return parts


def first_string_arg(args: str) -> str:
    match = re.search(r"""["']([^"']+)["']""", args)
    return match.group(1) if match else ""


def is_caption(selector: str, body: str = "") -> bool:
    haystack = f"{selector} {body}"
    if CAPTION_RE.search(haystack):
        return True
    if ".w" in selector and "captions" in body.lower():
        return True
    return False


def repeat_value(body: str) -> float | None:
    match = REPEAT_RE.search(body)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def max_duration(body: str) -> float:
    values = []
    for match in DURATION_RE.finditer(body):
        try:
            values.append(float(match.group(1)))
        except ValueError:
            pass
    return max(values) if values else 0.0


def is_float(body: str) -> bool:
    repeat = repeat_value(body)
    if repeat is not None and (repeat >= 6 or repeat == -1):
        return True
    if re.search(r"repeat\s*:\s*-1\b", body):
        return True
    if "yoyo" in body and max_duration(body) >= 1.5:
        return True
    return False


def iter_tl_calls(text: str):
    pattern = re.compile(r"\btl\.(to|from|fromTo)\s*\(")
    for match in pattern.finditer(text):
        open_i = text.find("(", match.start())
        close_i = find_matching(text, open_i, "(", ")")
        if close_i == -1:
            continue
        body = text[match.start() : close_i + 1]
        args = text[open_i + 1 : close_i]
        yield match.start(), match.group(1), args, body


def is_real_tween(args: str, body: str) -> bool:
    selector = first_string_arg(args)
    if is_caption(selector, body):
        return False
    if is_float(body):
        return False
    return True


def collect_direct_beats(text: str) -> list[dict]:
    beats = []
    for index, method, args, body in iter_tl_calls(text):
        parts = split_args(args)
        if not parts:
            continue
        match = NUM_RE.match(parts[-1])
        if not match:
            continue
        if not is_real_tween(args, body):
            continue
        beats.append(
            {
                "time": float(match.group(1)),
                "source": f"tl.{method}",
                "line": line_for_index(text, index),
                "selector": first_string_arg(args),
            }
        )
    return beats


def iter_functions(text: str):
    pattern = re.compile(r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\(([^)]*)\)\s*\{")
    for match in pattern.finditer(text):
        open_i = text.find("{", match.end() - 1)
        close_i = find_matching(text, open_i, "{", "}")
        if close_i == -1:
            continue
        params = [p.strip() for p in match.group(2).split(",") if p.strip()]
        body = text[open_i + 1 : close_i]
        yield match.start(), match.group(1), params, body


def helper_has_real_tween(body: str) -> bool:
    saw_tween = False
    saw_real = False
    for _index, _method, args, call_body in iter_tl_calls(body):
        saw_tween = True
        if is_real_tween(args, call_body):
            saw_real = True
    return saw_tween and saw_real


TIME_PARAM_NAMES = {"t", "tin", "tout", "time", "at"}


def param_name(param: str) -> str:
    return param.split("=")[0].strip()


def collect_helpers(text: str) -> dict[str, list[int]]:
    helpers: dict[str, list[int]] = {}
    for _index, name, params, body in iter_functions(text):
        if not params:
            continue
        # O tempo pode vir em qualquer posição da assinatura (`wipe(sel,tin,tout)`,
        # `sIn(sel,t)`, etc.); guardamos todos os seus índices para contá-los como beats.
        time_indexes = [i for i, param in enumerate(params) if param_name(param) in TIME_PARAM_NAMES]
        if not time_indexes:
            continue
        if "tl." not in body:
            continue
        if helper_has_real_tween(body):
            helpers[name] = time_indexes
    return helpers


def collect_helper_beats(text: str, helpers: dict[str, list[int]]) -> list[dict]:
    beats = []
    for name in sorted(helpers):
        pattern = re.compile(rf"(?<!function\s)\b{re.escape(name)}\s*\(")
        for match in pattern.finditer(text):
            open_i = text.find("(", match.start())
            close_i = find_matching(text, open_i, "(", ")")
            if close_i == -1:
                continue
            args = split_args(text[open_i + 1 : close_i])
            if not args:
                continue
            for arg_index in helpers[name]:
                if arg_index >= len(args):
                    continue
                time_match = NUM_RE.match(args[arg_index])
                if not time_match:
                    continue
                beats.append(
                    {
                        "time": float(time_match.group(1)),
                        "source": f"{name}()",
                        "line": line_for_index(text, match.start()),
                        "selector": "",
                    }
                )
    return beats


def dedupe_times(beats: list[dict], threshold: float = 0.15) -> list[float]:
    times = sorted(b["time"] for b in beats)
    merged: list[float] = []
    for value in times:
        if not merged or value - merged[-1] > threshold:
            merged.append(round(value, 3))
    return merged


def compute_gaps(beats: list[float], duration: float, max_gap: float) -> tuple[list[dict], list[dict]]:
    points = [0.0] + beats + [duration]
    gaps = []
    errors = []
    for start, end in zip(points, points[1:]):
        length = round(end - start, 3)
        gap = {"start": round(start, 3), "end": round(end, 3), "len": length}
        gaps.append(gap)
        if length > max_gap:
            errors.append(
                {
                    "time": round(start, 3),
                    "message": (
                        f"Buraco de {length:.1f}s entre {start:.1f}s e {end:.1f}s "
                        "— coloque um beat (snap/selo/B-roll) sincronizado com uma palavra-âncora"
                    ),
                    "gap": gap,
                }
            )
    return gaps, errors


def compute_density(beats: list[float], duration: float, window: float) -> tuple[float, list[dict]]:
    if window <= 0:
        return 0.0, []
    step = 5.0
    starts = []
    current = 0.0
    while current < duration:
        starts.append(round(current, 3))
        current += step
    counts = []
    warnings = []
    for start in starts:
        end = min(duration, start + window)
        count = sum(1 for beat in beats if start <= beat < end)
        counts.append(count)
        if count < 4:
            warnings.append(
                {
                    "time": round(start, 3),
                    "message": (
                        f"Trecho lento: {count} beats entre {start:.1f}s e {end:.1f}s "
                        f"(janela {window:.0f}s); verifique se é respiro intencional"
                    ),
                }
            )
    return (round(mean(counts), 2) if counts else 0.0), warnings


def lint(path: str, max_gap: float, window: float) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        raw = handle.read()

    duration_attr = extract_attr(raw, "data-duration")
    if duration_attr is None:
        raise ValueError("não encontro data-duration no index.html")
    duration = float(duration_attr)
    width = extract_attr(raw, "data-width")
    height = extract_attr(raw, "data-height")

    text = strip_comments(raw)
    direct_beats = collect_direct_beats(text)
    helpers = collect_helpers(text)
    helper_beats = collect_helper_beats(text, helpers)
    beats = dedupe_times(direct_beats + helper_beats)
    gaps, errors = compute_gaps(beats, duration, max_gap)

    warnings = []
    if beats and beats[0] > 1.5:
        warnings.append(
            {
                "time": 0.0,
                "message": (
                    f"Hook latency: o primeiro beat real entra em {beats[0]:.1f}s; "
                    "o corpo deveria começar com movimento visual"
                ),
            }
        )
    elif not beats:
        warnings.append({"time": 0.0, "message": "Não foram detectados beats visuais reais"})

    density, density_warnings = compute_density(beats, duration, window)
    warnings.extend(density_warnings)

    return {
        "duration": duration,
        "width": int(width) if width and width.isdigit() else width,
        "height": int(height) if height and height.isdigit() else height,
        "beats": beats,
        "gaps": gaps,
        "errors": errors,
        "warnings": warnings,
        "density_per_10s": density,
        "exit": 1 if errors else 0,
    }


def print_human(result: dict, path: str) -> None:
    size = ""
    if result.get("width") and result.get("height"):
        size = f" · {result['width']}x{result['height']}"
    print(f"lint-timeline: {path}")
    print(
        f"Duração {result['duration']:.2f}s{size} · "
        f"{len(result['beats'])} beats · densidade média {result['density_per_10s']:.2f} beats/10s"
    )
    print("")
    if not result["errors"] and not result["warnings"]:
        print("OK: sem gaps >4s nem warnings.")
        return
    if result["errors"]:
        print("ERRORS")
        for item in result["errors"]:
            print(f"L{item['time']:.2f} ERROR {item['message']}")
    if result["warnings"]:
        if result["errors"]:
            print("")
        print("WARNINGS")
        for item in result["warnings"]:
            print(f"L{item['time']:.2f} WARN {item['message']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint estático de beats visuais Hyperframes.")
    parser.add_argument("index_html", help="Caminho para motion/index.html")
    parser.add_argument("--max-gap", type=float, default=4.0, help="Buraco máximo permitido entre beats")
    parser.add_argument("--window", type=float, default=10.0, help="Janela de densidade em segundos")
    parser.add_argument("--json", action="store_true", help="Imprime apenas JSON")
    args = parser.parse_args(argv)

    if not os.path.exists(args.index_html):
        return fail_usage(f"arquivo não existe: {args.index_html}")

    try:
        result = lint(args.index_html, args.max_gap, args.window)
    except Exception as exc:
        return fail_usage(str(exc))

    if args.json:
        public = {k: result[k] for k in ("duration", "beats", "gaps", "errors", "warnings", "density_per_10s", "exit")}
        print(json.dumps(public, ensure_ascii=False, separators=(",", ":")))
    else:
        print_human(result, args.index_html)
    return int(result["exit"])


if __name__ == "__main__":
    raise SystemExit(main())
