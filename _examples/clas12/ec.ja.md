---
layout: default
title: "CLAS12 EC"
permalink: /examples/clas12/ec.html
lang: ja
human_reviewed: false
---

# CLAS12 電磁カロリメータの例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、`clas12-systems` の CLAS12 電磁カロリメータ（EC）のジオメトリを示します。

{% assign example = site.data.examples | where: "title", "EC" | first %}

<br/>

## クイックスタート

`clas12-systems` リポジトリ内で、ジオメトリデータベースを構築し、短いシミュレーションを実行します。

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ec
./ec.py
gemc ec.yaml -n=1
```

<br/>

## ジオメトリ

以下に示すジオメトリは、`geometry_src/ec/ec.py` と `geometry_src/ec/geometry.py` で定義されています。
EC ビルダーはローカルの coatjava ジオメトリファクトリを読み込み、CLAS12 カロリメータのセクター、リッド、
鉛アブソーバー、シンチレータストリップを GEMC ボリュームに変換して `gemc.db` に格納します。

ワールド（%%root%% という名前のボックス）には、次のものが含まれます。

- %%ec_s1%% から %%ec_s6%% までの 6 つのセクターマザーボリューム
- セクターごとに 3 つのリッド層（%%eclid1%% から %%eclid3%%）：2 枚のステンレス鋼のスキンと Last-a-Foam のコア
- %%lead_<layer>_s<sector>_view_<view>_stack_<stack>%% という名前の鉛アブソーバー層
- %%U_strip_...%%、%%V_strip_...%%、%%W_strip_...%% という名前の U、V、W の各シンチレータストリップ

EC は大規模なジオメトリであるため、この例では `_data/examples.yml` で `pyvista-fast: true` を設定し、
以下のインタラクティブビューをエクスポートする際に高速な PyVista レンダリングパスを使用します。

インタラクティブビューア：

{% assign ec_vtksz = "/home/assets/images/examples/ec/ec.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ec_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 EC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理リスト

デフォルトでは `FTFP_BERT` が使用され、YAML ファイル内で `phys_list: FTFP_BERT` により選択されます。

{% include notes/physics-list-note.md %}

<br/>

## ジェネレータ

粒子の運動学的条件は YAML ファイルで定義されます。

```yaml
gparticle:
  - name: e-
    p: 5000*MeV
    delta_p: 1*GeV
    theta: 25*deg
    delta_theta: 15*deg
    randomThetaModel: cosine
    phi: 60*deg
    delta_phi: 180*deg
```

詳細については、[内部ジェネレータのドキュメント]( /home/documentation/generator/internal ) も参照してください。

<br/>

## デジタイゼーション

シンチレータストリップは、CLAS12 固有の %%ec%% デジタイゼーションプラグインを使用します。識別子には、
セクター、層、ストリップの各番号が記録されます。

```python
gvolume.digitization = "ec"
gvolume.set_identifier("sector", sector, "layer", hipo_layer, "strip", strip)
```

<br/>

## 使い方

### 検出器の構築

`geometry_src/ec/ec.py` を使って検出器を構築します。デフォルトでは、セットアップは `gemc.db` という名前の
SQLite ファイルに格納されます。

詳細については、[ジオメトリの構築]( /home/documentation/geometry/geometry_building ) も参照してください。

<br/>

### GEMC の実行

`ec.yaml` ファイルを使ってセットアップを実行できます。インタラクティブに実行するには `-gui` を追加します。

```shell
gemc ec.yaml -gui
```

必要に応じて `ec.yaml` を変更します。特に、粒子の追加、スレッド数の制御、出力の変更などを行えます。

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/ec/gemc_view.png"
caption="CLAS12 EC simulation: generated electrons showering in the electromagnetic calorimeter geometry."
%}

<br/>

## 出力

%%gstreamer%% オプションで、出力ファイル名とフォーマットを選択します。

```yaml
gstreamer:
  - format: csv
    filename: ec
  - format: hipo
    filename: ec
```

詳細については、[出力のドキュメント]( /home/documentation/output ) も参照してください。


## GEMC Analyzer によるプロット

まず GEMC で 2,000 イベントを実行します。デフォルトの YAML ファイルではアナライザ用の CSV ストリームを出力します。

```shell
gemc ec.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

ヒットごとの総エネルギー付与量をプロットします。

```shell
gemc-analyzer ec_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![ec のヒットごとの総エネルギー付与量][ec-analyzer_totEdep]{:width="70%"}

[ec-analyzer_totEdep]: /home/assets/images/examples/ec/analyzer_totEdep.png

ヒット位置の y 対 x をプロットします。

```shell
gemc-analyzer ec_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![ec のヒット位置の y 対 x][ec-analyzer_yvsx]{:width="70%"}

[ec-analyzer_yvsx]: /home/assets/images/examples/ec/analyzer_yvsx.png
