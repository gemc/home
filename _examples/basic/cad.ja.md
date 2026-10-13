---
layout: default
title: "CAD example"
permalink: /examples/basic/cad.html
lang: ja
human_reviewed: false
---

# CAD の例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

この例では、GEMC CAD ファクトリを使って 3 つの STL 臓器メッシュをインポートし、医療用の小線源治療を
モデル化します。**イリジウム192** の高線量率（HDR）線源を*肝臓内部*に配置し、光子を等方的に放出させます。
各臓器は %%flux%% 有感検出器であるため、臓器ごとに付与されたエネルギーが記録されます。
`plot_dose.py` がそれを吸収線量と、それに相当する Ir-192 の照射時間に変換します。

<br/>

## クイックスタート

この例を現在のディレクトリにコピーします。CAD 定義をアップロードし、200 イベントを実行して CSV 出力を
生成し、各臓器の線量をプロットするには、次のようにします。

```shell
cp -r $GEMC_HOME/examples/basic/cad .
cd cad
./cad.py
gemc cad.yaml -n=200
./plot_dose.py
```

<br/>

## ジオメトリ

ジオメトリは `stls/cad__default.yaml` に宣言的に定義され、`cad.py` によって `gemc.db` にアップロード
されます。

%%stls%% という名前の CAD システムには、次が含まれます。

- %%heart_NIH3D%%：材質を血液とした心臓メッシュ。
- %%respiratory_NIH3D%%：材質を %%G4_LUNG_ICRP%% とした半透明の肺メッシュ。
- %%liver_NIH3D%%：材質を軟組織とした肝臓メッシュ。

`stls/cad__default.yaml` の各エントリは、メッシュファイル、材質、色、スケール、位置、および識別子を
設定します。%%system%% の値は、`cad.yaml` の `gsystem` 名と、STL ファイルを含むディレクトリの両方に
一致していなければなりません。3 つの臓器は y 軸上に中心を置き（各重心は `x = z = 0`）、y 方向に並んで
います。また、気管が下を向くように作成された肺メッシュには、上下を正しい向きにするため、z 軸まわりに
180° の `rotation` が設定されています。

詳しくは [CAD インポートのドキュメント](/home/documentation/geometry/cad_imports) も参照してください。

インタラクティブビューア：

<iframe
  src="/home/assets/vtkjs-viewer.html?fileURL=/home/assets/images/examples/cad/cad.vtksz"
  title="Interactive VTK.js view of the CAD organ geometry"
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

粒子の運動学的条件は YAML ファイル内で定義されます。

```yaml
gparticle:
  - name: gamma
    p: 380*keV
    delta_p: 120*keV
    multiplicity: 300
    theta: 90*deg
    delta_theta: 90*deg
    randomThetaModel: cosine
    phi: 180*deg
    delta_phi: 180*deg
    vx: 0*mm
    vy: -140*mm
    vz: 0*mm
    delta_vx: 20*mm
    delta_vy: 20*mm
    delta_vz: 20*mm
    randomVertexModel: sphere
```

これは、肝臓内に配置された臨床用の **イリジウム192 HDR 小線源治療線源**をモデル化しています。

- **エネルギー** — Ir-192 は線スペクトルを放出します（主要なスペクトル線は 0.30〜0.61 MeV）。ここでは、
  平均光子エネルギーである約 0.38 MeV の光子で近似し、`delta_p` でエネルギーに幅を持たせて
  スペクトルの範囲をカバーしています。
- **位置** — 生成位置の中心は、ワールド座標での肝臓の重心 `(0, -140, 0) mm` です。線源の滞留領域を
  模擬するため、生成位置を半径約 35 mm の球内に一様に分布させます（`randomVertexModel: sphere` は
  `|delta_v|` を半径として使用します）。臓器は y 軸に沿って（`x = z = 0`）並んでおり、心臓が原点に、
  肝臓はそのすぐ下に、肺はその上にあります。
- **方向** — 全立体角 4π への等方的な放出：θ を 0〜180° の範囲で `cosine` に従ってサンプリングし、
  φ を 0〜360° の範囲で一様にサンプリングして組み合わせます。

詳しくは [内部ジェネレータのドキュメント](/home/documentation/generator/internal) も参照してください。

<br/>

## デジタイズ

各臓器は、`stls/cad__default.yaml` で %%flux%% 有感検出器として設定されています。

```yaml
defaults:
  digitization: flux

volumes:
  - name: heart_NIH3D
    identifier: "organ: 1"
```

%%flux%% デジタイズは**イベントモード**の検出器です。ヒットごとに 1 行を出力し、各行には臓器の
%%identifier%% と付与エネルギー %%totEdep%% が含まれます。これにより、1 回の実行で 3 つの臓器を
個別に区別できます。

> 組み込みの %%dosimeter%% デジタイズでも線量を計算できますが、これは**ランモード**の検出器であり、
> 同じ有感検出器名を共有するすべてのヒットを合算して 1 つのレコードに記録します。3 つの臓器すべてが
> `dosimeter` という同じ名前を共有するため、それらは 1 つの数値に集約されてしまいます。%%flux%% を
> 使用することで、すべてのヒットに臓器ごとの識別情報が保持されます。

### 吸収線量

`plot_dose.py` は、臓器ごとに付与エネルギーを合計し、臓器の質量で割って吸収線量を求めます。

$$
D_{\text{organ}} = \frac{\sum_i \mathrm{totEdep}_i}{m_{\text{organ}}},
\qquad
m_{\text{organ}} = \rho \, V_{\text{mesh}}
$$

ここで、総和はその臓器のすべてのヒットについて取ります。\\(\rho\\) は割り当てられた材質の密度
（`gemc cad.yaml -printSystemsMaterials` は、血液、肺、軟組織の各材質についてそれぞれ 1.06、1.04、
1.03 g/cm³ を報告します）、\\(V_{\text{mesh}}\\) は CAD メッシュの体積（元の符号付き体積 ×
一様な `scale`³）です。1 グレイは 1 キログラムあたり 1 ジュール、\\(1\,\mathrm{Gy} = 1\,\mathrm{J/kg}\\)
です。

### 照射時間

シミュレーションは一定数の光子を放出します。対応する**実際の照射時間**は、放射能 \\(A\\) の Ir-192 線源が
それだけの数の光子を放出するのに必要な時間です。光子収率 \\(Y\\)（1 崩壊あたりの光子数）のとき、線源は
1 秒あたり \\(R = A\,Y\\) 個の光子を放出するため、シミュレートされた光子数
\\(N_\gamma = N_{\text{events}} \times m\\)（多重度 \\(m\\)）に対して、次が成り立ちます。

$$
R = A \, Y,
\qquad
t_{\text{rad}} = \frac{N_\gamma}{A \, Y}
$$

`plot_dose.py` はデフォルトで、公称放射能 \\(A = 10\ \mathrm{Ci} = 3.7\times10^{11}\\) Bq の HDR 線源と、
Ir-192 の 1 崩壊あたり \\(Y = 2.3\\) 個の光子収率（ガンマ線の各スペクトル線の強度の総和）を使用します。
両者はそれぞれ `--activity` と `--yield` で調整できます。線量と \\(t_{\text{rad}}\\) はどちらも
\\(N_\gamma\\) に比例するため、単位治療時間あたりの吸収線量（線量率）は
\\(D_{\text{organ}} / t_{\text{rad}}\\) となり、光子数（同等に、線源の滞留時間）を増やすことで
治療に必要な線量に到達します。

詳しくは [線量計のドキュメント](/home/documentation/sensitivity/dosimeter) を参照してください。

<br/>

## 使い方

### 検出器の構築

Python スクリプト `cad.py` を使って CAD 定義をアップロードします。このスクリプトは
`stls/cad__default.yaml` を読み込み、設定を `gemc.db` という名前の SQLite ファイルに保存します。

```shell
./cad.py
```

{% include notes/python-api-note.md %}

詳しくは [ジオメトリの構築](/home/documentation/geometry/geometry_building) も参照してください。

<br/>

### GEMC の実行

`cad.yaml` ファイルを使ってこの設定で実行できます。インタラクティブに実行するには `-gui` を追加します。

```shell
gemc cad.yaml -gui
```

必要に応じて `cad.yaml` を変更してください。特に、粒子の追加、スレッド数の制御、出力の変更などを
行えます。

<br/>

## イベントの実行

{% include figure.html
src="/assets/images/examples/cad/gemc_view.png"
caption="CAD simulation: an Iridium-192 brachytherapy source inside the liver emits photons
isotropically, depositing dose in the imported liver, heart, and lung meshes."
%}

<br/>

## 出力

%%gstreamer%% オプションで出力ファイル名と形式を選択します。

```yaml
gstreamer:
  - format: csv
    filename: organs
```

{% include notes/output-note.md %}

詳しくは [出力のドキュメント](/home/documentation/output) も参照してください。

<br/>

## 各臓器の線量のプロット

まず GEMC を実行して flux の CSV ストリームを出力します（イベント数が多いほど、リスク臓器の
統計精度が向上します）。

```shell
gemc cad.yaml -n=200
```

次に `plot_dose.py` で臓器ごとの線量をプロットします。このスクリプトは `organs_t0_digitized.csv` を
読み込み、臓器ごとの付与エネルギー、質量、線量を表示し、棒グラフを描画します。

```shell
./plot_dose.py                       # nominal 10 Ci Ir-192 source
./plot_dose.py --activity 5          # a weaker 5 Ci source (rescales the irradiation time)
./plot_dose.py --save organs_dose.png
```

![CAD の臓器ごとの線量][cad-dose_per_organ]{:width="70%"}

線源が配置された肝臓の吸収線量が圧倒的に大きくなります。そのすぐ上の心臓と最上部の肺が散乱線から受ける
線量は、はるかに小さくなります。このように線量が局所に集中することが、小線源治療の利点です。タイトルには、
シミュレートされた光子数に相当する Ir-192 の照射時間が示されます（上記の [照射時間](#irradiation-time)
を参照）。

[cad-dose_per_organ]: /home/assets/images/examples/cad/dose_per_organ.png


## GEMC アナライザでのプロット

まず GEMC で 200 イベントを実行します。デフォルトの YAML ファイルの設定により、アナライザ用の
CSV ストリームが出力されます。

```shell
gemc cad.yaml -n=200
```

ヒットごとの総付与エネルギーをプロットします。

```shell
gemc-analyzer organs_t0_digitized.csv totEdep --kind csv
```

![CAD のヒットごとの総付与エネルギー][cad-analyzer_totEdep]{:width="70%"}

[cad-analyzer_totEdep]: /home/assets/images/examples/cad/analyzer_totEdep.png
