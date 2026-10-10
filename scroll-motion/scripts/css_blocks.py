#!/usr/bin/env python3
"""CSS のブロック構造を調べる小さなヘルパー（python3 標準ライブラリのみ）。"""

from __future__ import annotations

import re

MEDIA_RE = re.compile(
    r"@media\s*\((?P<condition>[^{)]*)\)\s*\{",
    re.IGNORECASE,
)


def _match_brace(text: str, open_index: int) -> int:
    """open_index の '{' に対応する '}' の位置を返す（見つからなければ len(text)）。"""
    depth = 0
    index = open_index
    while index < len(text):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return len(text)


def media_blocks(text: str):
    """(condition, start, end) のリスト。start は '{'、end は対応する '}' の位置。"""
    blocks = []
    for match in MEDIA_RE.finditer(text):
        brace = text.find("{", match.start())
        end = _match_brace(text, brace)
        blocks.append((match.group("condition").strip(), brace, end))
    return blocks


def innermost_condition(blocks, position: int):
    """position を含む最も内側の @media 条件を返す。含まれなければ None。"""
    best = None
    for condition, start, end in blocks:
        if start < position < end:
            if best is None or start > best[1]:
                best = (condition, start)
    return best[0] if best else None


def has_condition(condition: str, needle: str) -> bool:
    normalized = re.sub(r"\s+", " ", condition.lower())
    return needle.lower() in normalized


def block_body(text: str, condition_needle: str) -> str:
    """条件に needle を含むブロックの本体を連結して返す。"""
    bodies = []
    for condition, start, end in media_blocks(text):
        if has_condition(condition, condition_needle):
            bodies.append(text[start + 1 : end])
    return "\n".join(bodies)
