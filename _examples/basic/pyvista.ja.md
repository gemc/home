---
layout: default
title: "PyVista Geometry Visualization"
permalink: /examples/basic/pyvista.html
lang: ja
human_reviewed: false
---

# PyVista ジオメトリの可視化
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

GEMC は [PyVista](https://docs.pyvista.org/) を使用して、Python から直接検出器ジオメトリを可視化します。
ジオメトリはインタラクティブに表示したり、Web 表示用に `.vtksz` ファイルとしてエクスポートしたり、
スクリーンショットとしてレンダリングしたりできます。完全な API リファレンスについては、
[PyVista API ドキュメント](/home/documentation/api/pyvista_api) を参照してください。

<br/>

## クイックスタート

サンプルをカレントディレクトリにコピーします:

```shell
cp -r $GEMC_HOME/examples/basic/pyvista .
cd pyvista
./gemc_pyvista.py
```

ジオメトリをインタラクティブにプレビューするには（PyVista ウィンドウが開きます）:

```shell
./gemc_pyvista.py -pv
```

<br/>

## ジオメトリ

このサンプルでは `pyvista_basic_shapes.py` で 4 つのボリュームを定義しています: 透明なコンテナボックス、
中実の円柱、球、およびコンテナ内部に角度を付けて配置した小さなボックスです。

インタラクティブビューア:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/pyvista/pyvista.vtksz"
  title="Interactive VTK.js view of the pyvista geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 使い方

### ジオメトリの構築

```shell
./gemc_pyvista.py
```

{% include notes/python-api-note.md %}

<br/>

### GEMC の実行

```shell
gemc pyvista.yaml -n=10
```

インタラクティブに実行するには `-gui` を追加します。
