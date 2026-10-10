#!/usr/bin/env python3
"""ショールームのフック（コード切替・コピー・再実行・詳細デモ）と単一正本性を検証する。

- 24 演出すべてにカード・タブ・コードパネル・コピー・再実行・詳細デモのフックがある
- showroom.js がそれらのフックを実装している
- カードに埋め込まれたコードが examples/ のファイル内容そのもの（正本と一致・重複実装なし）
"""

from __future__ import annotations

import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import catalog_lib  # noqa: E402

REQUIRED_JS_TOKENS = (
    "code-tab",
    '"copy"',
    '"rerun"',
    "navigator.clipboard",
    "execCommand",
    "aria-selected",
    "data-code-panel",
    "cloneNode",
    "currentLang",
    "tabIndex",
)
# 詳細デモのリンクは CSS 版に固定する（JS で href を差し替えないこと）
FORBIDDEN_JS_TOKENS = ("detailTailwind", "dataset.detailCss", "setAttribute('href'")
REQUIRED_HTML_TOKENS = (
    'role="status"',
    'role="tab"',
    'role="tabpanel"',
    "skip-link",
    "loading=\"lazy\"",
)


def main() -> int:
    root = catalog_lib.skill_root()
    catalog = catalog_lib.load_catalog(root)
    effects = catalog_lib.sorted_effects(catalog)
    index_path = os.path.join(root, "showroom", "index.html")
    js_path = os.path.join(root, "showroom", "showroom.js")
    css_path = os.path.join(root, "showroom", "showroom.css")
    errors = []

    if not os.path.isfile(index_path):
        print("NG: showroom/index.html がありません（python3 scripts/build-showroom.py を実行してください）", file=sys.stderr)
        return 1
    with open(index_path, encoding="utf-8") as fh:
        index = fh.read()
    with open(js_path, encoding="utf-8") as fh:
        js = fh.read()
    with open(css_path, encoding="utf-8") as fh:
        css = fh.read()

    multi_check = {
        'data-code-tab="css"': len(effects),
        'data-code-tab="tailwind"': len(effects),
        'data-code-panel="css"': len(effects),
        'data-code-panel="tailwind"': len(effects),
        'data-action="copy"': len(effects),
        'data-action="rerun"': len(effects),
        "data-detail-link": len(effects),
        "data-demo-frame": len(effects),
        'aria-live="polite"': len(effects),
    }
    for token, expected in multi_check.items():
        found = index.count(token)
        if found != expected:
            errors.append(f"showroom/index.html: {token} が {expected} 件あるべきところ {found} 件")

    for effect in effects:
        effect_id = effect["id"]
        anchor = f'id="effect-{effect_id}"'
        if index.count(anchor) != 1:
            errors.append(f"showroom/index.html: カード {anchor} が 1 件ではありません")
        if index.count(f'data-effect="{effect_id}"') != 1:
            errors.append(f"showroom/index.html: 演出 {effect_id} の data-effect が 1 件ではありません")
        for expected in (
            f'src="../{effect["cssPath"]}"',
            f'<a class="btn btn--link" data-detail-link href="../{effect["cssPath"]}" target="_blank" rel="noopener">詳細デモを開く（CSS版）</a>',
        ):
            # data-demo-src などの部分一致を避けて、属性としての出現だけを数える
            found = len(re.findall(r"(?<![\w-])" + re.escape(expected), index))
            if found != 1:
                errors.append(f"showroom/index.html: 演出 {effect_id} の {expected} が 1 件ではありません（{found} 件）")
        for panel in ("css", "tailwind"):
            if index.count(f'aria-controls="panel-{effect_id}-{panel}"') != 1:
                errors.append(f"showroom/index.html: 演出 {effect_id} の aria-controls（{panel}）が 1 件ではありません")
            if index.count(f'id="panel-{effect_id}-{panel}"') != 1:
                errors.append(f"showroom/index.html: 演出 {effect_id} のコードパネル id（{panel}）が 1 件ではありません")
        if index.count(f'title="演出{effect_id} ') != 1 or "のライブデモ（CSS版）" not in index:
            errors.append(f"showroom/index.html: 演出 {effect_id} の iframe に title がありません")
        for variant, field in (("css", "cssPath"), ("tailwind", "tailwindPath")):
            path = os.path.join(root, effect[field])
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            escaped = html.escape(content)
            count = index.count(escaped)
            if count != 1:
                errors.append(
                    f"showroom/index.html: 演出 {effect_id} の {variant} コードが examples/{variant} の内容と一致しない/重複しています（{count} 件）"
                )

    for token in REQUIRED_JS_TOKENS:
        if token not in js:
            errors.append(f"showroom/showroom.js: フック {token} の実装が見つかりません")
    for token in FORBIDDEN_JS_TOKENS:
        if token in js:
            errors.append(f"showroom/showroom.js: 詳細デモのリンクは CSS 版に固定するため {token} は使わないでください")
    for token in ("data-detail-link", "tabIndex"):
        if token not in js:
            errors.append(f"showroom/showroom.js: {token} の扱いが見つかりません")

    for token in REQUIRED_HTML_TOKENS:
        if token not in index:
            errors.append(f"showroom/index.html: {token} が見つかりません")

    css_tokens = (".demo-frame--md", ".demo-frame--lg", "prefers-reduced-motion", "overflow-x")
    for token in css_tokens:
        if token not in css:
            errors.append(f"showroom/showroom.css: {token} の定義が見つかりません")
    if "role=\"tab\"" not in index:
        errors.append("showroom/index.html: タブに role=\"tab\" がありません")
    if 'role="tabpanel"' not in index:
        errors.append("showroom/index.html: コードパネルに role=\"tabpanel\" がありません")
    if index.count("Tailwind版はコード表示用のサンプル") != len(effects):
        errors.append("showroom/index.html: Tailwind 版がコード表示専用である旨の可視注記が全カードにありません")
    if "skip-link" not in index:
        errors.append("showroom/index.html: スキップリンクがありません")

    print(f"ショールームのフックチェック: {len(effects)} 演出分のタブ・コピー・再実行・詳細デモを確認")
    print(f"- 埋め込みコードが examples/ と一致した演出: {len(effects)} × 2 系統")
    if errors:
        print("\nフック・単一正本性チェックに失敗しました:", file=sys.stderr)
        for error in errors:
            print(f"NG: {error}", file=sys.stderr)
        return 1
    print("OK: コード切替・コピー・再実行・詳細デモのフックと単一正本性を確認")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
