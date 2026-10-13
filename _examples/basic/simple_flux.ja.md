---
layout: default
title: "Simple flux"
permalink: /examples/basic/simple_flux.html
lang: ja
human_reviewed: false
---

# シンプルなフラックス検出器
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、%%flux%% デジタイゼーションを使用して、真値情報とデジタイズされた情報を出力に保存します。

{% assign example = site.data.examples | where: "title", "Simple Flux" | first %}

この例はブラウザ上で実行できます: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## クイックスタート

この例をカレントディレクトリにコピーします。
ジオメトリを作成し、10 イベントを実行し、ROOT および CSV の出力ファイルを生成するには、以下を実行します:

```shell
cp -r $GEMC_HOME/examples/basic/simple_flux .
cd simple_flux
./simple_flux.py
gemc simple_flux.yaml -n=10
```

<br/>

## ジオメトリ

以下に示すジオメトリは `simple_flux.py` で定義されています。

ワールド（%%root%% という名前のボックス）には、次のものが含まれます:

- %%target%%: 円柱形の液体水素ターゲット（%%G4_lH2%%）
- %%FluxPlane%%: 空気（%%G4_AIR%%）でできたボックスで、%%flux%% デジタイゼーションが割り当てられています


インタラクティブビューア:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/simple_flux/simple_flux.vtksz"
  title="Interactive VTK.js view of the simple_flux geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>


<br/>

## 物理リスト

デフォルトでは `QBBC` が使用され、YAML ファイル内で `phys_list: QBBC` により選択されます。

{% include notes/physics-list-note.md %}

<br/>


## ジェネレータ

粒子の運動学的条件は YAML ファイルで定義されます:

```yaml
gparticle:
  - name: proton
    p: 2000*MeV
    vz: -3*cm
    delta_vx: 0.1*cm
    delta_vy: 0.1*cm
    multiplicity: 10
```

詳細は [内部ジェネレータのドキュメント]( /home/documentation/generator/internal ) も参照してください。

<br/>


## デジタイゼーション

%%FluxPlane%% の感応設定には、%%flux%% デジタイゼーション（GEMC に組み込まれたルーチンの一つ）を使用します。
`simple_flux.py` で指定され、識別子は %%flux_plane = 1%% です。

```python
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
```

この場合、%%identifier%% には %%flux_plane%% という 1 つの名前が含まれます。

詳細は [Flux のドキュメント]( /home/documentation/sensitivity/flux ) を参照してください。


デジタイズされた変数に加えて、真値情報も出力ストリームに保存されます。

{% include notes/true_info-note.md %}


<br/>

## 使い方

### 検出器のビルド

検出器をビルドするには Python スクリプト `simple_flux.py` を使用します。デフォルトでは、セットアップは SQLite ファイル
`gemc.db` に保存されます。コマンドラインオプションで、データベースの種類、バリエーション、ラン番号を指定できます。

詳細は [ジオメトリのビルド]( /home/documentation/geometry/geometry_building ) も参照してください。


<br/>

### GEMC の実行

`simple_flux.yaml` ファイルを使ってセットアップを実行できます。インタラクティブに実行するには `-gui` を追加します:

```shell
gemc simple_flux.yaml -gui
```

必要に応じて `simple_flux.yaml` を変更してください。特に、粒子の追加、スレッド数の制御、出力の変更などを行えます。

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/simple_flux/gemc_view.png"
caption="Simple flux simulation: proton tracks traversing the flux detector volumes."
%}

<br/>

## 出力

%%gstreamer%% オプションで、出力ファイル名とフォーマットを選択します:

```yaml
gstreamer:
  - format: csv
    filename: simple_flux
```

%%flux%% はイベントごとのデジタイゼーションであるため、GEMC はスレッドごとに 1 つの出力ファイルを生成します。
ROOT ファイルの場合は、`hadd` を使ってファイルをマージできます。


詳細は [出力のドキュメント]( /home/documentation/output ) も参照してください。


<br/>

## GEMC Analyzer によるプロット

まず 10,000 イベントで GEMC を実行します。デフォルトの YAML ファイルはアナライザ用の CSV ストリームを書き出します。

```shell
gemc simple_flux.yaml -n=10000
```

ヒットごとに付与された総エネルギーをプロットします:

```shell
gemc-analyzer simple_flux_t0_digitized.csv totEdep --kind csv
```

![simple_flux のヒットごとに付与された総エネルギー][simple_flux-analyzer_totEdep]{:width="70%"}

[simple_flux-analyzer_totEdep]: /home/assets/images/examples/simple_flux/analyzer_totEdep.png

粒子トラックのエネルギーの真値をプロットします:

```shell
gemc-analyzer simple_flux_t0_true_info.csv E --kind csv --data true_info
```

![simple_flux の粒子トラックのエネルギーの真値][simple_flux-analyzer_true_energy]{:width="70%"}

[simple_flux-analyzer_true_energy]: /home/assets/images/examples/simple_flux/analyzer_true_energy.png
