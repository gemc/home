---
layout: default
title: "Solenoid ASCII Field Map"
permalink: /examples/fields/solenoid.html
lang: ja
human_reviewed: false
---

# ソレノイド ASCII フィールドマップの例
<hr style="height:4px;border:0;background:#4a90e2;">

このフィールドの例では、`asciimap` フィールドプラグインを通じて読み込まれる円筒形の ASCII フィールドマップを
表示します。マップファイルは意図的に小さくしてあるため、例の確認や変更が簡単に行えます。

{% assign example = site.data.examples | where: "title", "Solenoid ASCII Field Map" | first %}

<br/>

## クイックスタート

この例を現在のディレクトリにコピーし、ジオメトリデータベースを構築して、フィールド表示を開きます。

```shell
cp -r $GEMC_HOME/examples/fields/solenoid .
cd solenoid
./solenoid.py
gemc solenoid.yaml -gui
```

<br/>

## ジオメトリ

ジオメトリは `solenoid.py` で定義されています。ワールドボリューム %%root%% には透明なチューブ
%%solenoid_field_tube%% が 1 つ含まれており、その %%mfield%% プロパティは %%solenoid%% に設定されています。

<br/>

## フィールドの定義

YAML ファイルは `solenoid_map.txt` を円筒 z 型の ASCII マップとして読み込みます。

```yaml
gfields:
  - name: solenoid
    type: asciimap
    symmetry: cylindrical-z
    map: solenoid_map.txt
    field_unit: T
    interpolation: linear
    coordinate1: "transverse,   4, 0*m, 3*m"
    coordinate2: "longitudinal, 7, -3*m, 3*m"
```

マップの最初の 2 列は %%transverse%% と %%longitudinal%% です。次の 2 列は、テスラ単位で表した
フィールドの横方向成分と縦方向成分です。

<br/>

## フィールド表示

{% include figure.html
src="/assets/images/examples/solenoid/gemc_view.png"
caption="Solenoid ASCII-map display: a transparent tube with field lines from a cylindrical map."
%}

<br/>

## 使い方

ファイル `solenoid.yaml` では `n: 0` が設定されているため、この表示シーンでは `/run/beamOn` は不要です。
設定したフィールドをある点で確認するには、`-fieldAt` を追加します。

```shell
gemc solenoid.yaml -fieldAt="1*m 0*m 0*m"
```
