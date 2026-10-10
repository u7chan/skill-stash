#!/usr/bin/env python3
"""参照切れチェック。

SKILL.md / references/*.md / examples/*.html / showroom/* / README.md にある
相対参照（Markdown リンクと HTML の読み込み属性）が実在するか、
ページ内フラグメント（#anchor）が解決できるかを検証する。

コードサンプル内の文字列は読み込み参照ではないため、doc_scan がマスクして除外する。
"""

from __future__ import annotations

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import catalog_lib  # noqa: E402
import doc_scan  # noqa: E402

SCAN_SUFFIXES = (".md", ".html", ".css", ".js", ".json")


def collect_files(root: str) -> list:
    files = []
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"}]
        for name in sorted(names):
            if name.endswith(SCAN_SUFFIXES):
                files.append(os.path.join(base, name))
    repo_root = os.path.dirname(root)
    files.append(os.path.join(repo_root, "README.md"))
    return files


def main() -> int:
    root = catalog_lib.skill_root()
    repo_root = os.path.dirname(root)
    errors: list[str] = []
    checked = 0

    for path in collect_files(root):
        if not os.path.isfile(path):
            continue
        rel = os.path.relpath(path, repo_root)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        kind = "md" if path.endswith(".md") else "html"
        own_fragments = doc_scan.fragments(text, kind)
        local_references = set(doc_scan.references(text, kind))
        if kind == "md":
            local_references |= {value for value in doc_scan.MD_LINK_RE.findall(text) if value.startswith("#")}

        for link in sorted(local_references):
            if not doc_scan.is_relative_reference(link):
                continue
            checked += 1
            relative, _, fragment = link.partition("#")
            if not relative:
                continue  # 同一ページ内リンクは下で検証する
            if relative.startswith("/"):
                errors.append(f"{rel}: 絶対パス参照は使わないでください: {link}")
                continue
            absolute = os.path.normpath(os.path.join(os.path.dirname(path), relative))
            if not os.path.exists(absolute):
                errors.append(f"{rel}: 参照先が存在しません: {link}")
                continue
            if not fragment or not absolute.endswith((".html", ".md")):
                continue
            if os.path.abspath(absolute) == os.path.abspath(path):
                target_fragments = own_fragments
                target_label = rel
            else:
                with open(absolute, encoding="utf-8") as fh:
                    target_text = fh.read()
                target_kind = "md" if absolute.endswith(".md") else "html"
                target_fragments = doc_scan.fragments(target_text, target_kind)
                target_label = os.path.relpath(absolute, repo_root)
            if fragment not in target_fragments:
                errors.append(f"{rel}: 参照先 {target_label} に #{fragment} がありません: {link}")

        # コードスパンや本文中のパス表記（ワイルドカード可）も実在確認する。
        # 表示用にリポジトリルート基準で書かれたパスがあるため、ファイル相対・スキルルート・
        # リポジトリルートのいずれかで解決できれば許容する。
        roots = (os.path.dirname(path), root, repo_root)
        # HTML はコードサンプル（<pre> 内の埋め込みコード）を除外してから走査する
        token_source = text if kind == "md" else doc_scan.mask_html(text)
        for token in doc_scan.path_tokens(token_source):
            if token.startswith(("http://", "https://", "//")):
                continue
            checked += 1
            if token.startswith("/"):
                errors.append(f"{rel}: 絶対パス参照は使わないでください: {token}")
                continue
            found = False
            for base in roots:
                if glob.glob(os.path.normpath(os.path.join(base, token))):
                    found = True
                    break
            if not found:
                errors.append(f"{rel}: 参照先が存在しません: {token}")

        for fragment in sorted({link[1:] for link in local_references if link.startswith("#")}):
            checked += 1
            if fragment not in own_fragments:
                errors.append(f"{rel}: ページ内リンク #{fragment} のアンカーがありません")

    showroom_dir = os.path.join(root, "showroom")
    if os.path.isdir(showroom_dir):
        for name in sorted(os.listdir(showroom_dir)):
            if name.endswith(".html") and name != "index.html":
                errors.append(f"showroom/{name}: ショールーム専用の重複実装は置かず、examples/ を参照してください")

    print(f"参照チェック: {checked} 件の相対参照を確認")
    if errors:
        print("\n参照切れチェックに失敗しました:", file=sys.stderr)
        for error in errors:
            print(f"NG: {error}", file=sys.stderr)
        return 1
    print("OK: 参照切れなし（SKILL.md / references / examples / showroom / README.md）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
