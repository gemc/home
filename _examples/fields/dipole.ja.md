---
layout: default
title: "Dipole Field"
permalink: /examples/fields/dipole.html
lang: ja
human_reviewed: false
---

# ダイポール磁場の例
<hr style="height:4px;border:0;background:#4a90e2;">

この磁場の例では、`gmultipoles` による理想的な横方向ダイポール磁場を表示します。単一ボリュームへの
磁場の関連付けや、磁力線表示の起動オプションを視覚的に確認するのに役立ちます。

{% assign example = site.data.examples | where: "title", "Dipole Field" | first %}

<br/>

## クイックスタート

この例をカレントディレクトリにコピーし、ジオメトリデータベースをビルドして、磁場表示を開きます。

```shell
cp -r $GEMC_HOME/examples/fields/dipole .
cd dipole
./dipole.py
gemc dipole.yaml -gui
```

<br/>

## ジオメトリ

ジオメトリは `dipole.py` で定義されています。ワールドボリューム %%root%% には、1 つの透明なボックス
%%dipole_field_box%% が含まれており、その %%mfield%% プロパティは %%dipole%% に設定されています。

<br/>

## 磁場の定義

この YAML ファイルでは、z 軸まわりに 30 度回転させた 2 T のダイポールを定義しています。

```yaml
gmultipoles:
  - name: dipole
    pole_number: 2
    strength: 2
    rotaxis: z
    rotation_angle: "30*deg"
```

表示オプションでは、80 本の磁力線と補助的なジオメトリのエッジを要求しています。

```yaml
show_field_lines: 80
show_auxiliary_edges: true
```

<br/>

## 磁場の表示

{% include figure.html
src="/assets/images/examples/dipole/gemc_view.png"
caption="Dipole field display: a transparent field box with ideal transverse field lines."
%}

<br/>

## 使い方

ファイル `dipole.yaml` では `n: 0` が設定されているため、この表示シーンでは `/run/beamOn` は不要です。
設定された磁場をある点で確認するには、`-fieldAt` を追加します。

```shell
gemc dipole.yaml -fieldAt="0*cm 0*cm 0*cm"
```
