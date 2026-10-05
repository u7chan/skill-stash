#!/usr/bin/env python3
"""DADS 準拠の HTML を機械的に検査する（ヒューリスティック）。

完璧な検証ではなく、作り込みで抜けやすい観点を落とすための補助。
ERROR は修正必須、WARN は意図的な逸脱かどうかを人が判断する。

使い方:
    python3 scripts/check-page.py page.html
    python3 scripts/check-page.py page.html --json
    python3 scripts/check-page.py page.html --quiet   # ERROR のみ表示

終了コード: ERROR があれば 1、なければ 0。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

MIN_FONT_PX = 14
MIN_TARGET_PX = 44

TOKEN_CSS = ("dads-tokens.css", "dads-global.css")

REQUIRED_TOKEN_HINT = re.compile(r"--(color|font|elevation|border-radius)-")


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.attrs_by_tag: list[tuple[str, dict[str, str]]] = []
        self.headings: list[tuple[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.svgs: list[dict[str, str]] = []
        self.label_for: set[str] = set()
        self.ids: list[str] = []
        self.text_chunks: list[str] = []
        self._heading_tag: str | None = None
        self._heading_text: list[str] = []
        self._in_title = False
        self.title = ""
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        items = {k: (v if v is not None else "") for k, v in attrs}
        self.attrs_by_tag.append((tag, items))
        if "id" in items:
            self.ids.append(items["id"])
        if tag == "img":
            self.images.append(items)
        if tag == "svg":
            self.svgs.append(items)
            self._skip_depth = 1  # svg 内部の title/path は本文ではない
        elif self._skip_depth:
            self._skip_depth += 1
        if tag == "label" and "for" in items:
            self.label_for.add(items["for"])
        if re.fullmatch(r"h[1-6]", tag):
            self._heading_tag = tag
            self._heading_text = []
        if tag == "title":
            self._in_title = True

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == "svg":
            self._skip_depth = 0

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "svg" and self._skip_depth:
            self._skip_depth = 0
        elif self._skip_depth:
            self._skip_depth -= 1
        if self._heading_tag == tag:
            self.headings.append((tag, "".join(self._heading_text).strip()))
            self._heading_tag = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        if self._heading_tag:
            self._heading_text.append(data)
        if not self._skip_depth:
            self.text_chunks.append(data)


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def collect_css(html: str) -> str:
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S | re.I)
    return strip_comments("\n".join(blocks))


def check(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    html = path.read_text(encoding="utf-8")

    parser = Collector()
    parser.feed(html)
    attrs = parser.attrs_by_tag
    tags = [t for t, _ in attrs]
    root = next((a for t, a in attrs if t == "html"), {})
    css = collect_css(html)

    # --- 文書の基本 ---------------------------------------------------------
    if not root.get("lang"):
        errors.append("<html> に lang 属性がない（例: lang=\"ja\"）")
    elif root["lang"].lower().startswith("ja") and root["lang"] not in {"ja", "ja-JP"}:
        warnings.append(f"lang=\"{root['lang']}\" は表記ゆれの可能性がある（例: ja）")
    if not any(t == "meta" and a.get("charset") for t, a in attrs):
        warnings.append("<meta charset> がない")
    if not any(
        t == "meta" and a.get("name", "").lower() == "viewport" for t, a in attrs
    ):
        errors.append("viewport meta がない（モバイルで拡大縮小できない）")
    if not parser.title.strip():
        warnings.append("<title> がない、または空")

    # --- アセットの読み込み -------------------------------------------------
    linked = " ".join(
        a.get("href", "") for t, a in attrs if t == "link"
    )
    for name in TOKEN_CSS:
        if name not in linked and name not in html:
            errors.append(f"{name} が読み込まれていない（DADS のトークン/共通スタイル）")

    # --- 見出し構造 ---------------------------------------------------------
    h1s = [t for t, _ in parser.headings if t == "h1"]
    if len(h1s) == 0:
        warnings.append("<h1> がない（ページの主題を示す見出しが必要）")
    elif len(h1s) > 1:
        errors.append(f"<h1> が {len(h1s)} 個ある（1 ページ 1 つ）")
    levels = [int(t[1]) for t, _ in parser.headings]
    for prev, cur in zip(levels, levels[1:]):
        if cur > prev + 1:
            warnings.append(f"見出しレベルが飛んでいる: h{prev} -> h{cur}")

    # --- ランドマーク -------------------------------------------------------
    for landmark, selector in (("main", "main"), ("header", "header"), ("footer", "footer")):
        if landmark not in tags:
            warnings.append(f"<{landmark}> がない（{selector} ランドマーク）")

    # --- 画像・アイコン -----------------------------------------------------
    for img in parser.images:
        if "alt" not in img:
            errors.append(f"<img src=\"{img.get('src', '?')}\"> に alt がない（装飾なら alt=\"\"）")
    for svg in parser.svgs:
        if "aria-hidden" not in svg and "role" not in svg and "aria-label" not in svg:
            warnings.append(
                "インライン <svg> に aria-hidden=\"true\" か role/aria-label がない（"
                "ラベル併記のアイコンは aria-hidden=\"true\"、単体利用は role=\"img\" + aria-label）"
            )

    # --- フォーム -----------------------------------------------------------
    for tag, a in attrs:
        if tag in {"input", "select", "textarea"}:
            if a.get("type") in {"hidden", "submit", "button", "reset", "image"}:
                continue
            wired = bool(a.get("id") and a["id"] in parser.label_for)
            if not wired and not (a.get("aria-label") or a.get("aria-labelledby")):
                errors.append(
                    f"<{tag} name=\"{a.get('name', '?')}\"> にラベルがない"
                    "（<label for> か aria-label を付ける）"
                )
    # --- インタラクション ---------------------------------------------------
    for tag, a in attrs:
        if tag not in {"a", "button", "input", "select", "textarea", "summary", "label", "form"} and (
            "onclick" in a or a.get("role") in {"button", "link", "tab", "checkbox", "radio"}
        ):
            errors.append(
                f"<{tag}> で操作を実装している（<button> または <a> を使う）"
            )
    if "onsubmit" in html and "preventDefault" not in html:
        warnings.append("onsubmit があるが preventDefault が見当たらない（ネイティブ送信で遷移する）")

    # --- フォーカス可視化 ---------------------------------------------------
    if "outline: none" in css or "outline:none" in css:
        if "focus-visible" not in css:
            errors.append("outline: none が指定され、代替のフォーカス表示がない")
        else:
            warnings.append("outline: none がある。:focus-visible の代替表示を確認する")
    if "focus-visible" not in css and "dads-u-focus" not in css and "focus-visible" not in html:
        errors.append(":focus-visible のフォーカスインジケーターが見当たらない（DADS は必須）")

    # --- スキップリンク -----------------------------------------------------
    if "main" in tags and not re.search(r"href=\"#(main|content|main-content)\"", html):
        warnings.append("スキップリンク（本文へ移動）がない")

    # --- トークン利用 -------------------------------------------------------
    hex_colors = set(re.findall(r"#[0-9a-fA-F]{3,8}\b", css))
    allowed_hex = {"#ffffff", "#fff", "#000000", "#000"}
    stray = {c for c in hex_colors if c.lower() not in allowed_hex}
    if stray:
        warnings.append(
            "CSS にハードコードされた色がある（トークン var(--color-*) を使う）: "
            + ", ".join(sorted(stray)[:8])
        )
    if css and not REQUIRED_TOKEN_HINT.search(css):
        warnings.append("CSS で DADS のデザイントークン（var(--...)）が使われていない")

    font_sizes = [float(m) for m in re.findall(r"font-size:\s*([0-9.]+)px", css)]
    too_small = sorted({s for s in font_sizes if s < MIN_FONT_PX})
    if too_small:
        errors.append(f"14 CSS px 未満のフォントサイズがある: {', '.join(f'{s}px' for s in too_small)}")

    # --- ターゲットサイズ ---------------------------------------------------
    if re.search(r"width:\s*([1-3][0-9])px", css) and "min-height" not in css:
        warnings.append(
            f"小さい固定幅の指定がある。操作要素なら {MIN_TARGET_PX}x{MIN_TARGET_PX} CSS px 以上を確保する"
        )

    # --- DADS コンポーネントクラスの利用 ------------------------------------
    if css and "dads-" not in html:
        warnings.append("DADS のコンポーネントクラス（dads-*）が使われていない")

    if not parser.text_chunks or not "".join(parser.text_chunks).strip():
        warnings.append("本文テキストが空")

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=Path, help="検査する HTML ファイル")
    ap.add_argument("--json", action="store_true", help="結果を JSON で出力する")
    ap.add_argument("--quiet", action="store_true", help="ERROR のみ表示する")
    args = ap.parse_args()

    if not args.html.exists():
        sys.exit(f"[fail] not found: {args.html}")

    errors, warnings = check(args.html)

    if args.json:
        print(json.dumps({"file": str(args.html), "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        print(f"# {args.html}")
        if not errors and not warnings:
            print("PASS: ERROR/WARN なし")
        for e in errors:
            print(f"ERROR: {e}")
        if not args.quiet:
            for w in warnings:
                print(f"WARN : {w}")
        print(f"\nERROR {len(errors)} / WARN {len(warnings)}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
