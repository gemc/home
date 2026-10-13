---
layout: default
title: "CLAS12 FTOF"
permalink: /examples/clas12/ftof.html
lang: ja
human_reviewed: false
---

# CLAS12 前方飛行時間測定器（FTOF）の例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、`clas12-systems` に含まれる CLAS12 前方飛行時間測定器（FTOF）のジオメトリを示します。

{% assign example = site.data.examples | where: "title", "FTOF" | first %}

<br/>

## クイックスタート

`clas12-systems` リポジトリで、ジオメトリデータベースを構築し、短いシミュレーションを実行します。

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ftof
./ftof.py
gemc ftof.yaml -n=1
```

<br/>

## ジオメトリ

以下に示すジオメトリは、`geometry_src/ftof/ftof.py` と `geometry_src/ftof/geometry.py` で定義されています。
FTOF ビルダーはローカルの coatjava ジオメトリファクトリを読み込み、CLAS12 前方 TOF パネルと
シンチレータパドルを GEMC ボリュームに変換して、`gemc.db` に格納します。

ワールド（%%root%% という名前のボックス）には、6 つのセクターのそれぞれについて次の要素が含まれます。

- %%ftof_p1a_s<sector>%%、%%ftof_p1b_s<sector>%%、%%ftof_p2_s<sector>%% という名前の 3 つのパネル母ボリューム
- %%panel1a_sector<sector>_paddle_<n>%%（23 枚）、%%panel1b_...%%（62 枚）、
  %%panel2_...%%（5 枚）という名前のシンチレータパドル
- パネル 1a と 2 の背後にある、%%ftof_shield_p1a_sector<sector>%% と
  %%ftof_shield_p2_sector<sector>%% という名前の鉛シールド

インタラクティブビューア：

{% assign ftof_vtksz = "/home/assets/images/examples/ftof/ftof.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ftof_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 FTOF geometry"
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

粒子の運動学的パラメータは YAML ファイル内で定義されます。

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

詳細については、[内部ジェネレータのドキュメント]( /home/documentation/generator/internal ) も参照してください。

<br/>

## デジタイゼーション

シンチレータパドルは、CLAS12 固有の %%ftof%% デジタイゼーションプラグインを使用します。各パドルは両端で
読み出されるため、プラグインは各ヒットを左（Left）と右（Right）の PMT チャンネルに分割します。識別子には、
セクター、パネル、パドル、PMT の左右の区別が記録されます。

```python
gvolume.digitization = "ftof"
gvolume.set_identifier("sector", sector, "panel", layer, "paddle", paddle, "side", 0)
```

<br/>

## 使い方

### 検出器の構築

`geometry_src/ftof/ftof.py` を使用して検出器を構築します。デフォルトでは、検出器の構成は SQLite ファイル
`gemc.db` に格納されます。

詳細については、[ジオメトリの構築]( /home/documentation/geometry/geometry_building ) も参照してください。

<br/>

### GEMC の実行

`ftof.yaml` ファイルを使ってこの構成で実行できます。インタラクティブに実行するには `-gui` を追加します。

```shell
gemc ftof.yaml -gui
```

必要に応じて `ftof.yaml` を変更してください。特に、粒子の追加、スレッド数の制御、
出力の変更を行えます。

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/ftof/gemc_view.png"
caption="CLAS12 FTOF simulation: generated electrons crossing the forward time-of-flight geometry."
%}

<br/>

## 出力

%%gstreamer%% オプションで、出力ファイル名と形式を選択します。

```yaml
gstreamer:
  - format: csv
    filename: ftof
  - format: hipo
    filename: ftof
```

詳細については、[出力のドキュメント]( /home/documentation/output ) も参照してください。


## GEMC Analyzer によるプロット

まず GEMC で 2,000 イベントを実行します。デフォルトの YAML ファイルでは、アナライザ用の CSV ストリームを
書き出すように設定されています。

```shell
gemc ftof.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

ヒットごとの総エネルギー付与量をプロットします。

```shell
gemc-analyzer ftof_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![ftof のヒットごとの総エネルギー付与量][ftof-analyzer_totEdep]{:width="70%"}

[ftof-analyzer_totEdep]: /home/assets/images/examples/ftof/analyzer_totEdep.png

ヒット位置の x 座標に対する y 座標をプロットします。

```shell
gemc-analyzer ftof_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![ftof のヒット位置の x 座標に対する y 座標][ftof-analyzer_yvsx]{:width="70%"}

[ftof-analyzer_yvsx]: /home/assets/images/examples/ftof/analyzer_yvsx.png
