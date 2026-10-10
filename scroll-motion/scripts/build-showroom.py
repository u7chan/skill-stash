#!/usr/bin/env python3
"""showroom/index.html と references/catalog.md を catalog.json + examples/ から生成する。

- 正本: scroll-motion/catalog.json（メタデータ）と scroll-motion/examples/**（実装サンプル）
- 生成物: scroll-motion/showroom/index.html, scroll-motion/references/catalog.md
- コードは examples/ のファイル内容をそのまま埋め込むため、ショールーム専用の重複実装は持たない。

使い方:
  python3 scripts/build-showroom.py           # 生成（生成物を上書き）
  python3 scripts/build-showroom.py --check    # 生成物と正本の一致を検証（差分があれば exit 1）

python3 標準ライブラリのみで動作する。
"""

from __future__ import annotations

import argparse
import difflib
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import catalog_lib  # noqa: E402

SHORT_TECH = {
    "CSS": "CSSのみ",
    "IO": "IntersectionObserver",
    "JS": "素のJS",
    "scroll-timeline": "CSS Scroll-driven",
}
LANG_LABELS = {"css": "CSS版", "tailwind": "Tailwind版"}


def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def relative_links(value: str) -> str:
    return value


def render_markdown(catalog: dict) -> str:
    categories = catalog_lib.category_map(catalog)
    effects = catalog_lib.sorted_effects(catalog)
    lines: list[str] = []
    lines.append(f"# {catalog['title']}")
    lines.append("")
    lines.append(
        "> このファイルは `catalog.json` から `scripts/build-showroom.py` が生成します。"
        "手で編集せず、`catalog.json` を変更して再生成してください"
        "（`python3 scripts/build-showroom.py --check` で差分を検出できます）。"
    )
    lines.append("")
    lines.append(f"- 演出数: {len(effects)}")
    lines.append("- 実装サンプル: `examples/css/`（HTML/CSS をそのまま使う版）/ `examples/tailwind/`（Tailwind CSS 導入済みプロジェクト向け）")
    lines.append("- ショールーム: [`../showroom/index.html`](../showroom/index.html)")
    lines.append("")
    lines.append("## カテゴリ")
    lines.append("")
    lines.append("| カテゴリ | ID範囲 | 概要 |")
    lines.append("| --- | --- | --- |")
    for category in catalog["categories"]:
        ids = [effect["id"] for effect in effects if effect["category"] == category["id"]]
        span = f"{ids[0]}–{ids[-1]}" if ids else "—"
        lines.append(f"| {category['name']} | {span} | {category['summary']} |")
    lines.append("")
    lines.append("## 一覧")
    lines.append("")
    lines.append("| ID | 演出 | カテゴリ | 使用技術 | CSS版 | Tailwind版 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for effect in effects:
        tech = " + ".join(SHORT_TECH.get(token, token) for token in effect["tech"])
        lines.append(
            f"| {effect['id']} | [{effect['name']}](#{catalog_lib.effect_anchor(effect)}) "
            f"| {categories[effect['category']]['name']} | {tech} "
            f"| [`{os.path.basename(effect['cssPath'])}`](../{effect['cssPath']}) "
            f"| [`{os.path.basename(effect['tailwindPath'])}`](../{effect['tailwindPath']}) |"
        )
    lines.append("")
    lines.append("## 演出の詳細")
    lines.append("")
    for effect in effects:
        anchor = catalog_lib.effect_anchor(effect)
        lines.append(f'<a id="{anchor}"></a>')
        lines.append("")
        lines.append(f"### {effect['id']} {effect['name']}")
        lines.append("")
        lines.append(f"- スラッグ: `{effect['slug']}`")
        lines.append(f"- カテゴリ: {categories[effect['category']]['name']}")
        lines.append(f"- 概要: {effect['summary']}")
        lines.append(f"- 向いている用途: {' / '.join(effect['useCases'])}")
        lines.append(f"- 検索キーワード: {', '.join(effect['keywords'])}")
        lines.append(
            "- 使用技術: "
            + " / ".join(catalog_lib.tech_label(catalog, token) for token in effect["tech"])
        )
        if effect["optionalLibs"]:
            lines.append("- 任意ライブラリ: " + " / ".join(effect["optionalLibs"]))
        else:
            lines.append("- 任意ライブラリ: 不要（標準APIとCSSのみ）")
        lines.append("- 実装の要点:")
        for point in effect["keyPoints"]:
            lines.append(f"  - {point}")
        lines.append("- ブラウザ制約:")
        for note in effect["browserNotes"]:
            lines.append(f"  - {note}")
        lines.append(f"- `prefers-reduced-motion`: {effect['reducedMotion']}")
        lines.append("- アクセシビリティ:")
        for note in effect["a11yNotes"]:
            lines.append(f"  - {note}")
        lines.append(
            f"- サンプル: [CSS版](../{effect['cssPath']}) / [Tailwind版](../{effect['tailwindPath']})"
        )
        lines.append(
            f"- ショールーム: [カードを開く](../showroom/index.html#effect-{effect['id']})"
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def tech_chips(catalog: dict, effect: dict) -> str:
    chips = []
    for token in effect["tech"]:
        glossary = catalog_lib.tech_label(catalog, token)
        chips.append(
            f'<li class="chip" title="{html.escape(glossary, quote=True)}">'
            f'{html.escape(SHORT_TECH.get(token, token))}</li>'
        )
    if effect["optionalLibs"]:
        chips.append(
            '<li class="chip chip--optional">任意: '
            + html.escape(" / ".join(effect["optionalLibs"]))
            + "</li>"
        )
    else:
        chips.append('<li class="chip chip--none">任意ライブラリ不要</li>')
    return "\n          ".join(chips)


def list_items(values) -> str:
    return "".join(f"<li>{html.escape(value)}</li>" for value in values)


def render_card(catalog: dict, effect: dict, categories: dict, css_code: str, tailwind_code: str) -> str:
    effect_id = effect["id"]
    anchor = f"effect-{effect_id}"
    css_path = "../" + effect["cssPath"]
    tailwind_path = "../" + effect["tailwindPath"]
    tech = ", ".join(SHORT_TECH.get(token, token) for token in effect["tech"])
    return f"""      <article class="card" id="{anchor}" data-effect="{effect_id}" data-current-lang="css"
        data-detail-css="{css_path}" data-detail-tailwind="{tailwind_path}" data-demo-src="{css_path}">
        <header class="card__header">
          <p class="card__eyebrow"><span class="card__id">{effect_id}</span> <span class="card__slug">{effect['slug']}</span></p>
          <h3 class="card__title">{html.escape(effect['name'])}</h3>
          <p class="card__summary">{html.escape(effect['summary'])}</p>
          <ul class="chips" aria-label="使用技術: {html.escape(tech, quote=True)}">
          {tech_chips(catalog, effect)}
          </ul>
        </header>
        <div class="card__demo">
          <div class="demo-toolbar">
            <p class="demo-label">ライブデモ（CSS版・カード内 iframe）</p>
            <div class="demo-actions">
              <button type="button" class="btn" data-action="rerun">再実行</button>
              <a class="btn btn--link" data-detail-link href="{css_path}" target="_blank" rel="noopener">詳細デモを開く</a>
            </div>
          </div>
          <iframe class="demo-frame demo-frame--{effect['demoHeight']}" data-demo-frame src="{css_path}"
            title="演出{effect_id} {html.escape(effect['name'], quote=True)} のライブデモ（CSS版）" loading="lazy"></iframe>
          <p class="demo-hint">{html.escape(effect['demoHint'])}</p>
        </div>
        <details class="code" data-code>
          <summary>コードを表示 <span class="code__current" data-lang-label>CSS版</span></summary>
          <div class="code__body">
            <div class="tabs" role="tablist" aria-label="演出{effect_id} のコード切替">
              <button type="button" role="tab" id="tab-{effect_id}-css" aria-controls="panel-{effect_id}-css" aria-selected="true" data-code-tab="css">CSS版</button>
              <button type="button" role="tab" id="tab-{effect_id}-tailwind" aria-controls="panel-{effect_id}-tailwind" aria-selected="false" tabindex="-1" data-code-tab="tailwind">Tailwind版</button>
              <button type="button" class="btn btn--copy" data-action="copy">このコードをコピー</button>
            </div>
            <p class="code__status" data-copy-status role="status" aria-live="polite"></p>
            <pre class="code__pre" id="panel-{effect_id}-css" role="tabpanel" aria-labelledby="tab-{effect_id}-css" data-code-panel="css" tabindex="0"><code>{html.escape(css_code)}</code></pre>
            <pre class="code__pre" id="panel-{effect_id}-tailwind" role="tabpanel" aria-labelledby="tab-{effect_id}-tailwind" data-code-panel="tailwind" tabindex="0" hidden><code>{html.escape(tailwind_code)}</code></pre>
            <p class="code__note">Tailwind版は呼び出し元プロジェクトに Tailwind CSS が導入済みである前提のサンプルです。このショールームは Tailwind ランタイムを読み込まないため、ライブデモは CSS版を表示し、切替はコード表示とコピーに限定しています。ファイル: <code>{effect['tailwindPath']}</code></p>
          </div>
        </details>
        <footer class="card__meta">
          <div class="meta-grid">
            <section>
              <h4>実装の要点</h4>
              <ul>{list_items(effect['keyPoints'])}</ul>
            </section>
            <section>
              <h4>ブラウザ制約</h4>
              <ul>{list_items(effect['browserNotes'])}</ul>
            </section>
            <section>
              <h4>prefers-reduced-motion</h4>
              <p>{html.escape(effect['reducedMotion'])}</p>
            </section>
            <section>
              <h4>アクセシビリティ</h4>
              <ul>{list_items(effect['a11yNotes'])}</ul>
            </section>
          </div>
          <p class="card__files">正本: <code>catalog.json</code> / <a href="{css_path}"><code>{effect['cssPath']}</code></a> / <a href="{tailwind_path}"><code>{effect['tailwindPath']}</code></a></p>
        </footer>
      </article>"""


def render_showroom(catalog: dict, root: str) -> str:
    categories = catalog_lib.category_map(catalog)
    effects = catalog_lib.sorted_effects(catalog)
    nav_items = "\n        ".join(
        f'<li><a href="#cat-{category["id"]}">{category["name"]} <span>{sum(1 for e in effects if e["category"] == category["id"])}</span></a></li>'
        for category in catalog["categories"]
    )
    sections = []
    for category in catalog["categories"]:
        cards = []
        for effect in effects:
            if effect["category"] != category["id"]:
                continue
            css_code = read_text(os.path.join(root, effect["cssPath"]))
            tailwind_code = read_text(os.path.join(root, effect["tailwindPath"]))
            cards.append(render_card(catalog, effect, categories, css_code, tailwind_code))
        sections.append(
            f"""    <section class="category" id="cat-{category['id']}" aria-labelledby="cat-{category['id']}-title">
      <header class="category__header">
        <h2 id="cat-{category['id']}-title">{category['name']}</h2>
        <p>{category['summary']}</p>
      </header>
{chr(10).join(cards)}
    </section>"""
        )
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>scroll-motion ショールーム | スクロール演出24種</title>
<link rel="stylesheet" href="showroom.css">
</head>
<body>
<a class="skip-link" href="#main">本文へスキップ</a>
<header class="site-header">
  <div class="site-header__inner">
    <p class="site-title">scroll-motion<span>ショールーム</span></p>
    <nav aria-label="カテゴリ">
      <ul>
        {nav_items}
      </ul>
    </nav>
  </div>
</header>
<main id="main">
  <section class="intro" aria-labelledby="intro-title">
    <h1 id="intro-title">スクロール演出24種のショールーム</h1>
    <p>演出を実際のスクロールで試し、CSS版 / Tailwind版のコードを確認してコピーできます。すべて静的ファイルで動作し、外部CDN・外部フォント・外部画像を読み込みません（オフライン可）。</p>
    <ul class="intro__notes">
      <li><strong>ライブデモは常にCSS版</strong>です。Tailwindランタイムを読み込まないため、CSS / Tailwind切替は<strong>コード表示の切替とコピー</strong>として実装しています。</li>
      <li>カード内のiframeをスクロールすると演出が再生されます。ピン留め・横スクロールなど長いスクロールが必要な演出は、カード内の十分な高さのデモか「詳細デモを開く」で確認してください。</li>
      <li>このページは <code>catalog.json</code> と <code>examples/</code> を正本として <code>scripts/build-showroom.py</code> が生成しています。手編集は <code>--check</code> で検出されます。</li>
    </ul>
    <p class="intro__links">正本: <a href="../catalog.json"><code>catalog.json</code></a> / <a href="../references/catalog.md">演出カタログ</a> / <a href="../references/implementation.md">実装ガイド</a> / <a href="../SKILL.md">SKILL.md</a> / 生成スクリプト: <code>scripts/build-showroom.py</code></p>
  </section>
{chr(10).join(sections)}
</main>
<script src="showroom.js"></script>
</body>
</html>
"""


def write_if_changed(path: str, content: str) -> bool:
    current = read_text(path) if os.path.isfile(path) else None
    if current == content:
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return True


def unified_diff(label: str, expected: str, actual: str) -> str:
    diff = difflib.unified_diff(
        actual.splitlines(),
        expected.splitlines(),
        fromfile=label + " (current)",
        tofile=label + " (regenerated)",
        lineterm="",
        n=2,
    )
    return "\n".join(diff)


def main() -> int:
    parser = argparse.ArgumentParser(description="showroom とカタログMarkdownを生成する")
    parser.add_argument("--check", action="store_true", help="生成物が正本と一致するか検証する")
    args = parser.parse_args()

    root = catalog_lib.skill_root()
    catalog = catalog_lib.load_catalog(root)
    errors = catalog_lib.validate(catalog, root)
    if errors:
        print("catalog.json の検証に失敗しました:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    targets = {
        os.path.join(root, "showroom", "index.html"): render_showroom(catalog, root),
        os.path.join(root, "references", "catalog.md"): render_markdown(catalog),
    }

    if args.check:
        failed = False
        for path, content in targets.items():
            label = os.path.relpath(path, root)
            if not os.path.isfile(path):
                print(f"NG: {label} が存在しません（python3 scripts/build-showroom.py で生成してください）")
                failed = True
                continue
            current = read_text(path)
            if current != content:
                print(f"NG: {label} が正本と一致しません。python3 scripts/build-showroom.py で再生成してください")
                print(unified_diff(label, content, current))
                failed = True
            else:
                print(f"OK: {label} は正本から再生成した内容と一致")
        if failed:
            return 1
        print("showroom / catalog.md の再生成チェックが成功しました")
        return 0

    changed = [os.path.relpath(path, root) for path, content in targets.items() if write_if_changed(path, content)]
    if changed:
        for label in changed:
            print(f"generated: {label}")
    else:
        print("生成物に変更はありません")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
