# Pyxel Cube 実装リファレンス

`SKILL.md`から必要な節だけ参照する。Pyxel CubeのAPIは通常のPyxel 2D APIと異なるため、引数や戻り値が不明なら公式APIリファレンスで確認する。

## 最小の実行例

```python
import pyxel
from pyxel.cube import Camera, Mat4, Node, Shading, Vec3


class Spinner(Node):
    def on_update(self):
        self.transform = Mat4.from_euler(Vec3(0, pyxel.frame_count * 2, 0))

    def on_draw(self):
        self.box(Mat4.IDENTITY, Vec3(24, 24, 24), 11)


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Cube")
        self.root = Node()
        self.root.add_child(Spinner())

        self.root.camera = Camera()
        self.root.camera.transform = Mat4.look_at(
            Vec3(0, 32, 64), Vec3.ZERO
        )
        self.root.camera.clear_color = 0
        self.root.shading = Shading(pyxel.colors)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.root.update()

    def draw(self):
        self.root.draw(0, 0, pyxel.width, pyxel.height)
        pyxel.text(4, 4, "Q: quit", 7)


App()
```

`pyxel run game.py`で起動する。以後の変更は`Spinner`または必要なNodeを最小限追加して行う。

## APIの使い分け

| 目的 | API・パターン | 注意点 |
| --- | --- | --- |
| 3Dの位置・移動 | `Vec3(x, y, z)`、ベクトル演算、`normalize()` | `x/y/z`は読み取り専用。長さ0の向きは検証する |
| 回転・平行移動・拡縮 | `Mat4.from_euler`、`from_translation`、`from_scale` | 角度は度。積`A * B`は`B`から適用 |
| 親子配置 | `parent.add_child(child)`、`node.transform` | 子の`transform`は親相対。`world_transform`と混同しない |
| 3D視点 | `Camera()`、`Mat4.look_at(eye, target)` | `fov`、`near`、`far`、`ortho_size`を用途に応じて変更 |
| ライティング | `Shading(pyxel.colors)`、`shading.direction` | 親Nodeの設定が子へ継承。独自パレット変更時は再構築 |
| 基本図形 | `Node.box`、`sphere`、`line`、`rect`、`sprite`、`text`等 | `pyxel.rect`などの2D APIと取り違えない |
| テクスチャ | `pyxel.Image.from_image(path)`を`box`等へ渡す | `sprite`はカメラ正面向きでシェーディング対象外 |
| 独自形状 | `Primitive`と`node.prim` | 頂点変更後は必要に応じて`compute_normals()` |
| 3D文字・2D HUD | `node.text(Vec3(...), ...)` / `pyxel.text(x, y, ...)` | HUDはrootの3D描画の後に描く |

`Node.draw(x, y, w, h)`の4値は**画面ピクセル**。`Vec3`で指定する図形サイズと単位が違う。

## GLBモデルとモーション

```python
from pyxel.cube import Mesh, Node

mesh = Mesh.from_glb("assets/character.glb")
actor = Node.from_mesh(mesh)
root.add_child(actor)

for motion in mesh.motions:
    if motion.name == "walk":
        actor.play_motion(motion)
        break
```

- `Mesh.from_glb`で読み込み、`Node.from_mesh`で階層構造を持つNodeを作る。同じMeshから複数のNodeツリーを作成できる。
- `mesh.motions`はアニメーションがないと空。FPSの整合が必要なら`Mesh.from_glb(..., fps=...)`と`pyxel.init(..., fps=...)`を揃える。
- GLBは**三角形ジオメトリ**、親子変換、キーフレームアニメーションを扱う。スキニング・モーフィング、GLB内カメラ/ライト、BLEND半透明等はそのまま使えない。
- 外部ファイル参照があるGLBはロードできない。画像等はGLBに埋め込む。マテリアルの透過切り抜きは`alphaMode: MASK`を使うが、パレット空き状況に制約がある。
- Blockbenchは**Generic Model**を使う。GLB出力で**Embed Textures: ON / Export Groups as Armature: OFF**。必要なときだけアニメーションを出力する。
- ソースの`.bbmodel`を残し、実行には`.glb`を使う。複雑な地形では描画用と簡略化した衝突用のMeshを分ける。

## 衝突と物理（必要な場合のみ）

```python
from pyxel.cube import Collider, Mat4, Vec3

# Nodeの初期化時
self.collider = Collider(size=Vec3(26, 26, 26), mass=1)

# Nodeのメソッド。親のワールド変換が単位行列の場合の最小例
def on_collide(self, other, contact):
    if self.collider.mass > 0:
        shift = Mat4.from_translation(contact.normal * contact.depth)
        self.transform = shift * self.transform
        self.collider.velocity += contact.delta_velocity
        self.collider.angular_velocity += contact.delta_angular_velocity
```

- `mass=0`: 静的な床等。`gravity=0`: 重力なしで自力制御するキャラクター。`trigger=True`: 接触検知専用。
- `Collider.velocity`は更新ごとのワールド座標の変位。3D長さ100を1mとして重力を計算するので、独自スケールでの`gravity`に注意する。
- **衝突時の分離と反発は自動適用されない。** `contact.normal/depth`と`delta_velocity/delta_angular_velocity`に基づいて補正する。
- 上記の平行移動による分離は親の`world_transform == Mat4.IDENTITY`を仮定する。親に回転・拡縮があるならワールド方向からローカル方向へ適切に変換する。
- 球・カプセル・箱の動的Colliderのノードと祖先には、移動と回転のみを適用する。見た目の拡縮は子ノードで行う。Colliderインスタンスはノード間で共有しない。
- `on_collide`中の`active=False`では同一更新内の後続通知は消せない。コインなど1回きりの判定は取得済みフラグで重複を防ぐ。
- レイ判定は`root.raycast(origin, direction, tags={"ground"})`、範囲判定は`overlap_sphere`/`overlap_box`。結果が`None`の場合を処理する。

## よくある失敗の確認順

1. **何も映らない**: `root.camera`、`look_at`の位置、`near/far`、`root.draw(...)`の範囲を確認。
2. **動かない**: `root.update()`が毎フレーム呼ばれ、Nodeの`on_update`が実装され、`active=True`か確認。
3. **位置・向きがずれる**: ローカル/ワールド座標、行列の乗算順序、前方向`-Z`を確認。
4. **表示されない部分がある**: `visible`、背面カリング、深度、GLBのジオメトリ/テクスチャ制約を確認。
5. **衝突するのにすり抜ける**: `on_collide`の補正有無、Colliderの形状/質量、親の変換を確認。
6. **GLBが読めない**: バイナリGLBか、テクスチャを埋め込んだか、非対応アニメーション/モーフが含まれないか確認。

詳しい引数とサンプル: [Cube APIリファレンス](https://kitao.dev/pyxel/api-reference/cube/) / [Cube公式サンプル](https://github.com/kitao/pyxel/tree/main/python/pyxel/examples/cube)
