---
layout: default
title: "CLAS12 FT"
permalink: /examples/clas12/ft.html
lang: ja
human_reviewed: false
---

# CLAS12 Forward Tagger の例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、`clas12-systems` に含まれる CLAS12 Forward Tagger (FT) のジオメトリを紹介します。FT は小さな
極角の位置に配置され、電磁カロリメータ、シンチレータホドスコープ、Micromegas トラッカーという 3 つの
サブシステムで構成されています。

FT のジオメトリとデジタイズは、GEMC 0.5 および `pygemc` 0.5.0 と組み合わせて `clas12-systems` 0.3 で利用
できます。

{% assign example = site.data.examples | where: "title", "FT" | first %}

<br/>

## クイックスタート

`clas12-systems` リポジトリで、ジオメトリデータベースをビルドして短いシミュレーションを実行します。

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ft
./ft.py
gemc ft.yaml -n=1
```

<br/>

## ジオメトリ

以下に示すジオメトリは `geometry_src/ft/geometry.py` で定義され、`geometry_src/ft/ft.py` によってビルド
されます。FT ビルダーは 3 つのサブシステムをまとめて単一の `gemc.db` に格納します。

- **カロリメータ**：PbWO4 結晶のマトリクスで、各結晶はラッピングされて APD に結合されており、
  %%ft_cal_cr_h<ih>_v<iv>%% という名前が付けられます。銅製ハウジング、マザーボード、遮蔽ボリュームも含まれます
- **ホドスコープ**：セクター、レイヤー、コンポーネントごとに名前が付けられたシンチレータタイル
- **トラッカー**：各レイヤーの両側にカプトン、フォトレジスト、リングのボリュームを備えた Micromegas ディスク

ワールド（%%root%% という名前のボックス）には、これら 3 つのサブシステムがすべて含まれます。入射粒子
のフラックスを記録するために、カロリメータとトラッカーにフラックス検出器が追加されています。

インタラクティブビューア：

{% assign ft_vtksz = "/home/assets/images/examples/ft/ft.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ft_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 FT geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理リスト

デフォルトでは `FTFP_BERT` が使用され、YAML ファイルで `phys_list: FTFP_BERT` によって選択されます。

{% include notes/physics-list-note.md %}

<br/>

## ジェネレータ

粒子の運動学的条件は YAML ファイルで定義されます。

```yaml
gparticle:
  - name: e-
    p: 2000*MeV
    theta: 3*deg
    phi: 10*deg
    delta_phi: 180*deg
```

詳細については [内部ジェネレータのドキュメント]( /home/documentation/generator/internal ) も参照してください。

<br/>

## デジタイズ

各 FT サブシステムは、それぞれ独自の CLAS12 固有のデジタイズプラグインを使用します。カロリメータ結晶は
%%ft_cal%%、ホドスコープタイルは %%ft_hodo%%、トラッカーディスクは %%ft_trk%% を使用します。識別子には
読み出すコンポーネントが記録されます。例えば、カロリメータ結晶の行と列は次のように指定します。

```python
digitization="ft_cal",
identifiers=("ih", ix, "iv", iy),
```

<br/>

## 使い方

### 検出器のビルド

`geometry_src/ft/ft.py` を使って検出器をビルドします。デフォルトでは、セットアップは `gemc.db` という
名前の SQLite ファイルに保存されます。

詳細については [ジオメトリのビルド]( /home/documentation/geometry/geometry_building ) も参照してください。

<br/>

### GEMC の実行

`ft.yaml` ファイルを使ってセットアップを実行できます。インタラクティブに実行するには `-gui` を追加します。

```shell
gemc ft.yaml -gui
```

必要に応じて `ft.yaml` を変更します。特に、粒子の追加、スレッド数の制御、出力の変更などを行います。

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/ft/gemc_view.png"
caption="CLAS12 FT simulation: generated electrons crossing the forward tagger geometry."
%}

<br/>

## 出力

%%gstreamer%% オプションで出力ファイル名とフォーマットを選択します。

```yaml
gstreamer:
  - format: csv
    filename: ft
  - format: hipo
    filename: ft
```

詳細については [出力ドキュメント]( /home/documentation/output ) も参照してください。

Forward Tagger は、異なる識別子構造を持つ 3 つの検出器（%%ft_cal%%、%%ft_hodo%%、%%ft_trk%%）を読み出します。
以下のアナライザの例では、フラックス、ホドスコープ、トラッカーの各検出器について真値情報の出力と
デジタイズ出力を無効にし、CSV に一貫した %%ft_cal%% スキーマが含まれるようにしています。


## GEMC アナライザによるプロット

まず 2,000 イベントで GEMC を実行します。デフォルトの YAML ファイルはアナライザの CSV ストリームを
書き出します。

```shell
gemc ft.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build \
  -no_true_info="flux ft_hodo ft_trk" -no_digitized="flux ft_hodo ft_trk"
```

ヒットごとの総付与エネルギーをプロットします。

```shell
gemc-analyzer ft_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![ft のヒットごとの総付与エネルギー][ft-analyzer_totEdep]{:width="70%"}

[ft-analyzer_totEdep]: /home/assets/images/examples/ft/analyzer_totEdep.png

ヒット位置の y 対 x をプロットします。

```shell
gemc-analyzer ft_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![ft のヒット位置の y 対 x][ft-analyzer_yvsx]{:width="70%"}

[ft-analyzer_yvsx]: /home/assets/images/examples/ft/analyzer_yvsx.png
