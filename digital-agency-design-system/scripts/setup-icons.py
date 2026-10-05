#!/usr/bin/env python3
"""デジタル庁デザインシステムの公式アイコン素材を取得して assets/icons/ へ展開する。

公式配布 ZIP（イラストレーション・アイコン素材）をダウンロードし、unzip して
SVG アイコンだけを取り出し、色を currentColor に正規化して配置する。

使い方:
    python3 scripts/setup-icons.py                    # SVG アイコンのみ
    python3 scripts/setup-icons.py --illustrations    # イラスト PNG も取得
    python3 scripts/setup-icons.py --from /tmp/designsystem-assets.zip
    python3 scripts/setup-icons.py --list             # 収録アイコン名を表示

ZIP はキャッシュ（既定: .cache/designsystem-assets.zip）に保持し、再実行時は
ダウンロードをスキップする。--refresh で再取得する。
"""

from __future__ import annotations

import argparse
import shutil
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ASSETS_URL = (
    "https://www.digital.go.jp/assets/contents/node/basic_page/"
    "field_ref_resources/bb5d3e3b-30be-4487-b4f0-b3191a1ef823/c7976118/"
    "designsystem-assets.zip"
)

SKILL_ROOT = Path(__file__).resolve().parent.parent
ICON_DIR = SKILL_ROOT / "assets" / "icons"
ILLUSTRATION_DIR = SKILL_ROOT / "assets" / "illustrations"
CACHE_DIR = SKILL_ROOT / ".cache"
CACHE_ZIP = CACHE_DIR / "designsystem-assets.zip"

ICON_PREFIX = "designsystem-assets/icon/svg/"
ILLUSTRATION_PREFIX = "designsystem-assets/illustration/png/"
LICENSE_PREFIX = "designsystem-assets/LICENSE.txt"

# 公式 SVG の描画色。currentColor に置き換えて CSS の color を継承させる。
OFFICIAL_INK = "#1A1A1C"


def download(dest: Path, refresh: bool) -> Path:
    if dest.exists() and not refresh:
        print(f"[skip] cached zip: {dest} ({dest.stat().st_size:,} bytes)")
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"[get ] {ASSETS_URL}")
    try:
        with urllib.request.urlopen(ASSETS_URL, timeout=120) as res, dest.open("wb") as fh:
            shutil.copyfileobj(res, fh)
    except urllib.error.URLError as exc:  # pragma: no cover - network failure path
        sys.exit(f"[fail] download failed: {exc}\n       hand-place the zip and rerun with --from <zip>")
    print(f"[ok  ] {dest} ({dest.stat().st_size:,} bytes)")
    return dest


def normalize_svg(text: str) -> str:
    text = text.replace(OFFICIAL_INK, "currentColor")
    # 24 固定の width/height は CSS で上書きできるよう削らないが、簡潔化のため付与しない場合も許容する
    return text


def iter_members(zip_path: Path):
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if name.startswith("__MACOSX/"):
                continue
            yield name


def extract(zip_path: Path, with_illustrations: bool) -> tuple[int, int]:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    icon_count = 0
    illustration_count = 0

    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if name.startswith("__MACOSX/"):
                continue

            if name.startswith(ICON_PREFIX) and name.endswith(".svg"):
                data = normalize_svg(zf.read(name).decode("utf-8"))
                (ICON_DIR / Path(name).name).write_text(data, encoding="utf-8")
                icon_count += 1
            elif name.startswith(LICENSE_PREFIX):
                (ICON_DIR.parent / "icons-LICENSE.txt").write_bytes(zf.read(name))
            elif with_illustrations and name.startswith(ILLUSTRATION_PREFIX) and name.endswith(".png"):
                ILLUSTRATION_DIR.mkdir(parents=True, exist_ok=True)
                (ILLUSTRATION_DIR / Path(name).name).write_bytes(zf.read(name))
                illustration_count += 1

    return icon_count, illustration_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from", dest="zip_path", type=Path, help="展開する designsystem-assets.zip のパス")
    parser.add_argument("--illustrations", action="store_true", help="イラストレーション PNG も展開する")
    parser.add_argument("--refresh", action="store_true", help="キャッシュ済み ZIP を無視して再ダウンロードする")
    parser.add_argument("--list", action="store_true", help="展開せずに収録アイコン名を一覧表示する")
    args = parser.parse_args()

    zip_path = args.zip_path if args.zip_path else CACHE_ZIP
    if args.zip_path:
        if not args.zip_path.exists():
            sys.exit(f"[fail] zip not found: {args.zip_path}")
    elif args.list and CACHE_ZIP.exists():
        pass
    else:
        zip_path = download(CACHE_ZIP, refresh=args.refresh)

    if args.list:
        names = sorted(
            Path(n).stem
            for n in iter_members(zip_path)
            if n.startswith(ICON_PREFIX) and n.endswith(".svg")
        )
        print(f"{len(names)} icons")
        for chunk in range(0, len(names), 6):
            print("  " + "  ".join(f"{n:<28}" for n in names[chunk : chunk + 6]).rstrip())
        return 0

    icons, illustrations = extract(zip_path, with_illustrations=args.illustrations)
    print(f"[ok  ] icons: {icons} -> {ICON_DIR.relative_to(SKILL_ROOT)}")
    if args.illustrations:
        print(f"[ok  ] illustrations: {illustrations} -> {ILLUSTRATION_DIR.relative_to(SKILL_ROOT)}")
    if icons == 0:
        sys.exit("[fail] no SVG icons found in the zip; check the archive structure")
    print("\n使い方: <img src=\"assets/icons/search_line.svg\" alt=\"\"> で参照する。")
    print("色を変えたい場合は <span style=\"color: var(--color-neutral-solid-gray-800)\"> で包むか、")
    print("SVG をインライン展開して fill=\"currentColor\" を継承させる。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
