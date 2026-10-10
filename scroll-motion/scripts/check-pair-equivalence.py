#!/usr/bin/env python3
"""CSS版とTailwind版の挙動が同等であることを機械的に確認する。

見た目を固定するのではなく、「同じ演出を同じフックで実装しているか」を比較する。

- data-* フック（演出が依存する属性）の集合が一致する
- @keyframes 名の集合が一致する
- CSS カスタムプロパティ名の集合が一致する
- prefers-reduced-motion の扱い（no-preference / reduce / matchMedia）が一致する
- <script> ブロックの数が一致する
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import catalog_lib  # noqa: E402

DATA_ATTR_RE = re.compile(r"\s(data-[a-z0-9-]+)(?=[\s=/>])", re.IGNORECASE)
KEYFRAMES_RE = re.compile(r"@keyframes\s+([A-Za-z0-9_-]+)")
CUSTOM_PROP_RE = re.compile(r"(--[a-z0-9-]+)\s*:")
SCRIPT_RE = re.compile(r"<script\b[^>]*>", re.IGNORECASE)
STYLE_RE = re.compile(r"<style\b[^>]*>(?P<body>.*?)</style>", re.DOTALL | re.IGNORECASE)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
SELECTOR_RE = re.compile(r"querySelector(?:All)?\(\s*['\"](?P<selector>[^'\"]+)['\"]")
CLASS_SELECTOR_RE = re.compile(r"\.([A-Za-z][A-Za-z0-9_-]*)")
CLASS_ATTR_RE = re.compile(r"class\s*=\s*[\"'](?P<value>[^\"']*)[\"']")

# Tailwind 版ではレイアウト（グリッド・余白・タイポグラフィ）をユーティリティで組み、
# レイアウト専用クラスを持たない。演出の核ではないため差を許容する。
LAYOUT_ONLY_CLASSES = {
    "grid-2",
    "demo-list",
    "sticky-layout",
    "story",
    "story__steps",
    "story__caption",
    "spy",
}


def fingerprint(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    styles = "\n".join(match.group("body") for match in STYLE_RE.finditer(text))
    # <style> と HTML コメントを除いた本文から <script> を数える（コメント内の言及を拾わない）
    markup = COMMENT_RE.sub("", text)
    markup = STYLE_RE.sub("", markup)
    scripts = SCRIPT_RE.findall(markup)
    scripts_body = "\n".join(
        body for body in re.findall(r"<script\b[^>]*>(.*?)</script>", markup, re.DOTALL | re.IGNORECASE)
    )
    style_classes = set(CLASS_SELECTOR_RE.findall(styles))
    markup_classes = set()
    for match in CLASS_ATTR_RE.finditer(markup):
        markup_classes.update(match.group("value").split())
    return {
        "data": set(DATA_ATTR_RE.findall(text)),
        "classHooks": (style_classes & markup_classes) - LAYOUT_ONLY_CLASSES,
        "selectors": set(SELECTOR_RE.findall(scripts_body)),
        "keyframes": set(KEYFRAMES_RE.findall(styles)),
        "customProps": set(CUSTOM_PROP_RE.findall(styles)),
        "noPreference": "prefers-reduced-motion: no-preference" in text,
        "reduce": "prefers-reduced-motion: reduce" in text,
        "matchMedia": "matchMedia" in text,
        "scripts": len(scripts),
    }


def describe(value) -> str:
    if isinstance(value, set):
        return ", ".join(sorted(value)) if value else "(なし)"
    return str(value)


def main() -> int:
    root = catalog_lib.skill_root()
    catalog = catalog_lib.load_catalog(root)
    errors = []
    rows = []
    for effect in catalog_lib.sorted_effects(catalog):
        left = fingerprint(os.path.join(root, effect["cssPath"]))
        right = fingerprint(os.path.join(root, effect["tailwindPath"]))
        mismatches = []
        for key, label in (
            ("data", "data-* フック"),
            ("classHooks", "演出クラスのフック"),
            ("selectors", "JS が参照するセレクタ"),
            ("keyframes", "@keyframes"),
            ("customProps", "CSS カスタムプロパティ"),
            ("noPreference", "no-preference の有無"),
            ("reduce", "reduce の有無"),
            ("matchMedia", "matchMedia の有無"),
            ("scripts", "<script> の数"),
        ):
            if left[key] != right[key]:
                mismatches.append(f"{label}: CSS版=[{describe(left[key])}] Tailwind版=[{describe(right[key])}]")
        rows.append((effect["id"], effect["name"], mismatches))
        for mismatch in mismatches:
            errors.append(f"演出 {effect['id']} {effect['name']}: {mismatch}")
        if not left["data"] and not left["selectors"] and left["scripts"]:
            errors.append(f"演出 {effect['id']} {effect['name']}: 演出のフック（data-* 属性 / セレクタ）がありません")

    print(f"CSS版 / Tailwind版の同等性チェック: {len(rows)} 演出")
    for effect_id, name, mismatches in rows:
        state = "OK " if not mismatches else "NG "
        note = "" if not mismatches else " / ".join(mismatches)
        print(f"{state}{effect_id} {name}{('  ' + note) if note else ''}")
    if errors:
        print("\n同等性チェックに失敗しました:", file=sys.stderr)
        for error in errors:
            print(f"NG: {error}", file=sys.stderr)
        return 1
    print("OK: 全演出でフック・セレクタ・keyframes・reduce 対応が CSS版 / Tailwind版 で一致")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
