---
layout: default
title: "Constant Field"
permalink: /examples/fields/constant.html
lang: zh
human_reviewed: false
---

# 恒定场示例
<hr style="height:4px;border:0;background:#4a90e2;">

本场示例使用 `gmultipoles` 展示一个均匀的纵向磁场。它是一个最简场景，用于在不运行事件的情况下检查
场线可视化效果。

{% assign example = site.data.examples | where: "title", "Constant Field" | first %}

<br/>

## 快速上手

将示例复制到当前目录，构建几何数据库，然后打开场显示：

```shell
cp -r $GEMC_HOME/examples/fields/constant .
cd constant
./constant.py
gemc constant.yaml -gui
```

<br/>

## 几何

几何在 `constant.py` 中定义。世界体 %%root%% 包含一个透明盒子 %%constant_field_box%%，其 %%mfield%%
属性被设置为 %%constant%%。

<br/>

## 场定义

该 YAML 文件通过 `gmultipoles` 定义了一个纵向均匀场：

```yaml
gmultipoles:
  - name: constant
    pole_number: 2
    strength: 1
    rotaxis: z
    longitudinal: true
```

显示选项请求绘制 30 条场线以及辅助几何边线：

```yaml
show_field_lines: 30
show_auxiliary_edges: true
```

<br/>

## 场显示

{% include figure.html
src="/assets/images/examples/constant/gemc_view.png"
caption="Constant field display: a transparent box with uniform field lines."
%}

<br/>

## 用法

文件 `constant.yaml` 设置了 `n: 0`，因此该显示场景无需 `/run/beamOn`。添加 `-fieldAt` 可以检查指定点处
所配置的场：

```shell
gemc constant.yaml -fieldAt="0*cm 0*cm 0*cm"
```
