---
layout: default
title: "CLAS12 HTCC"
permalink: /examples/clas12/htcc.html
lang: ja
human_reviewed: false
---

# CLAS12 高閾値チェレンコフカウンターの例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、`clas12-systems` に含まれる CLAS12 高閾値チェレンコフカウンター (HTCC) のジオメトリを紹介します。
GEMC ネイティブのミラー光学系と、`gcad` 機能で読み込んだ CAD メッシュを組み合わせています。両方のシステムは
1 つの SQLite データベースに格納されます。

HTCC のジオメトリとデジタイズ処理は、`clas12-systems` 0.3 と GEMC 0.5、`pygemc` 0.5.0 の組み合わせで利用できます。

{% assign example = site.data.examples | where: "title", "HTCC" | first %}

<br/>

## クイックスタート

`clas12-systems` リポジトリで、ジオメトリデータベースをビルドし、短いシミュレーションを実行します。

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/htcc
./htcc.py
gemc htcc.yaml -n=1
```

<br/>

## ジオメトリ

下に示すジオメトリは `geometry_src/htcc/geometry.py` で定義され、その構築処理は
`geometry_src/htcc/htcc.py` によって制御されます。ネイティブビルダーは元の clas12Tags の perl スクリプト
(ガスボリューム、窓、48 枚の楕円ミラー、48 本の光電子増倍管) を移植したもので、3 つのビームラインコーンは
CAD メッシュとしてインポートされます。ネイティブのデータ行は %%htcc%% SQLite システムを使用し、メッシュのデータ行は
別の %%htcc_cad%% CAD システムを使用します。両者は同じデータベース、バリエーション、ランを共有するため、
1 つの `gemc.db` で検出器全体が読み込まれます。

ワールド (%%root%% という名前のボックス) には以下が含まれます。

- ポリコーンのブール演算で構築された %%htcc%% ガスボリュームと、%%htccEntryWindow%% および %%htccExitWindow%%
- ポリコーンのバレルから切り出され、%%htcc_AlMgF2%% 光学表面を設定して登録された
  48 個の楕円ミラーセグメント
- %%pmt_<ring>_sector<sector>_<half>%% という名前の光電子増倍管。各セクターを 2 つの半セクターに分けて読み出す
- %%htcc_AlMgF2%% ミラー用スキン表面を共有するウィンストンコーンの放物面シェル
- %%root%% の下に配置された CAD ビームラインコーン (%%htccCone%%、%%htccMollerCone%%、%%htccMollerConeExt%%)

インタラクティブビューア:

{% assign htcc_vtksz = "/home/assets/images/examples/htcc/htcc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ htcc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 HTCC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理リスト

HTCC はチェレンコフ検出器であるため、光学光子を生成して追跡する必要があります。YAML ファイルでは
`phys_list: FTFP_BERT + G4OpticalPhysics` により `FTFP_BERT + G4OpticalPhysics` を選択します。

{% include notes/physics-list-note.md %}

<br/>

## ジェネレーター

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

詳細については [内部ジェネレーターのドキュメント]( /home/documentation/generator/internal ) も参照してください。

<br/>

## デジタイズ処理

光電子増倍管は CLAS12 固有の %%htcc%% デジタイズプラグインを使用します。識別子にはセクター、ミラーのリング、
および光電子増倍管が読み出す半セクターが記録されます。

```python
pmt.digitization = "htcc"
pmt.set_identifier("sector", sector, "ring", ring, "half", hindex)
```

<br/>

## 使い方

### 検出器のビルド

`geometry_src/htcc/htcc.py` を使用して検出器をビルドします。このスクリプトは材料とミラー表面を定義し、
ネイティブの %%htcc%% ボリュームを登録するとともに、3 つのビームラインコーンを CAD メッシュとして
%%htcc_cad%% システムに登録します。デフォルトでは、両方のシステムが `gemc.db` という名前の SQLite ファイルに格納されます。

詳細については [ジオメトリのビルド]( /home/documentation/geometry/geometry_building ) も参照してください。

<br/>

### GEMC の実行

`htcc.yaml` ファイルを使ってこの構成で実行できます。インタラクティブに実行するには `-gui` を追加します。

```shell
gemc htcc.yaml -gui
```

必要に応じて `htcc.yaml` を変更します。特に、粒子の追加、スレッド数の制御、
出力の変更などを行えます。

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/htcc/gemc_view.png"
caption="CLAS12 HTCC simulation: generated electrons crossing the high-threshold Cherenkov counter geometry."
%}

<br/>

## 出力

%%gstreamer%% オプションで出力ファイル名と形式を選択します。

```yaml
gstreamer:
  - format: csv
    filename: htcc
  - format: hipo
    filename: htcc
```

詳細については [出力のドキュメント]( /home/documentation/output ) も参照してください。


## GEMC Analyzer でのプロット

まず 2,000 イベントで GEMC を実行します。デフォルトの YAML ファイルでは、アナライザー用の CSV ストリームが出力されます。

```shell
gemc htcc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

ヒットごとの総エネルギー付与量をプロットします。

```shell
gemc-analyzer htcc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![htcc のヒットごとの総エネルギー付与量][htcc-analyzer_totEdep]{:width="70%"}

[htcc-analyzer_totEdep]: /home/assets/images/examples/htcc/analyzer_totEdep.png

ヒット位置の y 座標を x 座標に対してプロットします。

```shell
gemc-analyzer htcc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![htcc のヒット位置の y 座標対 x 座標][htcc-analyzer_yvsx]{:width="70%"}

[htcc-analyzer_yvsx]: /home/assets/images/examples/htcc/analyzer_yvsx.png
