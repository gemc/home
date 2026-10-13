---
layout: default
title: "CLAS12 DC"
permalink: /examples/clas12/dc.html
lang: ja
human_reviewed: false
---

# CLAS12 ドリフトチェンバーの例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、`clas12-systems` に含まれる CLAS12 ドリフトチェンバーのジオメトリを紹介します。

{% assign example = site.data.examples | where: "title", "DC" | first %}

<br/>

## クイックスタート

`clas12-systems` リポジトリからジオメトリデータベースを構築し、短いシミュレーションを実行します。

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/dc
./dc.py
gemc dc.yaml -n=1
```

<br/>

## ジオメトリ

以下に示すジオメトリは、`geometry_src/dc/dc.py` と `geometry_src/dc/geometry.py` で定義されています。
DC ビルダーはローカルの coatjava ジオメトリファクトリを読み込み、CLAS12 ドリフトチェンバーの領域と
スーパーレイヤーを GEMC ボリュームに変換して、`gemc.db` に格納します。

ワールド（%%root%% という名前のボックス）には、以下が含まれます。

- %%region1_s1%% から %%region3_s6%% までの名前を持つ、6 セクター分の領域マザーボリューム
- %%sl1_s1%% から %%sl6_s6%% までの名前を持つ、6 セクター分のスーパーレイヤーボリューム

インタラクティブビューア：

{% assign dc_vtksz = "/home/assets/images/examples/dc/dc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ dc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 DC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理リスト

デフォルトでは `FTFP_BERT` が使用され、YAML ファイル内で `phys_list: FTFP_BERT` によって選択されます。

{% include notes/physics-list-note.md %}

<br/>

## ジェネレータ

粒子の運動学的条件は YAML ファイル内で定義されます。

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

スーパーレイヤーの感応設定には、CLAS12 固有の %%dc%% デジタイゼーションプラグインを使用します。識別子には、セクター、
スーパーレイヤー、レイヤー、ワイヤーの番号が記録されます。

```python
gvolume.digitization = "dc"
gvolume.set_identifier("sector", sector, "superlayer", superlayer, "layer", 1, "wire", 1)
```

<br/>

## 使い方

### ディテクタの構築

ディテクタを構築するには `geometry_src/dc/dc.py` を使用します。デフォルトでは、セットアップは
`gemc.db` という名前の SQLite ファイルに格納されます。

詳細については、[ジオメトリの構築]( /home/documentation/geometry/geometry_building ) も参照してください。

<br/>

### GEMC の実行

セットアップの実行には `dc.yaml` ファイルを使用できます。インタラクティブに実行するには `-gui` を追加します。

```shell
gemc dc.yaml -gui
```

必要に応じて `dc.yaml` を変更します。特に、粒子の追加、スレッド数の制御、出力の変更などを行えます。

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/dc/gemc_view.png"
caption="CLAS12 DC simulation: generated electrons crossing the drift chamber geometry."
%}

<br/>

## 出力

%%gstreamer%% オプションで出力ファイル名とフォーマットを選択します。

```yaml
gstreamer:
  - format: csv
    filename: dc
  - format: hipo
    filename: dc
```

詳細については、[出力のドキュメント]( /home/documentation/output ) も参照してください。


## GEMC アナライザによるプロット

まず 2,000 イベントで GEMC を実行します。デフォルトの YAML ファイルはアナライザ用の CSV ストリームを書き出します。

```shell
gemc dc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

ヒットごとの総エネルギー付与量をプロットします。

```shell
gemc-analyzer dc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![dc のヒットごとの総エネルギー付与量][dc-analyzer_totEdep]{:width="70%"}

[dc-analyzer_totEdep]: /home/assets/images/examples/dc/analyzer_totEdep.png

ヒット位置の y 対 x をプロットします。

```shell
gemc-analyzer dc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![dc のヒット位置の y 対 x][dc-analyzer_yvsx]{:width="70%"}

[dc-analyzer_yvsx]: /home/assets/images/examples/dc/analyzer_yvsx.png

デジタイズされた TDC 時間をプロットします。

```shell
gemc-analyzer dc_t0_digitized.csv TDC_TDC --kind csv
```

![dc のデジタイズされた TDC 時間][dc-analyzer_tdc]{:width="70%"}

[dc-analyzer_tdc]: /home/assets/images/examples/dc/analyzer_tdc.png
