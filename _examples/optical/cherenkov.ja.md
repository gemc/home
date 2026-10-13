---
layout: default
title: "Cherenkov"
permalink: /examples/optical/cherenkov.html
lang: ja
human_reviewed: false
---

[low-img]: /home/assets/images/examples/cherenkov/low_index_radiator.png
[medium-img]: /home/assets/images/examples/cherenkov/medium_index_radiator.png
[high-img]: /home/assets/images/examples/cherenkov/high_index_radiator.png
[lowy-img]: /home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png
[mediumy-img]: /home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png
[highy-img]: /home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png


# Cherenkov の例 
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、GEMC 検出器で Cherenkov 放射を有効にする方法を示します。
3 つのラジエーター名は、中立的なデモ用のラベルです。これらの光学定数は非物理的な場合があり、
実在する材料の定義として解釈すべきではありません。

{% assign example = site.data.examples | where: "title", "Cherenkov" | first %}

この例はブラウザ上で実行できます: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## クイックスタート

この例を現在のディレクトリにコピーします。
ジオメトリを作成し、1 イベントを実行し、ROOT および CSV の出力ファイルを生成するには:

```shell
cp -r $GEMC_HOME/examples/optical/cherenkov .
cd cherenkov
./cherenkov.py
gemc cherenkov.yaml -n=1
```

<br/>

## ジオメトリ

以下に示すジオメトリは `cherenkov.py` で定義されています。これは 3 つのバリエーションで生成されます:
%%default%%、%%mediumIndexRadiator%%、%%highIndexRadiator%% です。

ワールド（%%root%% という名前のボックス）には %%radiator%% ボックスが含まれます。ラジエーターの材料は選択したバリエーションによって異なります:

{:.zebra .compact-table}

| バリエーション | 材料 | 色 | 屈折率の範囲 |
|-----------|----------|-------|------------------------|
| %%default%% | %%lowIndexRadiator%% | 赤 | 1.0010-1.0013 |
| %%mediumIndexRadiator%% | %%mediumIndexRadiator%% | 青 | 1.0110-1.0150 |
| %%highIndexRadiator%% | %%highIndexRadiator%% | 緑 | 1.0500-1.0530 |


- 4 つのボックス（%%detector_left%%、%%detector_right%%、%%detector_top%%、%%detector_bottom%%）で構成される %%gPhotonDetector%% 検出器。これにより、ビーム用に中心部へ小さな穴が残されます。

インタラクティブビューア:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/cherenkov/cherenkov.vtksz"
  title="Interactive VTK.js view of the Cherenkov geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="/assets/images/examples/cherenkov/high_index_radiator.png"
caption="Cherenkov geometry with 1 generated electron. The highIndexRadiator volume (green, style = 2 renders it as a cloud) is the medium generating Cherenkov radiation."
%}


<br/>

## 物理リスト

YAML ファイルではデフォルトで `FTFP_BERT + G4OpticalPhysics` が使用されます。光学光子を生成するには、光学物理コンポーネントが必要です。

{% include notes/physics-list-note.md %}

<br/>

## ジェネレーター

粒子の運動学は YAML ファイルで定義されています:

```yaml
gparticle:
  - name: e-
    p: 1000*MeV
    vz: -50*cm
```

詳細については、[内部ジェネレーターのドキュメント]( /home/documentation/generator/internal ) も参照してください。


<br/>


## デジタイゼーション

検出器ボリュームの感度は、`cherenkov.py` 内の %%gPhotonDetector%% デジタイゼーション（GEMC に組み込まれている
利用可能なルーチンの 1 つ）で指定されます。

%%identifier%% は、異なる検出器ボックスを区別するために使用されます:

```python
backplate.digitization = "gPhotonDetector"
backplate.set_identifier("detector", panel_id)
```

詳細については、[Flux のドキュメント]( /home/documentation/sensitivity/gPhotonDetector ) を参照してください。


<br/>

## 使い方

### 検出器の構築

Python スクリプト `cherenkov.py` を使用して検出器を構築します。デフォルトでは、セットアップは
`gemc.db` という名前の SQLite ファイルに保存されます。コマンドラインオプションで、データベースの種類、
バリエーション、ラン番号を定義できます。

詳細については、[ジオメトリの構築]( /home/documentation/geometry/geometry_building ) も参照してください。

<br/>

### GEMC の実行

ファイル `cherenkov.yaml` を使用してセットアップを実行できます。インタラクティブに実行するには `-gui` を追加します:

```shell
gemc cherenkov.yaml -gui
```

YAML は `g4view.cloudPoints: 60000` を設定しており、クラウドスタイルのボリュームが、レンダリングされた
ジオメトリのスクリーンショットに対して十分に密になるようにしています。

必要に応じて `cherenkov.yaml` を変更してください。特に、粒子の追加、スレッド数の制御、出力の変更などに使用します。
%%gPhotonDetector%% デジタイゼーションは、エネルギーをまったく付与しない場合でも光学光子を記録するため、
この例では %%recordZeroEdep%% は必要ありません。

<br/>

### バリエーション

YAML ファイル内では、バリエーションは %%mediumIndexRadiator%% に設定されています。材料を変更するには、これを
%%default%% または %%highIndexRadiator%% に置き換えることができます。例えば:

```yaml
gsystem:
  - name: cherenkov
    variation: highIndexRadiator
```

以下に示すように、ラジエーター材料が異なると、光子の収量や角度も異なります。
これらの光学定数はデモ用の値であり、非物理的な場合があります。
バリエーションごとに個別の出力ファイルが必要な場合は、%%gstreamer%% のファイル名にバリエーション名を使用してください。


<br/>

|:---:|:---:|:---:|
| ![low index radiator](/home/assets/images/examples/cherenkov/low_index_radiator.png) | ![medium index radiator](/home/assets/images/examples/cherenkov/medium_index_radiator.png) | ![high index radiator](/home/assets/images/examples/cherenkov/high_index_radiator.png) |
| ![low index radiator y vs x](/home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png) | ![medium index radiator y vs x](/home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png) | ![high index radiator y vs x](/home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png) |

<p class="image-caption">
  左: <span class="gstring">lowIndexRadiator</span>、中央: <span class="gstring">mediumIndexRadiator</span>、右: <span class="gstring">highIndexRadiator</span>。
</p>

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/cherenkov/gemc_view.png"
caption="Cherenkov simulation: electron beam entering the radiator volume."
%}

<br/>

## 出力

%%gstreamer%% オプションは、出力ファイル名とフォーマットを選択します:


```yaml
gstreamer:
  - format: csv
    filename: cherenkov
```

%%gPhotonDetector%% はイベントごとのデジタイゼーションであるため、GEMC はスレッドごとに 1 つの出力ファイルを生成します。
ROOT ファイルの場合は、`hadd` を使用してファイルをマージできます。

詳細については、[出力のドキュメント]( /home/documentation/output ) も参照してください。

<br/>

## GEMC Analyzer によるプロット

まず GEMC を 1 イベントで実行します。デフォルトの YAML ファイルは、アナライザー用の CSV ストリームを書き出します。

```shell
gemc cherenkov.yaml -n=1
```

ヒットごとに付与された総エネルギーをプロットします:

```shell
gemc-analyzer cherenkov_t0_digitized.csv totEdep --kind csv
```

![cherenkov total energy deposited per hit][cherenkov-analyzer_totEdep]{:width="70%"}

[cherenkov-analyzer_totEdep]: /home/assets/images/examples/cherenkov/analyzer_totEdep.png

y 対 x のヒット位置をプロットします:

```shell
gemc-analyzer cherenkov_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![cherenkov y vs x hit positions][cherenkov-analyzer_yvsx]{:width="70%"}

[cherenkov-analyzer_yvsx]: /home/assets/images/examples/cherenkov/analyzer_yvsx.png
