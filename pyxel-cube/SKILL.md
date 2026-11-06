---
name: pyxel-cube
description: Pyxel 3.0以降のPyxel Cubeでレトロ3Dゲームを新規作成・拡張・デバッグ・レビューする。Nodeツリー、Camera、3D描画、GLBモデル、アニメーション、衝突・物理演算を扱うときに使う。
---

# Pyxel Cube

PythonのPyxel Cubeで、要求された3Dゲームの動作を最小構成から実装する。既存プロジェクトへの適用では、その構成と使用中のPyxel APIを優先する。

## 適用範囲

- Pyxel 3.0以降の `pyxel.cube` による3Dゲーム・3D表現の実装、修正、レビュー。
- 2DのみのPyxel処理では通常のPyxel APIを使い、このスキルの3D構成を持ち込まない。
- 初めてPyxelを導入する場合はPython 3.11以降とPyxelのインストール状況を確認する。

## 実装フロー

1. **現状を確認**: 起動ファイル、Pyxelバージョン、既存のNode構成、画面サイズ、アセット、実行コマンドを確認する。新規なら操作・勝敗条件・視点に必要な最小シーンを決める。
2. **動く最小シーンを作る**: `pyxel.init` → `Node`のroot → 子Node → `Camera` → `pyxel.run(update, draw)`。各フレームで`root.update()`と`root.draw(x, y, w, h)`を呼ぶ。最小例は[実装リファレンス](references/implementation.md)。
3. **3Dの状態と表示を分ける**: `on_update`で入力・ゲーム状態・`transform`を更新し、`on_draw`で3D形状を描く。スコア・操作説明など固定HUDは3D描画の後に通常の`pyxel`の2D APIで描く。
4. **必要な機能だけ追加**: 単純な形状 → テクスチャ・シェーディング → GLB・モーション → 衝突・物理の順で、要求に必要なものだけ導入する。詳細はリファレンスの該当節のみ読む。
5. **検証して報告**: 変更ファイルを構文チェックし、実行可能な環境なら`pyxel run`で起動・入力・描画を確認する。未実行の項目は未検証と明示する。

## 設計上の必須ルール

- **Nodeを中心に組み立てる**: `Node`を継承し、`on_update`/`on_draw`を実装する。親子の`transform`はローカル座標、`world_transform`はワールド座標。複数オブジェクトに同じ更新・描画処理を重複させない。
- **座標を混同しない**: 標準的には右が`+X`、上が`+Y`、前が`-Z`。3Dは`Vec3`、変換は`Mat4`、2D HUDはスクリーン座標。`Mat4`の積は右側から適用される。
- **値の更新方法に注意**: `Vec3`の`x/y/z`を直接変更しない。必要なら新しいベクトルを作り、`transform`を再代入する。
- **カメラを明示**: `root.camera = Camera()`と`Mat4.look_at`を基本にし、用途に応じて透視投影か`ortho_size`による平行投影を選ぶ。`clear_color=None`は既存2D背景を残す場合に使う。
- **衝突補正を省略しない**: `Collider`の接触通知だけでは分離・反発しない。`on_collide(other, contact)`で必要な位置と速度補正を実装する。単に当たり判定するだけなら`trigger=True`を使う。異なるNode間で同じ`Collider`インスタンスを共有しない。
- **GLBに存在しない機能を仮定しない**: `Mesh.from_glb`/`Node.from_mesh`で読み込み、必要なら`mesh.motions`を使用する。スキニング・モーフィング・半透明BLEND・GLB内ライト等がそのまま動く前提で設計しない。
- **過剰実装を避ける**: 独自3Dレンダラー・外部物理エンジン・抽象化レイヤーを先に増やさない。Pyxel Cubeが提供するNode、描画、Colliderで満たせるかを先に判断する。

## 検証

```sh
python -m py_compile path/to/game.py
pyxel run path/to/game.py
```

- `py_compile`は構文チェックのみ。3D描画・カメラ・衝突・アセット読み込みを保証しない。
- GUI/実行環境があるときは、起動・操作入力・オブジェクトの前後関係・カメラ・シーン更新を実機確認する。
- `pyxel copy_examples`は既存の`pyxel_examples`ディレクトリを**上書きする**ため、編集済みのサンプルがある環境では安易に実行しない。

## 関連情報

- [実装リファレンス](references/implementation.md): 動作する最小例、APIの使い分け、物理、GLB、診断ポイント。
- [公式Cubeユーザーガイド](https://kitao.dev/pyxel/user-guide/cube/)
- [公式Cube APIリファレンス](https://kitao.dev/pyxel/api-reference/cube/)
- [Cube公式サンプル](https://github.com/kitao/pyxel/tree/main/python/pyxel/examples/cube)
