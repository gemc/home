---
layout: default
title: "Dipole Field"
permalink: /examples/fields/dipole.html
lang: zh
human_reviewed: false
---

# 偶极场示例
<hr style="height:4px;border:0;background:#4a90e2;">

本场示例展示了来自 `gmultipoles` 的理想横向偶极场。它可用于检查单个体上的场关联，以及可视化的场线启动选项。

{% assign example = site.data.examples | where: "title", "Dipole Field" | first %}

<br/>

## 快速开始

将示例复制到当前目录，构建几何数据库，然后打开场显示：

```shell
cp -r $GEMC_HOME/examples/fields/dipole .
cd dipole
./dipole.py
gemc dipole.yaml -gui
```

<br/>

## 几何

几何在 `dipole.py` 中定义。世界体 %%root%% 包含一个透明盒子 %%dipole_field_box%%，其 %%mfield%% 属性设置为 %%dipole%%。

<br/>

## 场定义

该 YAML 文件定义了一个绕 z 轴滚转 30 度的 2 T 偶极场：

```yaml
gmultipoles:
  - name: dipole
    pole_number: 2
    strength: 2
    rotaxis: z
    rotation_angle: "30*deg"
```

显示选项请求 80 条场线以及辅助的几何边：

```yaml
show_field_lines: 80
show_auxiliary_edges: true
```

<br/>

## 场显示

{% include figure.html
src="/assets/images/examples/dipole/gemc_view.png"
caption="Dipole field display: a transparent field box with ideal transverse field lines."
%}

<br/>

## 用法

文件 `dipole.yaml` 设置了 `n: 0`，因此该显示场景不需要 `/run/beamOn`。添加 `-fieldAt` 可检查某点处配置的场：

```shell
gemc dipole.yaml -fieldAt="0*cm 0*cm 0*cm"
```
