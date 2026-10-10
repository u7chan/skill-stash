#!/usr/bin/env python3
"""外部依存（外部ネットワーク読み込み）チェック。

showroom / examples / SKILL.md / references が、外部の CSS・JS・フォント・画像・API を
読み込んでいないことを検証する。オフラインで動作するために http(s) / プロトコル相対の
「読み込み参照」を禁止する。

許容するもの:
- 出典・参考リンクとしての `<a href="https://...">` と Markdown の `[text](https://...)`
- `data:` URI（外部リクエストを発生させない）
- リポジトリ内の相対パス
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import catalog_lib  # noqa: E402

EXTERNAL_RE = re.compile(r"^(?:https?:)?//", re.IGNORECASE)
TAG_RE = re.compile(
    r"<(?P<tag>script|link|img|iframe|source|video|audio|track|embed|object|use|image|input|form)\b[^>]*>",
    re.IGNORECASE | re.DOTALL,
)
ATTR_RE = re.compile(r"(?P<name>[A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*(?P<quote>[\"'])(?P<value>.*?)(?P=quote)", re.DOTALL)
CSS_URL_RE = re.compile(r"url\(\s*['\"]?(?P<value>[^'\")]+)['\"]?\s*\)", re.IGNORECASE)
CSS_IMPORT_RE = re.compile(r"@import\s+(?:url\(\s*['\"]?[^'\")]+['\"]?\s*\)|['\"](?P<value>[^'\"]+)['\"])", re.IGNORECASE)
JS_PATTERNS = (
    re.compile(r"""\bimport\s*\(\s*['"`](?P<value>[^'"`]+)['"`]"""),
    # 副作用 import（バインディングなし）
    re.compile(r"""\bimport\s+['"](?P<value>[^'"]+)['"]"""),
    re.compile(r"""\bfrom\s*['"](?P<value>[^'"]+)['"]"""),
    re.compile(r"""\bfetch\s*\(\s*['"`](?P<value>[^'"`]+)['"`]"""),
    re.compile(r"""\bnew\s+WebSocket\s*\(\s*['"`](?P<value>[^'"`]+)['"`]"""),
    re.compile(r"""\bsendBeacon\s*\(\s*['"`](?P<value>[^'"`]+)['"`]"""),
    re.compile(r"""\bopen\s*\(\s*['"](?:GET|POST|PUT|DELETE)['"]\s*,\s*['"](?P<value>[^'"]+)['"]"""),
    # 代入形式（例: new Image().src = 外部URL / link.href = 外部URL）
    re.compile(r"""\.(?:src|href|srcset|poster)\s*=\s*['"`](?P<value>[^'"`]+)['"`]"""),
    # setAttribute 形式
    re.compile(
        r"""setAttribute\(\s*['"](?:src|href|srcset|poster)['"]\s*,\s*['"](?P<value>[^'"]+)['"]"""
    ),
)
# srcset は「URL 記述子, URL 記述子」の並びなので、カンマ区切りの各候補を個別に検査する
SRCSET_ATTRS = ("srcset", "imagesrcset", "data-srcset")
LOADING_ATTRS = ("src", "href", "data", "poster", "xlink:href", "data-src", "data-background")
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\((?P<value>[^)\s]+)\)")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((?P<value>[^)\s]+)\)")
BARE_URL_RE = re.compile(r"https?://[^\s)>\]\"']+")

SCAN_SUFFIXES = (".html", ".css", ".js", ".md", ".json", ".py")
LOADING_LINK_RELS = (
    "stylesheet",
    "icon",
    "preload",
    "prefetch",
    "preconnect",
    "dns-prefetch",
    "modulepreload",
    "manifest",
    "apple-touch-icon",
)


def scan(path: str, rel: str):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    loads = []
    citations = []

    for tag_match in TAG_RE.finditer(text):
        tag = tag_match.group("tag").lower()
        attrs = {match.group("name").lower(): match.group("value") for match in ATTR_RE.finditer(tag_match.group(0))}
        if tag == "link":
            rel_value = attrs.get("rel", "").lower()
            if not any(keyword in rel_value for keyword in LOADING_LINK_RELS):
                continue
        if tag == "form":
            continue
        for name in LOADING_ATTRS:
            value = attrs.get(name)
            if value and EXTERNAL_RE.match(value.strip()):
                loads.append((rel, f"<{tag} {name}=\"{value[:80]}\">"))
        for name in SRCSET_ATTRS:
            value = attrs.get(name)
            if not value:
                continue
            for candidate in value.split(","):
                url = candidate.strip().split(" ")[0].strip()
                if url and EXTERNAL_RE.match(url):
                    loads.append((rel, f"<{tag} {name}=\"{url[:80]}\">"))

    for match in CSS_URL_RE.finditer(text):
        if EXTERNAL_RE.match(match.group("value").strip()):
            loads.append((rel, f"url({match.group('value')[:80]})"))
    for match in CSS_IMPORT_RE.finditer(text):
        value = match.group("value") or match.group(0)
        if EXTERNAL_RE.match(value.strip()):
            loads.append((rel, f"@import {value[:80]}"))
    for pattern in JS_PATTERNS:
        for match in pattern.finditer(text):
            if EXTERNAL_RE.match(match.group("value").strip()):
                loads.append((rel, f"JS: {match.group(0)[:80]}"))
    for match in MARKDOWN_IMAGE_RE.finditer(text):
        if EXTERNAL_RE.match(match.group("value").strip()):
            loads.append((rel, f"Markdown画像: {match.group('value')[:80]}"))

    for match in MARKDOWN_LINK_RE.finditer(text):
        if EXTERNAL_RE.match(match.group("value").strip()):
            citations.append(match.group("value")[:100])
    for match in BARE_URL_RE.finditer(text):
        citations.append(match.group(0)[:100])
    return loads, citations


def collect_files(root: str) -> list:
    files = []
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"}]
        for name in sorted(names):
            if name.endswith(SCAN_SUFFIXES):
                files.append(os.path.join(base, name))
    return files


def main() -> int:
    root = catalog_lib.skill_root()
    repo_root = os.path.dirname(root)
    all_loads = []
    citation_count = 0
    scanned = 0
    for path in collect_files(root):
        rel = os.path.relpath(path, repo_root)
        loads, citations = scan(path, rel)
        all_loads.extend(loads)
        citation_count += len(citations)
        scanned += 1

    readme = os.path.join(repo_root, "README.md")
    if os.path.isfile(readme):
        loads, _ = scan(readme, "README.md")
        all_loads.extend(loads)
        scanned += 1

    print(f"外部依存チェック: {scanned} ファイルを走査")
    print(f"- 出典・参考リンク（許容）: {citation_count} 件")
    if all_loads:
        print("\n外部ネットワーク読み込みを検出しました:", file=sys.stderr)
        for rel, detail in all_loads:
            print(f"NG: {rel}: {detail}", file=sys.stderr)
        return 1
    print("OK: 外部CDN・外部フォント・外部画像・外部APIの読み込みなし（オフライン動作）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
