#!/usr/bin/env python3
"""文書から「実際に読み込まれる参照」だけを取り出すヘルパー（python3 標準ライブラリのみ）。

コードサンプル（<pre> 内の埋め込みコード、Markdown のコードブロック/コードスパン）は
データであって読み込み参照ではないため、走査前にマスクする。
"""

from __future__ import annotations

import re

HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
HTML_PRE_RE = re.compile(r"<pre\b[^>]*>.*?</pre>", re.DOTALL | re.IGNORECASE)
HTML_CODE_RE = re.compile(r"<code\b[^>]*>.*?</code>", re.DOTALL | re.IGNORECASE)
HTML_STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE)
HTML_SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE)
MD_FENCE_RE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
MD_INLINE_RE = re.compile(r"`[^`\n]*`")
MASK = "\u0000"

IGNORE_PREFIXES = ("#", "mailto:", "tel:", "data:", "javascript:", "http://", "https://", "//")
EXTENSION_RE = re.compile(
    r"\.(?:html|markdown|md|css|js|mjs|json|svg|png|jpe?g|webp|gif|txt|yaml|yml)$", re.IGNORECASE
)
ATTR_RE = re.compile(r"\b(?P<name>src|href|data|poster|xlink:href)\s*=\s*(?P<quote>[\"'])(?P<value>.*?)(?P=quote)", re.DOTALL)
MD_LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\((?P<value>[^)\s]+)\)")
MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\((?P<value>[^)\s]+)\)")
FRAGMENT_ATTR_RE = re.compile(r"\b(?:id|name)\s*=\s*[\"'](?P<id>[A-Za-z0-9._:-]+)[\"']")
HEADING_RE = re.compile(r"^#{1,6}\s+(?P<title>.+?)\s*$", re.MULTILINE)
PATH_TOKEN_RE = re.compile(
    r"(?<![\w./-])(?:\.{0,2}/)?(?:[A-Za-z0-9._-]+/)+[A-Za-z0-9._*,-]+\.(?:html|markdown|json|mjs|css|svg|png|jpe?g|webp|gif|md|js|py)(?![\w])",
    re.IGNORECASE,
)


def mask_html(text: str) -> str:
    """HTML からコードサンプル・スタイル・スクリプト・コメントを除いた文字列を返す。"""
    masked = HTML_COMMENT_RE.sub(MASK, text)
    masked = HTML_PRE_RE.sub(MASK, masked)
    masked = HTML_CODE_RE.sub(MASK, masked)
    masked = HTML_STYLE_RE.sub(MASK, masked)
    masked = HTML_SCRIPT_RE.sub(MASK, masked)
    return masked


def mask_markdown(text: str) -> str:
    """Markdown からフェンスコードブロックとインラインコードを除いた文字列を返す。"""
    masked = MD_FENCE_RE.sub(MASK, text)
    masked = MD_INLINE_RE.sub(MASK, masked)
    return masked


def is_relative_reference(value: str) -> bool:
    value = value.strip()
    if not value or value.startswith(IGNORE_PREFIXES):
        return False
    path = value.split("#", 1)[0].split("?", 1)[0]
    if not path:
        return False
    if path.startswith("/"):
        return True  # 絶対パスは参照エラーとして扱いたい
    return bool(EXTENSION_RE.search(path))


def references(text: str, kind: str) -> list:
    """(参照文字列, 参照元の種類) のリストを返す。kind は "html" か "md"。"""
    found = set()
    if kind == "html":
        masked = mask_html(text)
        for match in ATTR_RE.finditer(masked):
            value = match.group("value").strip()
            if is_relative_reference(value):
                found.add(value)
    else:
        masked = mask_markdown(text)
        for match in MD_LINK_RE.finditer(masked):
            value = match.group("value").strip()
            if is_relative_reference(value):
                found.add(value)
        for match in MD_IMAGE_RE.finditer(masked):
            value = match.group("value").strip()
            if is_relative_reference(value):
                found.add(value)
        # Markdown 内に生の HTML タグ（iframe 等）を書く場合も拾う
        for value in references(text, "html"):
            found.add(value)
    return sorted({value.split("?")[0] for value in found})


def fragments(text: str, kind: str) -> set:
    """ページ内アンカーとして解決できる id / name / 見出しスラグの集合。"""
    ids = set(FRAGMENT_ATTR_RE.findall(text))
    if kind == "md":
        for title in HEADING_RE.findall(text):
            slug = re.sub(r"[^\w\s-]", "", title.strip().lower())
            ids.add(re.sub(r"\s+", "-", slug))
    return ids


def path_tokens(text: str) -> list:
    """本文中のパスらしき文字列（ワイルドカード可）を返す。

    ドキュメントでは `examples/css/NN-*.html` のように ID を NN と書くため、
    glob 用に NN を * として扱う。
    """
    tokens = set()
    for match in PATH_TOKEN_RE.finditer(text):
        token = re.sub(r"(?<![A-Za-z0-9])NN(?=[-_./])", "*", match.group(0))
        tokens.add(token)
    return sorted(tokens)


def mask_css_blocks(text: str, header_regex: re.Pattern) -> str:
    """header_regex に一致する CSS ブロック（@keyframes 等）をコメント化して返す。"""
    result = text
    for match in header_regex.finditer(text):
        brace = text.find("{", match.start())
        if brace == -1:
            continue
        end = brace
        depth = 0
        while end < len(text):
            if text[end] == "{":
                depth += 1
            elif text[end] == "}":
                depth -= 1
                if depth == 0:
                    break
            end += 1
        result = result.replace(text[match.start() : end + 1], "/* masked */")
    return result
