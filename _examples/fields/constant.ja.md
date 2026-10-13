---
layout: default
title: "Constant Field"
permalink: /examples/fields/constant.html
lang: ja
human_reviewed: false
---

# 一様磁場の例
<hr style="height:4px;border:0;background:#4a90e2;">

この磁場の例では、`gmultipoles` を使って縦方向に一様な磁場を表示します。イベントを実行することなく
磁力線の可視化を確認するための、最小限のシーンです。

{% assign example = site.data.examples | where: "title", "Constant Field" | first %}

<br/>

## クイックスタート

例をカレントディレクトリにコピーし、ジオメトリデータベースを構築して、磁場表示を開きます:

```shell
cp -r $GEMC_HOME/examples/fields/constant .
cd constant
./constant.py
gemc constant.yaml -gui
```

<br/>

## ジオメトリ

ジオメトリは `constant.py` で定義されています。ワールドボリューム %%root%% には、1 つの透明な
ボックス %%constant_field_box%% が含まれ、その %%mfield%% プロパティは %%constant%% に設定されています。

<br/>

## 磁場の定義

YAML ファイルは、`gmultipoles` を通じて縦方向の一様磁場を定義します:

```yaml
gmultipoles:
  - name: constant
    pole_number: 2
    strength: 1
    rotaxis: z
    longitudinal: true
```

表示オプションでは、30 本の磁力線と補助的なジオメトリのエッジを要求します:

```yaml
show_field_lines: 30
show_auxiliary_edges: true
```

<br/>

## 磁場表示

{% include figure.html
src="/assets/images/examples/constant/gemc_view.png"
caption="Constant field display: a transparent box with uniform field lines."
%}

<br/>

## 使い方

`constant.yaml` では `n: 0` が設定されているため、この表示シーンに `/run/beamOn` は不要です。
設定された磁場をある点で確認するには、`-fieldAt` を追加します:

```shell
gemc constant.yaml -fieldAt="0*cm 0*cm 0*cm"
```
