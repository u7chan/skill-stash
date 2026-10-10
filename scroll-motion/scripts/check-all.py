#!/usr/bin/env python3
"""scroll-motion の検証スクリプトをまとめて実行する（python3 標準ライブラリのみ）。

使い方:
  python3 scripts/check-all.py
  python3 scripts/check-all.py --verbose   # 各チェックの出力も表示する
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

CHECKS = (
    "build-showroom.py",
    "check-catalog.py",
    "check-references.py",
    "check-external-deps.py",
    "check-reduced-motion.py",
    "check-mobile.py",
    "check-hooks.py",
    "check-pair-equivalence.py",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="scroll-motion の全チェックを実行する")
    parser.add_argument("--verbose", action="store_true", help="各チェックの標準出力も表示する")
    args = parser.parse_args()

    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    results = []
    for name in CHECKS:
        script = os.path.join(scripts_dir, name)
        command = [sys.executable, script, "--check"] if name == "build-showroom.py" else [sys.executable, script]
        completed = subprocess.run(command, capture_output=True, text=True)
        results.append((name, completed.returncode, completed.stdout, completed.stderr))
        state = "OK" if completed.returncode == 0 else "NG"
        print(f"[{state}] {name}")
        if args.verbose or completed.returncode != 0:
            for line in (completed.stdout + completed.stderr).strip().splitlines():
                print(f"      {line}")

    failed = [name for name, code, _, _ in results if code != 0]
    print()
    if failed:
        print(f"検証失敗: {len(failed)} / {len(results)} 件 -> {', '.join(failed)}", file=sys.stderr)
        return 1
    print(f"全 {len(results)} 件の検証に成功しました")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
