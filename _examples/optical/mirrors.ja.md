---
layout: default
title: "Mirrors"
permalink: /examples/optical/mirrors.html
lang: ja
human_reviewed: false
---

# ミラーの例
<hr style="height:4px;border:0;background:#4a90e2;">

この例では、GEMC の光学サーフェス（「ミラー」）を紹介します。3 個の同一の 1 GeV 電子が低屈折率
のガスラジエーターを通過し、それぞれが反射板の中心を狙って進みます。チェレンコフ光子は各電子の
周囲の狭い前方コーン内にとどまり、その電子の反射板に到達します。各反射板は、それぞれ異なるミラー
定義を示します。

* %%polished_metal%% - 明示的な反射率テーブルを持つ `dielectric_metal` / `polished` /
  `unified` のスキンサーフェス：典型的な金属コートミラー。
* %%rough_metal%% - `ground` 仕上げを使った同じスキンサーフェス：反射は鏡面ローブ
  （%%specularlobe%% = 1）に入り、そのぼけは %%sigmaAlpha%% で設定されます。
* %%semi_transparent%% - ラジエーターとその反射板の間の**ボーダーサーフェス**として定義された
  ハーフミラー：光子の 60% が反射され、30% が反射板を透過し（%%transmittance%%）、10% が吸収
  されます。

各反射板は、その光子を自身の上流にある光子検出パネルへ反射して戻します（%%gPhotonDetector%%
のデジタイゼーションを使用し、そのミラーの色で描画されます）。そのため、各パネルは同一の条件を
見ており、違いは反射のみです。4 番目のパネルは、半透明板の背後にある大きなギャップを横切った後の
透過光子を数えます。典型的な相対光子数（flat パネル = 1）：

| パネル | サーフェス | 相対カウント |
|---|---|---|
| flat (gold) | polished, R = 0.90 | 1.00 |
| rough (tomato) | specular lobe, sigmaAlpha = 0.03 | 約 0.99（ぼけた像、わずかな漏れ） |
| semi (blue) | reflected, R = 0.60 | 約 0.69（= 0.60 / 0.90） |
| behind (blue) | transmitted, T = 0.30 | 約 0.37（= 0.30 / 0.90） |

<br/>

## クイックスタート

この例をカレントディレクトリにコピーします。
ジオメトリを作成し、10 イベントを実行して、CSV 出力ファイルを生成するには、次を実行します。

```shell
cp -r $GEMC_HOME/examples/optical/mirrors .
cd mirrors
./mirrors.py
gemc mirrors.yaml -n=10
```

<br/>

## ジオメトリ

ジオメトリは `mirrors.py` で定義されています。ワールドボリューム %%root%% には、1 m^3 のガス
ラジエーター（%%radiatorGas%%、屈折率が約 1.001 のデモ用ガス）が含まれます。ラジエーターの
内部には、次のものがあります。

* ラジエーター中央部にある 3 枚の薄い板：スキンミラーを担う 2 枚のアルミニウム板と、
  半透明板 - 透過した光子が妨げられずに進み続けるようにラジエーターガスで作られています -
  これは %%semi_transparent%% ボーダーサーフェスの対象となります。
* 3 枚の上流光子検出パネル。各パネルは 1 枚の板と位置を合わせ、そのミラーの色で描画され、
  その板が反射した光子を収集します。
* 半透明板の背後にある長い透過ギャップ。光学真空（屈折率 1）で満たされているため、電子は
  ギャップ内でチェレンコフ光を放射せず、透過光子がギャップを横切る様子を見ることができます。
* ギャップの端にある 4 番目のパネル。透過光子を収集します。

インタラクティブビューア：

{% assign mirrors_vtk = "/assets/images/examples/mirrors/mirrors.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ mirrors_vtk }}"
  title="Interactive VTK.js view of the mirrors geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="/assets/images/examples/mirrors/gemc_view.png"
caption="Mirrors simulation with 1 generated event."
%}

<br/>

## ミラー定義

各ミラーは、ジオメトリと一緒に公開される `GMirror` です。

```python
polished = GMirror("polished_metal")
polished.type = "dielectric_metal"
polished.finish = "polished"
polished.model = "unified"
polished.border = "SkinSurface"
polished.photonEnergy = "2.0*eV 3.0*eV 4.0*eV 5.0*eV 6.0*eV"
polished.reflectivity = "0.90 0.90 0.89 0.88 0.87"
polished.publish(cfg)
```

そしてボリュームは名前でミラーを参照します。

```python
plate.mirror = "polished_metal"
```

フィールドの完全なリファレンスについては、[ミラーのドキュメント](/home/documentation/optical/mirrors)
を参照してください。

<br/>

## 物理

ステアリングカードは光学物理を有効にします。

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics
```

この例を実行すると、GEMC が作成したサーフェスが出力されます。

```text
G4World: created optical surface <mirrors/polished_metal> type <dielectric_metal>,
finish <polished>, model <unified>
G4World: created 3 optical surfaces, attached to 2 skin and 1 border logical surfaces
```


## GEMC Analyzer によるプロット

まず GEMC を 10 イベントで実行します。デフォルトの YAML ファイルが analyzer の CSV ストリームを
書き出します。

```shell
gemc mirrors.yaml -n=10
```

### パネルごとの y vs x

以下のプロットは、光学光子のヒット位置を %%panel%% ごとに分割したものです。背後の透過パネルは、
半透明の反射パネルのプロットに統合せず、独立したプロットとして示しています。各画像に表示される
カウントは、真情報ストリームから選択された行数です。

| | |
|:---:|:---:|
| ![flat panel y vs x][mirrors-flat-panel-yvsx] | ![rough panel y vs x][mirrors-rough-panel-yvsx] |
| flat 反射パネル<br>counts = 2,445 | rough 反射パネル<br>counts = 2,269 |
| ![semi panel y vs x][mirrors-semi-panel-yvsx] | ![back panel y vs x][mirrors-back-panel-yvsx] |
| 半透明反射パネル<br>counts = 1,681 | 背後の透過パネル<br>counts = 918 |

[mirrors-flat-panel-yvsx]: /home/assets/images/examples/mirrors/flat_panel_y_vs_x.png
[mirrors-rough-panel-yvsx]: /home/assets/images/examples/mirrors/rough_panel_y_vs_x.png
[mirrors-semi-panel-yvsx]: /home/assets/images/examples/mirrors/semi_panel_y_vs_x.png
[mirrors-back-panel-yvsx]: /home/assets/images/examples/mirrors/back_panel_y_vs_x.png
