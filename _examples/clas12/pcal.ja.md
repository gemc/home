---
layout: default
title: "CLAS12 PCAL"
permalink: /examples/clas12/pcal.html
lang: ja
human_reviewed: false
---

# CLAS12 プリシャワーカロリメータの例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、`clas12-systems` に含まれる CLAS12 プリシャワーカロリメータ（PCAL）のジオメトリを示します。

{% assign example = site.data.examples | where: "title", "PCAL" | first %}

<br/>

## クイックスタート

`clas12-systems` リポジトリから、ジオメトリデータベースをビルドし、短いシミュレーションを実行します。

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/pcal
./pcal.py
gemc pcal.yaml -n=1
```

<br/>

## ジオメトリ

以下に示すジオメトリは、`geometry_src/pcal/pcal.py` と `geometry_src/pcal/geometry.py` で定義されています。
PCAL ビルダーはローカルの coatjava ジオメトリファクトリを読み込み、CLAS12 プリシャワーカロリメータの
セクター、ウィンドウ、鉛層、シンチレータ層、および U、V、W のストリップボリュームを GEMC ボリュームに
変換して、`gemc.db` に格納します。

ワールド（%%root%% という名前のボックス）には、6 つのセクターそれぞれについて以下が含まれます。

- %%pcal_s1%% から %%pcal_s6%% までの名前を持つセクターのマザーボリューム
- %%Stainless_Steel_Front_...%% および %%Stainless_Steel_Back_...%% という名前の前後のステンレス鋼ウィンドウ
- %%Last-a-Foam_Front_...%% および %%Last-a-Foam_Back_...%% という名前の前後の Last-a-Foam ウィンドウ
- %%PCAL_Lead_Layer_<layer>_s<sector>%% という名前の鉛層
- U、V、W のシンチレータ層マザー、ならびに単一／二重ストリップボリューム

PCAL は大規模なジオメトリであるため、この例では以下のインタラクティブビューをエクスポートする際に高速な
PyVista レンダリングパスを使用するよう、`_data/examples.yml` に `pyvista-fast: true` を設定しています。

インタラクティブビューア:

{% assign pcal_vtksz = "/home/assets/images/examples/pcal/pcal.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ pcal_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 PCAL geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理リスト

デフォルトでは `FTFP_BERT` が使用され、YAML ファイルで `phys_list: FTFP_BERT` により選択されます。

{% include notes/physics-list-note.md %}

<br/>

## ジェネレータ

粒子の運動学は YAML ファイルで定義されます。

```yaml
gparticle:
  - name: e-
    p: 5000*MeV
    delta_p: 1*GeV
    theta: 25*deg
    delta_theta: 15*deg
    randomThetaModel: cosine
    delta_phi: 180*deg
```

詳細については [内部ジェネレータのドキュメント]( /home/documentation/generator/internal ) も参照してください。

<br/>

## デジタイゼーション

シンチレータストリップは、共有の CLAS12 %%ecal%% デジタイゼーションプラグインを使用します。PCAL は、hipo の
レイヤー 1 から 3 を使用して、EC システムと同じ ECAL バンクに書き込みます。識別子にはセクター、レイヤー、
ストリップの番号が記録されます。

```python
gvolume.digitization = "ecal"
gvolume.set_identifier("sector", sector, "layer", layer, "strip", pcal_strip_id(uvw, kind, strip))
```

<br/>

## 使い方

### 検出器のビルド

`geometry_src/pcal/pcal.py` を使用して検出器をビルドします。デフォルトでは、セットアップは `gemc.db` という
名前の SQLite ファイルに格納されます。

詳細については [ジオメトリのビルド]( /home/documentation/geometry/geometry_building ) も参照してください。

<br/>

### GEMC の実行

`pcal.yaml` ファイルを使用してセットアップを実行できます。インタラクティブに実行するには `-gui` を追加します。

```shell
gemc pcal.yaml -gui
```

必要に応じて `pcal.yaml` を変更します。特に、粒子の追加、スレッド数の制御、出力の変更などを行います。

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/pcal/gemc_view.png"
caption="CLAS12 PCAL simulation: generated electrons crossing the preshower calorimeter geometry."
%}

<br/>

## 出力

%%gstreamer%% オプションで出力のファイル名と形式を選択します。

```yaml
gstreamer:
  - format: csv
    filename: pcal
  - format: hipo
    filename: pcal
```

詳細については [出力のドキュメント]( /home/documentation/output ) も参照してください。


## GEMC Analyzer によるプロット

まず 2,000 イベントで GEMC を実行します。デフォルトの YAML ファイルはアナライザの CSV ストリームを書き出します。

```shell
gemc pcal.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

ヒットごとに堆積した全エネルギーをプロットします。

```shell
gemc-analyzer pcal_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![pcal total energy deposited per hit][pcal-analyzer_totEdep]{:width="70%"}

[pcal-analyzer_totEdep]: /home/assets/images/examples/pcal/analyzer_totEdep.png

ヒット位置の y 対 x をプロットします。

```shell
gemc-analyzer pcal_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![pcal y vs x hit positions][pcal-analyzer_yvsx]{:width="70%"}

[pcal-analyzer_yvsx]: /home/assets/images/examples/pcal/analyzer_yvsx.png
