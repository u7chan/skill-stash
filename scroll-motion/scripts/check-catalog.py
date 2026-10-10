#!/usr/bin/env python3
"""カタログ整合性チェック。

- ID 01–24 が連番で揃い、名称が Issue #42 の固定リストと一致する
- 各演出に概要・使用技術・CSS版 / Tailwind版のパスがある
- 欠落・重複・未知 ID のサンプルファイルが無い
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import catalog_lib  # noqa: E402

# Issue #42 で固定された 24 演出（ID順）
EXPECTED_NAMES = {
    "01": "フェードイン",
    "02": "スライドイン",
    "03": "スタッガー",
    "04": "テキストリビール",
    "05": "マスクリビール",
    "06": "ブラーイン",
    "07": "タイプライター",
    "08": "カウントアップ",
    "09": "スクロール連動",
    "10": "パララックス",
    "11": "スクロールズーム",
    "12": "画像シーケンス",
    "13": "SVGラインドロー",
    "14": "テキストフィル",
    "15": "背景色トランジション",
    "16": "マーキー（スクロール速度連動）",
    "17": "スティッキー",
    "18": "ピン留め＋スクラブ",
    "19": "スクロールテリング",
    "20": "カードスタック",
    "21": "スクロールスナップ",
    "22": "横スクロール",
    "23": "隠れるヘッダー",
    "24": "スクロールスパイ",
}

EXPECTED_CATEGORY_RANGES = {"enter": ("01", "08"), "progress": ("09", "16"), "pin": ("17", "24")}


def main() -> int:
    root = catalog_lib.skill_root()
    catalog = catalog_lib.load_catalog(root)
    errors = list(catalog_lib.validate(catalog, root))
    effects = catalog_lib.sorted_effects(catalog)

    for effect in effects:
        expected = EXPECTED_NAMES.get(effect["id"])
        if expected is None:
            errors.append(f"演出 {effect['id']} は Issue #42 の ID 一覧にありません")
        elif effect["name"] != expected:
            errors.append(f"演出 {effect['id']} の名称が Issue と不一致: {effect['name']!r} != {expected!r}")
        css = os.path.join(root, effect["cssPath"])
        tailwind = os.path.join(root, effect["tailwindPath"])
        for label, path in (("CSS版", css), ("Tailwind版", tailwind)):
            if not os.path.isfile(path):
                errors.append(f"演出 {effect['id']} の {label} サンプルがありません: {os.path.relpath(path, root)}")
        for field in ("cssPath", "tailwindPath"):
            if not effect.get(field, "").startswith("examples/"):
                errors.append(f"演出 {effect['id']} の {field} が examples/ 配下ではありません: {effect.get(field)!r}")

    for category_id, (first, last) in EXPECTED_CATEGORY_RANGES.items():
        ids = [effect["id"] for effect in effects if effect["category"] == category_id]
        if not ids:
            errors.append(f"カテゴリ {category_id} に演出がありません")
        elif (ids[0], ids[-1]) != (first, last):
            errors.append(f"カテゴリ {category_id} の ID 範囲が {first}–{last} ではありません: {ids[0]}–{ids[-1]}")

    print(f"カタログ: {len(effects)} 演出（ID 01–{effects[-1]['id']}）")
    for category in catalog["categories"]:
        names = [f"{e['id']} {e['name']}" for e in effects if e["category"] == category["id"]]
        print(f"- {category['name']}: {len(names)} 件")
        print("  " + ", ".join(names))
    print(f"CSS版サンプル: {len(effects)} / Tailwind版サンプル: {len(effects)}")

    if errors:
        print("\nカタログ整合性チェックに失敗しました:", file=sys.stderr)
        for error in errors:
            print(f"NG: {error}", file=sys.stderr)
        return 1
    print("\nOK: カタログ整合性チェックに成功（欠落・重複・未知IDなし）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
