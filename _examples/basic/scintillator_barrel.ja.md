---
layout: default
title: "Scintillator Barrel"
permalink: /examples/basic/scintillator_barrel.html
lang: ja
human_reviewed: false
---

# シンチレータバレル
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、48枚の台形パドルをリング状に一周配置した円筒形のシンチレータバレル検出器を構築します。
`distribute_on_circle` API を使って、円周上に等角度間隔でボリュームを複製する方法を示します。
また、隣り合う面がほぼ隙間なく接するように、
パドルの寸法を決める方法を説明します。


{% assign example = site.data.examples | where: "title", "Scintillator Barrel" | first %}
この例はブラウザ上で実行できます: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## クイックスタート

この例を現在のディレクトリにコピーします。
ジオメトリを作成して3イベントを実行するには、次のようにします。

```shell
cp -r $GEMC_HOME/examples/basic/scintillator_barrel .
cd scintillator_barrel
./scintillator_barrel.py
gemc scintillator_barrel.yaml
```

<br/>

## ジオメトリ

ジオメトリは `scintillator_barrel.py` で定義されています。ワールド（%%root%% という名前のボックス）には、
リング状に配置された48個の同一の %%paddle%% ボリュームが含まれています。

- 各 %%paddle%% は `G4Trap` の一般台形ソリッド（材質は %%G4_PLASTIC_SC_VINYLTOLUENE%%）で、
  幅の広い面が半径方向外側を、幅の狭い面がビーム軸側を向いています。
- 隣接する外側の面が隙間なく接するように、弦の公式を使ってパドルの寸法を決めます。
  - 外側の半幅: `pX  = (radius + pY) × sin(π/n)`
  - 内側の半幅: `pLTX = (radius − pY) × sin(π/n)`
- `distribute_on_circle(n=48, radius=400 mm, align=True, axis='z')` は、各コピーを z 軸まわりに
  7.5° の等間隔で配置し、回転させます。

`distribute_on_circle` の完全な API リファレンスと寸法の計算に用いる幾何学的関係については、
[構造ヘルパー](/home/documentation/geometry/structure)のドキュメントを参照してください。

インタラクティブビューア（48枚すべてのパドルで構成されるバレル）:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/scintillator_barrel/scintillator_barrel.vtksz"
  title="Interactive VTK.js view of the scintillator_barrel geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理リスト

デフォルトでは `QBBC` が使用され、YAML ファイルで `phys_list: QBBC` として選択されます。

{% include notes/physics-list-note.md %}

<br/>

## ジェネレータ

粒子の運動学的条件は YAML ファイルで定義されます。

```yaml
gparticle:
  - name: proton
    p: 500*MeV
    theta: 90*deg
    delta_phi: 360*deg
    multiplicity: 3
```

詳細については、[内部ジェネレータのドキュメント]( /home/documentation/generator/internal )も参照してください。

<br/>

## デジタイゼーション

各 %%paddle%% には、一意のパドル識別子とともに %%flux%% デジタイゼーションが割り当てられます。

```python
paddle.digitization = "flux"
# ...
v.set_identifier("paddle", i)
```

詳細については、[フラックスのドキュメント]( /home/documentation/sensitivity/flux )を参照してください。

<br/>

## `distribute_on_circle` API

`GVolume` の `distribute_on_circle` メソッドは、指定した半径 `radius` の円周上に
テンプレートボリュームを `n` 個複製します。`align=True` の場合、各コピーはさらに、選択した軸のまわりに
その角度位置 φᵢ だけ回転し、各パドルのローカル座標系が半径方向に揃います。

```python
for i, v in enumerate(paddle.distribute_on_circle(n, radius, align=True, axis='z')):
    v.set_identifier("paddle", i)
    v.publish(cfg)
```

このメソッドは、角度ステップごとに1つずつ、独立した `GVolume` コピーのリストを返します。各コピーは
`<name>_i` という名前で、`(radius·cos φᵢ, radius·sin φᵢ, 0)` に配置されます。
完全な API リファレンスは[構造ヘルパー](/home/documentation/geometry/structure)のドキュメントにあります。

<br/>

## 使い方

### 検出器の構築

検出器を構築するには Python スクリプト `scintillator_barrel.py` を使用します。デフォルトでは、
構成は `gemc.db` という名前の SQLite ファイルに保存されます。コマンドラインオプションで
データベースの種類、バリエーション、ラン番号を指定できます。

詳細については、[ジオメトリの構築]( /home/documentation/geometry/geometry_building )も参照してください。

<br/>

### GEMC の実行

`scintillator_barrel.yaml` ファイルを使ってシミュレーションを実行します。インタラクティブに実行するには、
`-gui` を追加します。

```shell
gemc scintillator_barrel.yaml -gui
```

必要に応じて `scintillator_barrel.yaml` を変更してください。特に、イベント数の変更、
スレッド数の増加、出力形式の選択などを行えます。

<br/>

## イベントの実行

以下のビューは、θ = 90° で半径方向外側に3個の陽子を発射した1イベント後のバレルを、
ビーム軸方向から見たものです。各陽子はシンチレータパドルを1枚ずつ通過します。

{% include figure.html
src="/assets/images/examples/scintillator_barrel/gemc_view.png"
caption="Scintillator barrel viewed end-on along the beam axis. Three protons at θ = 90°
travel radially outward, each depositing energy in one paddle."
%}

<br/>

## 出力

%%gstreamer%% オプションで出力ファイル名と形式を選択します。

```yaml
gstreamer:
  - format: csv
    filename: barrel
```

詳細については、[出力のドキュメント]( /home/documentation/output )も参照してください。

<br/>

## GEMC Analyzer によるプロット

まず1,000イベントで GEMC を実行します。デフォルトの YAML ファイルはアナライザ用の CSV ストリームを書き出します。

```shell
gemc scintillator_barrel.yaml -n=1000
```

ヒットごとの総エネルギー付与量をプロットします。

```shell
gemc-analyzer barrel_t0_digitized.csv totEdep --kind csv
```

![scintillator_barrel のヒットごとの総エネルギー付与量][scintillator_barrel-analyzer_totEdep]{:width="70%"}

[scintillator_barrel-analyzer_totEdep]: /home/assets/images/examples/scintillator_barrel/analyzer_totEdep.png

粒子トラックの真のエネルギーをプロットします。

```shell
gemc-analyzer barrel_t0_true_info.csv E --kind csv --data true_info
```

![scintillator_barrel の粒子トラックの真のエネルギー][scintillator_barrel-analyzer_true_energy]{:width="70%"}

[scintillator_barrel-analyzer_true_energy]: /home/assets/images/examples/scintillator_barrel/analyzer_true_energy.png
