---
layout: default
title: "CLAS12 LTCC"
permalink: /examples/clas12/ltcc.html
lang: ja
human_reviewed: false
---

# CLAS12 低閾値チェレンコフカウンターの例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、`clas12-systems` に含まれる CLAS12 低閾値チェレンコフカウンター（LTCC）のジオメトリを示します。
GEMC ネイティブのミラー光学系と、`gcad` 機能で読み込む CAD メッシュを組み合わせています。両方のシステムは
1 つの SQLite データベースに格納されます。

LTCC のジオメトリとデジタイゼーションは、`clas12-systems` 0.3 で、GEMC 0.5 および `pygemc` 0.5.0 と
組み合わせて利用できます。

{% assign example = site.data.examples | where: "title", "LTCC" | first %}

<br/>

## クイックスタート

`clas12-systems` リポジトリで、ジオメトリデータベースを構築し、短いシミュレーションを実行します：

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ltcc
./ltcc.py
gemc ltcc.yaml -n=1
```

<br/>

## ジオメトリ

以下に示すジオメトリは `geometry_src/ltcc/geometry.py` で定義され、構築処理は
`geometry_src/ltcc/ltcc.py` によって統括されます。ネイティブのビルダーは、元の clas12Tags の Perl スクリプト
（ミラー形状、PMT、鉄シールド）を移植したもので、反射型ウィンストンコーンと機械構造のフレームは CAD
メッシュとしてインポートされます。ネイティブのレコードは %%ltcc%% SQLite システムを使用し、メッシュのレコードは
別の %%ltcc_cad%% CAD システムを使用します。両者は同じデータベース、バリエーション、ランを共有するため、
1 つの `gemc.db` で検出器全体を読み込めます。

ワールド（%%root%% という名前のボックス）には、6 つのセクターそれぞれについて次のものが含まれます：

- そのセクターの光学系を収める、%%ltccS<sector>%% という名前のガスのくさび形母体ボリューム
- %%ltcc_AlMgF2%% 光学表面を指定して登録された、円筒面、双曲面、楕円面のミラーセグメント
- 各セグメントの左右で読み出しを行う、%%pmt_s<sector><side>_<n>%% という名前の光電子増倍管
- ウィンストンコーンの外面を覆う 5 mm の鉄シールド
- %%copyOf%% 配置として再利用される CAD ウィンストンコーン（%%WC_S%%、%%WC_M%%、%%WC_L%%）とフレームメッシュ

インタラクティブビューア：

{% assign ltcc_vtksz = "/home/assets/images/examples/ltcc/ltcc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ltcc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 LTCC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理リスト

LTCC はチェレンコフ検出器であるため、光学光子を生成して追跡する必要があります。YAML ファイルでは
`phys_list: FTFP_BERT + G4OpticalPhysics` により `FTFP_BERT + G4OpticalPhysics` を選択します。

{% include notes/physics-list-note.md %}

<br/>

## ジェネレーター

粒子の運動学的パラメーターは YAML ファイルで定義されます：

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

## デジタイゼーション

光電子増倍管は CLAS12 固有の %%ltcc%% デジタイゼーションプラグインを使用します。識別子には、セクター、
PMT の左右の区別、およびその光電子増倍管が読み出すミラーセグメントが記録されます：

```python
pmt.digitization = "ltcc"
pmt.set_identifier("sector", sector, "side", side_id, "segment", n)
```

<br/>

## 使い方

### 検出器の構築

`geometry_src/ltcc/ltcc.py` を使って検出器を構築します。このスクリプトは、材料とミラー表面を定義し、
ネイティブの %%ltcc%% ボリュームを登録し、`stls/cad__default.yaml` から %%ltcc_cad%% システム用の CAD 定義を
アップロードして、CAD の `copyOf` 配置を追加します。デフォルトでは、両方のシステムは
`gemc.db` という名前の SQLite ファイルに格納されます。

詳細については [ジオメトリの構築]( /home/documentation/geometry/geometry_building ) も参照してください。

<br/>

### GEMC の実行

この構成での実行には `ltcc.yaml` ファイルを使用できます。インタラクティブに実行するには `-gui` を追加します：

```shell
gemc ltcc.yaml -gui
```

必要に応じて `ltcc.yaml` を変更してください。特に、粒子の追加、スレッド数の制御、
出力の変更などを行えます。

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/ltcc/gemc_view.png"
caption="CLAS12 LTCC simulation: generated electrons crossing the low-threshold Cherenkov counter geometry."
%}

<br/>

## 出力

%%gstreamer%% オプションで出力のファイル名と形式を選択します：

```yaml
gstreamer:
  - format: csv
    filename: ltcc
  - format: hipo
    filename: ltcc
```

詳細については [出力のドキュメント]( /home/documentation/output ) も参照してください。


## GEMC アナライザーによるプロット

まず GEMC で 2,000 イベントを実行します。デフォルトの YAML ファイルでは、アナライザー用の CSV ストリームが
出力されます。

```shell
gemc ltcc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

ヒットごとの総エネルギー付与をプロットします：

```shell
gemc-analyzer ltcc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![ltcc のヒットごとの総エネルギー付与][ltcc-analyzer_totEdep]{:width="70%"}

[ltcc-analyzer_totEdep]: /home/assets/images/examples/ltcc/analyzer_totEdep.png

ヒット位置の y 対 x をプロットします：

```shell
gemc-analyzer ltcc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![ltcc のヒット位置の y 対 x][ltcc-analyzer_yvsx]{:width="70%"}

[ltcc-analyzer_yvsx]: /home/assets/images/examples/ltcc/analyzer_yvsx.png
