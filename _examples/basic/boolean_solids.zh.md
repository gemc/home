---
layout: default
title: "Boolean Solids"
permalink: /examples/basic/boolean_solids.html
lang: zh
human_reviewed: false
---

# 布尔实体示例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

本示例演示 GEMC 的布尔实体运算。它利用未放置的组件几何体构建三个已放置的实体：
一块通过差集运算得到的带孔板、一个通过并集运算得到的十字形实体，以及一个
通过对两个球体取交集得到的透镜形实体。

<br/>

## 快速开始

将示例复制到当前目录。
要创建几何模型并运行 10 个事件，请执行：

```shell
cp -r $GEMC_HOME/examples/basic/boolean_solids .
cd boolean_solids
./boolean_solids.py
gemc boolean_solids.yaml -n=10
```

<br/>

## 几何

几何模型在 `boolean_solids.py` 中定义。

世界体（一个名为 %%root%% 的盒形体）包含三个可见的布尔几何体：

| 几何体 | 运算 | 组件 |
|--------|-----------|------------|
| %%plate_with_hole%% | 差集 | %%plate_box - plate_hole%% |
| %%cross%% | 并集 | %%bar + bar_rotated%% |
| %%lens%% | 交集 | %%sphere_one * sphere_two%% |

组件几何体使用特殊材料 %%Component%%。它们定义布尔表达式的操作数，
但不会作为可见的探测器几何体放置。生成的布尔几何体与其他 `GVolume` 一样
进行放置，并具有各自的材料、颜色、位置和旋转。

交互式查看器：

{% assign boolean_solids_vtksz = "/assets/images/examples/boolean_solids/boolean_solids.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ boolean_solids_vtksz }}"
  title="Interactive VTK.js view of the boolean solids geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 布尔表达式

通过为 %%solidsOpr%% 赋值来指定布尔实体：

```python
plate.solidsOpr = 'plate_box - plate_hole'
cross.solidsOpr = 'bar + bar_rotated'
lens.solidsOpr = 'sphere_one * sphere_two'
```

第一个操作数以自身原点为基准进行求值。第二个操作数使用自身相对于
第一个操作数的位置和旋转。例如，%%plate_hole%% 在从 %%plate_box%% 中减去之前
先偏移 30 mm，因此孔洞不在板的中心。

<br/>

## 生成器

粒子的运动学参数在 YAML 文件中定义：

```yaml
gparticle:
  - name: e-
    p: 500*MeV
    theta: 90*deg
    vx: -40*cm
    delta_vx: 12*cm
    randomVertexModel: uniform
```

更多信息请参阅[内部生成器文档]( /home/documentation/generator/internal )。

<br/>

## 用法

### 构建探测器

使用 Python 脚本 `boolean_solids.py` 构建探测器。默认情况下，探测器配置存储在
名为 `gemc.db` 的 SQLite 文件中。

```shell
./boolean_solids.py
```

更多信息请参阅[构建几何模型]( /home/documentation/geometry/geometry_building )。

<br/>

### 运行 GEMC

可以使用文件 `boolean_solids.yaml` 运行该配置。添加 `-gui` 可交互式运行：

```shell
gemc boolean_solids.yaml -gui
```

<br/>

## 运行事件

{% include figure.html
src="/assets/images/examples/boolean_solids/gemc_view.png"
caption="Boolean solids simulation: electrons crossing the subtraction, union, and intersection volumes."
%}
