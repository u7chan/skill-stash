#!/usr/bin/env python3
"""catalog.json の読み込みと検証（python3 標準ライブラリのみ）。

SKILL.md / references / showroom から参照される 24 演出の正本を扱う共通処理。
"""

from __future__ import annotations

import json
import os
import re

TECH_TOKENS = ("CSS", "IO", "JS", "scroll-timeline")
DEMO_HEIGHTS = ("md", "lg")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_EFFECT_FIELDS = (
    "id",
    "slug",
    "name",
    "category",
    "summary",
    "useCases",
    "keywords",
    "tech",
    "optionalLibs",
    "demoHeight",
    "demoHint",
    "keyPoints",
    "browserNotes",
    "reducedMotion",
    "a11yNotes",
    "cssPath",
    "tailwindPath",
)


def skill_root() -> str:
    """scroll-motion/ の絶対パス。"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def catalog_path(root: str | None = None) -> str:
    return os.path.join(root or skill_root(), "catalog.json")


def load_catalog(root: str | None = None) -> dict:
    with open(catalog_path(root), encoding="utf-8") as fh:
        return json.load(fh)


def effect_anchor(effect: dict) -> str:
    return f"{effect['id']}-{effect['slug']}"


def category_map(catalog: dict) -> dict:
    return {category["id"]: category for category in catalog["categories"]}


def tech_label(catalog: dict, token: str) -> str:
    return catalog.get("techGlossary", {}).get(token, token)


def sorted_effects(catalog: dict) -> list:
    return sorted(catalog["effects"], key=lambda effect: effect["id"])


def validate(catalog: dict, root: str | None = None) -> list:
    """問題点を文字列のリストで返す。空リストなら整合している。"""
    root = root or skill_root()
    errors: list[str] = []

    if catalog.get("schemaVersion") != 1:
        errors.append(f"schemaVersion は 1 である必要があります: {catalog.get('schemaVersion')!r}")
    for field in ("id", "title", "description"):
        if not str(catalog.get(field, "")).strip():
            errors.append(f"トップレベルの {field} が空です")

    categories = catalog.get("categories", [])
    if len(categories) != 3:
        errors.append(f"categories は 3 件である必要があります: {len(categories)} 件")
    category_ids = []
    for category in categories:
        for field in ("id", "name", "summary"):
            if not str(category.get(field, "")).strip():
                errors.append(f"category {category.get('id')!r} の {field} が空です")
        category_ids.append(category.get("id"))
    if len(set(category_ids)) != len(category_ids):
        errors.append("categories の id が重複しています")
    known_categories = set(category_ids)

    glossary = catalog.get("techGlossary", {})
    for token in TECH_TOKENS:
        if not str(glossary.get(token, "")).strip():
            errors.append(f"techGlossary に {token} の説明がありません")
    for token in glossary:
        if token not in TECH_TOKENS:
            errors.append(f"techGlossary に未知の技術トークンがあります: {token}")

    effects = sorted_effects(catalog)
    expected_ids = [f"{index:02d}" for index in range(1, 25)]
    actual_ids = [effect.get("id") for effect in effects]
    if actual_ids != expected_ids:
        errors.append(f"演出 ID が 01–24 の連番になっていません: {actual_ids}")
    if len(set(actual_ids)) != len(actual_ids):
        errors.append("演出 ID が重複しています")

    seen_slugs: dict = {}
    seen_paths: dict = {}
    for effect in effects:
        prefix = f"演出 {effect.get('id')} ({effect.get('slug')})"
        for field in REQUIRED_EFFECT_FIELDS:
            if field not in effect:
                errors.append(f"{prefix}: 必須フィールド {field} がありません")
        slug = effect.get("slug", "")
        if not SLUG_RE.match(slug):
            errors.append(f"{prefix}: slug が kebab-case ではありません: {slug!r}")
        if slug in seen_slugs:
            errors.append(f"{prefix}: slug が {seen_slugs[slug]} と重複しています: {slug!r}")
        seen_slugs[slug] = effect.get("id")
        if effect.get("category") not in known_categories:
            errors.append(f"{prefix}: category が未知です: {effect.get('category')!r}")
        for field in ("name", "summary", "demoHint", "reducedMotion"):
            if not str(effect.get(field, "")).strip():
                errors.append(f"{prefix}: {field} が空です")
        for field in ("useCases", "keywords", "keyPoints", "browserNotes", "a11yNotes"):
            value = effect.get(field)
            if not isinstance(value, list) or not value:
                errors.append(f"{prefix}: {field} は 1 件以上の配列である必要があります")
        tech = effect.get("tech")
        if not isinstance(tech, list) or not tech:
            errors.append(f"{prefix}: tech は 1 件以上の配列である必要があります")
        else:
            for token in tech:
                if token not in TECH_TOKENS:
                    errors.append(f"{prefix}: tech に未知のトークンがあります: {token!r}")
            if len(set(tech)) != len(tech):
                errors.append(f"{prefix}: tech に重複があります: {tech}")
        if not isinstance(effect.get("optionalLibs"), list):
            errors.append(f"{prefix}: optionalLibs は配列である必要があります")
        if effect.get("demoHeight") not in DEMO_HEIGHTS:
            errors.append(f"{prefix}: demoHeight は {DEMO_HEIGHTS} のいずれかです: {effect.get('demoHeight')!r}")

        for field in ("cssPath", "tailwindPath"):
            rel = effect.get(field, "")
            expected_prefix = "examples/css/" if field == "cssPath" else "examples/tailwind/"
            expected_rel = f"{expected_prefix}{effect.get('id')}-{slug}.html"
            if rel != expected_rel:
                errors.append(f"{prefix}: {field} は {expected_rel} である必要があります: {rel!r}")
            else:
                absolute = os.path.join(root, rel)
                if not os.path.isfile(absolute):
                    errors.append(f"{prefix}: {field} のファイルが存在しません: {rel}")
            if rel in seen_paths:
                errors.append(f"{prefix}: {field} が {seen_paths[rel]} と重複しています: {rel!r}")
            seen_paths[rel] = effect.get("id")

    for variant in ("css", "tailwind"):
        directory = os.path.join(root, "examples", variant)
        if not os.path.isdir(directory):
            errors.append(f"examples/{variant}/ が存在しません")
            continue
        on_disk = sorted(name for name in os.listdir(directory) if name.endswith(".html"))
        expected = sorted(os.path.basename(effect[f"{variant}Path"]) for effect in effects)
        for name in sorted(set(on_disk) - set(expected)):
            errors.append(f"examples/{variant}/{name} はカタログに無い未知のサンプルです")
        for name in sorted(set(expected) - set(on_disk)):
            errors.append(f"examples/{variant}/{name} が存在しません")
    return errors
