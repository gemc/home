---
layout: default
title: "PyVista Geometry Visualization"
permalink: /examples/basic/pyvista.html
lang: zh
human_reviewed: false
---

# PyVista 几何可视化
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

GEMC 使用 [PyVista](https://docs.pyvista.org/) 在 Python 中直接可视化探测器几何。
几何可以交互式查看、导出为 `.vtksz` 文件以用于网页展示，或渲染为截图。
完整的 API 参考请参见 [PyVista API 文档](/home/documentation/api/pyvista_api)。

<br/>

## 快速开始

将示例复制到当前目录：

```shell
cp -r $GEMC_HOME/examples/basic/pyvista .
cd pyvista
./gemc_pyvista.py
```

交互式预览几何（会打开一个 PyVista 窗口）：

```shell
./gemc_pyvista.py -pv
```

<br/>

## 几何

该示例在 `pyvista_basic_shapes.py` 中定义了四个几何体：一个透明的容器盒、
一个实心圆柱体、一个球体，以及容器内一个经过旋转的小盒子。

交互式查看器：

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/pyvista/pyvista.vtksz"
  title="Interactive VTK.js view of the pyvista geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 用法

### 构建几何

```shell
./gemc_pyvista.py
```

{% include notes/python-api-note.md %}

<br/>

### 运行 GEMC

```shell
gemc pyvista.yaml -n=10
```

添加 `-gui` 可交互式运行。
