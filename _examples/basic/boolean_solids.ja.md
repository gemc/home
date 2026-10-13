---
layout: default
title: "Boolean Solids"
permalink: /examples/basic/boolean_solids.html
lang: ja
human_reviewed: false
---

# ブール演算ソリッドの例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、GEMC のソリッドに対するブール演算を示します。未配置の構成ボリュームから、
配置する 3 つのソリッドを構築します。穴をくり抜いたプレート、和集合で作った十字形、
2 つの球の共通部分で作ったレンズです。

<br/>

## クイックスタート

この例を現在のディレクトリにコピーします。
ジオメトリを作成して 10 イベントを実行するには、次のようにします。

```shell
cp -r $GEMC_HOME/examples/basic/boolean_solids .
cd boolean_solids
./boolean_solids.py
gemc boolean_solids.yaml -n=10
```

<br/>

## ジオメトリ

ジオメトリは `boolean_solids.py` で定義されています。

ワールド（%%root%% という名前のボックス）には、3 つの可視のブール演算ボリュームが含まれます。

| ボリューム | 演算 | 構成要素 |
|--------|-----------|------------|
| %%plate_with_hole%% | 差集合 | %%plate_box - plate_hole%% |
| %%cross%% | 和集合 | %%bar + bar_rotated%% |
| %%lens%% | 共通部分 | %%sphere_one * sphere_two%% |

構成ボリュームは特別なマテリアル %%Component%% を使用します。これらはブール式の
オペランドを定義しますが、可視の検出器ボリュームとしては配置されません。演算結果のボリュームは、
他の `GVolume` と同様に、それぞれのマテリアル、色、位置、回転を指定して配置します。

インタラクティブビューア:

{% assign boolean_solids_vtksz = "/assets/images/examples/boolean_solids/boolean_solids.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ boolean_solids_vtksz }}"
  title="Interactive VTK.js view of the boolean solids geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## ブール式

%%solidsOpr%% に式を設定することで、ブール演算ソリッドを指定します。

```python
plate.solidsOpr = 'plate_box - plate_hole'
cross.solidsOpr = 'bar + bar_rotated'
lens.solidsOpr = 'sphere_one * sphere_two'
```

最初のオペランドは、それ自身の原点で評価されます。2 番目のオペランドには、最初のオペランドを基準とした
自身の位置と回転が適用されます。例えば、%%plate_hole%% は %%plate_box%% から差し引かれる前に
30 mm 移動されるため、穴は中心からずれた位置にできます。

<br/>

## ジェネレータ

粒子の運動学的条件は YAML ファイルで定義されます。

```yaml
gparticle:
  - name: e-
    p: 500*MeV
    theta: 90*deg
    vx: -40*cm
    delta_vx: 12*cm
    randomVertexModel: uniform
```

詳細については、[内部ジェネレータのドキュメント]( /home/documentation/generator/internal ) も参照してください。

<br/>

## 使い方

### 検出器の構築

Python スクリプト `boolean_solids.py` を使って検出器を構築します。デフォルトでは、構成は
`gemc.db` という名前の SQLite ファイルに保存されます。

```shell
./boolean_solids.py
```

詳細については、[ジオメトリの構築]( /home/documentation/geometry/geometry_building ) も参照してください。

<br/>

### GEMC の実行

`boolean_solids.yaml` ファイルを使って、この構成でシミュレーションを実行できます。対話的に実行するには
`-gui` を追加します。

```shell
gemc boolean_solids.yaml -gui
```

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/boolean_solids/gemc_view.png"
caption="Boolean solids simulation: electrons crossing the subtraction, union, and intersection volumes."
%}
