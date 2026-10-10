#!/usr/bin/env python3
"""モバイル（375px 想定）での破綻を静的CSSから検出する。

Playwright の E2E は tester の担当なので、ここでは壊れやすい見た目を固定せず、
横溢れ・操作不能につながるパターンだけを機械的に禁止する。

- HTML に viewport meta（width=device-width）があること
- 100vw を使っていないこと（横スクロールバー分の溢れを避ける）
- 400px 以上の固定 width / min-width は @media (min-width: ...) の中だけに置くこと
- ショールーム CSS に狭い幅向けの @media (max-width: ...) があること

コードサンプル（<pre> 内）の CSS は実際には適用されないため走査対象から除外する。
"""

from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import catalog_lib  # noqa: E402
import css_blocks  # noqa: E402
import doc_scan  # noqa: E402

WIDTH_RE = re.compile(r"(?<!max-)(?<!min-)(width|min-width)\s*:\s*(?P<value>\d{3,})px", re.IGNORECASE)
FIXED_WIDTH_MIN = 400
MOBILE_QUERY_RE = re.compile(r"@media[^{]*\(\s*max-width\s*:", re.IGNORECASE)
MEDIA_PRELUDE_RE = re.compile(r"@media[^{]*\{", re.IGNORECASE)


def prelude_ranges(text: str) -> list:
    """@media の条件部分（開き波括弧まで）の範囲。ここに現れる min-width は宣言ではない。"""
    return [(match.start(), match.end()) for match in MEDIA_PRELUDE_RE.finditer(text)]


def in_ranges(position: int, ranges: list) -> bool:
    return any(start <= position < end for start, end in ranges)


def check_html(text: str, rel: str, require_viewport: bool) -> list:
    errors = []
    if require_viewport and not re.search(r'name="viewport"[^>]*width=device-width', text):
        errors.append(f"{rel}: viewport meta（width=device-width）がありません")
    masked = doc_scan.mask_html(text)
    if "100vw" in masked:
        errors.append(f"{rel}: 100vw を使っています（横溢れの原因）")
    return errors


def check_css(text: str, rel: str, require_mobile_query: bool) -> list:
    errors = []
    if require_mobile_query and not MOBILE_QUERY_RE.search(text):
        errors.append(f"{rel}: 狭い幅向けの @media (max-width: ...) がありません")
    if "100vw" in text:
        errors.append(f"{rel}: 100vw を使っています（横溢れの原因）")
    blocks = css_blocks.media_blocks(text)
    preludes = prelude_ranges(text)
    for match in WIDTH_RE.finditer(text):
        name, value = match.group(1), int(match.group("value"))
        if value < FIXED_WIDTH_MIN or in_ranges(match.start(), preludes):
            continue
        condition = css_blocks.innermost_condition(blocks, match.start())
        if condition is None or not css_blocks.has_condition(condition, "min-width"):
            errors.append(
                f"{rel}: {name}: {value}px が狭い幅でも適用されます（@media (min-width: ...) の中に置くか相対値にしてください）"
            )
    return errors


def main() -> int:
    root = catalog_lib.skill_root()
    catalog = catalog_lib.load_catalog(root)
    errors = []
    checked = 0
    for effect in catalog_lib.sorted_effects(catalog):
        for field in ("cssPath", "tailwindPath"):
            rel = effect[field]
            path = os.path.join(root, rel)
            if not os.path.isfile(path):
                errors.append(f"{rel}: ファイルがありません")
                continue
            checked += 1
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            errors.extend(check_html(text, rel, require_viewport=True))
            errors.extend(check_css(text, rel, require_mobile_query=False))

    for path in sorted(glob.glob(os.path.join(root, "examples", "_shared", "*.css"))):
        rel = os.path.relpath(path, root)
        with open(path, encoding="utf-8") as fh:
            errors.extend(check_css(fh.read(), rel, require_mobile_query=False))
        checked += 1

    showroom_html = os.path.join(root, "showroom", "index.html")
    showroom_css = os.path.join(root, "showroom", "showroom.css")
    if os.path.isfile(showroom_html):
        with open(showroom_html, encoding="utf-8") as fh:
            text = fh.read()
        errors.extend(check_html(text, "showroom/index.html", require_viewport=True))
        marked = doc_scan.mask_html(text)
        errors.extend(check_css(marked, "showroom/index.html", require_mobile_query=False))
        checked += 1
    else:
        errors.append("showroom/index.html: ファイルがありません")
    if os.path.isfile(showroom_css):
        with open(showroom_css, encoding="utf-8") as fh:
            errors.extend(check_css(fh.read(), "showroom/showroom.css", require_mobile_query=True))
        checked += 1
    else:
        errors.append("showroom/showroom.css: ファイルがありません")

    print(f"モバイル静的チェック: {checked} ファイル（しきい値: 固定幅 {FIXED_WIDTH_MIN}px 以上を禁止）")
    if errors:
        print("\nモバイル静的チェックに失敗しました:", file=sys.stderr)
        for error in errors:
            print(f"NG: {error}", file=sys.stderr)
        return 1
    print("OK: 375px 幅を想定した静的チェックを通過（横溢れパターンなし）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
