#!/usr/bin/env python3
"""演出サンプルの prefers-reduced-motion 対応と JS 無効時のフォールバックを機械チェックする。

検証内容:
- 48 サンプルすべてが `prefers-reduced-motion` に言及している
- 非表示の初期状態（opacity: 0 / visibility: hidden / clip-path のマスク / blur）が
  reduce 時に残らない（no-preference でゲートするか、reduce 側で戻している）
- 無限アニメーション（infinite）が reduce でも動き続けない
- JS でアニメーションループ（requestAnimationFrame / setTimeout / setInterval）を使うサンプルは
  matchMedia('(prefers-reduced-motion: reduce)') を確認している
- CSS で内容を隠し JS で表示するサンプルは、JS 無効時にも読めるよう <noscript> のフォールバックを持つ
- CSS でクリップしたコンテナを JS の transform で移動するサンプル（横スクロール・マーキー等）も、
  JS 無効時に中身へ到達できるよう <noscript> のフォールバックを持つ
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import catalog_lib  # noqa: E402
import css_blocks  # noqa: E402
import doc_scan  # noqa: E402

HIDDEN_TOKENS = {
    "opacity: 0": ("opacity: 1", "opacity:1"),
    "visibility: hidden": ("visibility: visible", "visibility:visible"),
    "clip-path: inset(0 100%": ("clip-path: none", "clip-path: inset(0)"),
    "filter: blur(": ("filter: none", "filter: blur(0"),
}
LOOP_TOKENS = ("requestAnimationFrame", "setInterval", "setTimeout")
# JS 無効時に内容が隠れたままになる組み合わせを検出するためのトークン
HIDDEN_STATE_TOKENS = (
    "opacity: 0",
    "visibility: hidden",
    "display: none",
    "clip-path: inset(0 100% 0 0)",
    "clip-path: inset(100% 0 0 0)",
    "transform: translate3d(0, 110%, 0)",
    "filter: blur(",
)
JS_REVEAL_TOKENS = ("classList.add", "classList.toggle", "classList.remove", ".style.transform", ".style.opacity", "strokeDashoffset", "textContent")
# 「クリップしたコンテナを JS の transform で動かす」構成の目印。
# overflow: hidden の中身は、横スクロール・マーキーのように JS が動かす前提だとユーザー操作では到達できない。
CLIP_TOKENS = ("overflow: hidden", "overflow-x: hidden")
JS_TRANSFORM_TOKENS = ("will-change: transform",)
JS_TRANSFORM_WRITE = ".style.transform"
# @keyframes の中身は「アニメーションを適用したときだけ」効くので、非表示トークンの走査から外す
KEYFRAMES_RE = re.compile(r"@keyframes\s+[A-Za-z0-9_-]+", re.IGNORECASE)
ANIMATION_DECL_RE = re.compile(r"animation(?:-name)?\s*:\s*(?P<value>[^;}]+)")
SCRIPT_RE = re.compile(r"<script\b[^>]*>(?P<body>.*?)</script>", re.DOTALL | re.IGNORECASE)
STYLE_RE = re.compile(r"<style\b[^>]*>(?P<body>.*?)</style>", re.DOTALL | re.IGNORECASE)


def occurrences(text: str, needle: str) -> list:
    return [match.start() for match in re.finditer(re.escape(needle), text)]


def check_file(path: str, rel: str) -> list:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    errors = []
    # 実際に適用される CSS（<style> の中）だけを走査対象にする
    css = "\n".join(match.group("body") for match in STYLE_RE.finditer(text))
    css = doc_scan.mask_css_blocks(css, KEYFRAMES_RE)
    blocks = css_blocks.media_blocks(css)
    reduce_body = css_blocks.block_body(css, "prefers-reduced-motion: reduce")
    no_preference_body = css_blocks.block_body(css, "prefers-reduced-motion: no-preference")

    if "prefers-reduced-motion" not in text:
        errors.append(f"{rel}: prefers-reduced-motion の記述がありません")
        return errors
    if not reduce_body and not no_preference_body and "matchMedia" not in text:
        errors.append(f"{rel}: reduce / no-preference / matchMedia のいずれの対応もありません")

    for token, reset_candidates in HIDDEN_TOKENS.items():
        for position in occurrences(css, token):
            condition = css_blocks.innermost_condition(blocks, position)
            if condition and css_blocks.has_condition(condition, "prefers-reduced-motion: reduce"):
                errors.append(f"{rel}: reduce 側で非表示状態を指定しています: {token}")
            elif condition and css_blocks.has_condition(condition, "prefers-reduced-motion: no-preference"):
                continue  # reduce では適用されないので安全
            else:
                if not any(candidate in reduce_body for candidate in reset_candidates):
                    errors.append(
                        f"{rel}: グローバルな非表示状態 {token!r} が reduce 側で解除されていません"
                    )

    if "infinite" in css:
        gated = any(
            css_blocks.has_condition(css_blocks.innermost_condition(blocks, position) or "", "prefers-reduced-motion: no-preference")
            for position in occurrences(css, "infinite")
        )
        if not gated and not ("animation: none" in reduce_body or "animation-play-state: paused" in reduce_body):
            errors.append(f"{rel}: 無限アニメーションが reduce で停止しません（no-preference ゲートか animation: none が必要）")

    script_body = "\n".join(match.group("body") for match in SCRIPT_RE.finditer(text))

    # JS 無効時に内容が読めるか（CSS で隠して JS で表示する構成には <noscript> が必要）
    hides_content = any(token in css for token in HIDDEN_STATE_TOKENS)
    reveals_with_js = any(token in script_body for token in JS_REVEAL_TOKENS)
    if hides_content and reveals_with_js and "<noscript>" not in text:
        errors.append(
            f"{rel}: CSS で隠して JS で表示する構成なのに <noscript> のフォールバックがありません（JS 無効時に内容が読めません）"
        )

    # クリップしたコンテナを JS の transform で移動する構成（横スクロール・マーキー等）
    clips_container = any(token in css for token in CLIP_TOKENS)
    moves_with_js = any(token in css for token in JS_TRANSFORM_TOKENS) and JS_TRANSFORM_WRITE in script_body
    if clips_container and moves_with_js and "<noscript>" not in text:
        errors.append(
            f"{rel}: クリップしたコンテナを JS の transform で動かす構成なのに <noscript> のフォールバックがありません"
            "（JS 無効時に中身へ到達できません）"
        )
    if any(token in script_body for token in LOOP_TOKENS):
        if "matchMedia" not in text:
            errors.append(f"{rel}: JS のアニメーションループが matchMedia で reduce を確認していません")
        elif not re.search(r"matchMedia\(\s*['\"]\(prefers-reduced-motion:\s*reduce\)['\"]", text):
            errors.append(f"{rel}: matchMedia の引数が '(prefers-reduced-motion: reduce)' ではありません")
    return errors


def main() -> int:
    root = catalog_lib.skill_root()
    catalog = catalog_lib.load_catalog(root)
    errors = []
    checked = 0
    js_guarded = 0
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
            if "matchMedia" in text:
                js_guarded += 1
            errors.extend(check_file(path, rel))
    print(f"prefers-reduced-motion チェック: {checked} サンプル（JSで matchMedia を使うもの: {js_guarded}）")
    if errors:
        print("\nprefers-reduced-motion チェックに失敗しました:", file=sys.stderr)
        for error in errors:
            print(f"NG: {error}", file=sys.stderr)
        return 1
    print("OK: 全サンプルで reduce 時にも内容が読める状態を維持")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
