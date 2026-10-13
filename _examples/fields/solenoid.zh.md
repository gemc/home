---
layout: default
title: "Solenoid ASCII Field Map"
permalink: /examples/fields/solenoid.html
lang: zh
human_reviewed: false
---

# 螺线管 ASCII 场图示例
<hr style="height:4px;border:0;background:#4a90e2;">

本场示例展示了一张通过 `asciimap` 场插件加载的圆柱形 ASCII 场图。
该场图文件刻意保持小巧，因此本示例易于查看和修改。

{% assign example = site.data.examples | where: "title", "Solenoid ASCII Field Map" | first %}

<br/>

## 快速开始

将示例复制到当前目录，构建几何数据库，然后打开场显示：

```shell
cp -r $GEMC_HOME/examples/fields/solenoid .
cd solenoid
./solenoid.py
gemc solenoid.yaml -gui
```

<br/>

## 几何

几何在 `solenoid.py` 中定义。世界体 %%root%% 包含一个透明管体
%%solenoid_field_tube%%，其 %%mfield%% 属性设置为 %%solenoid%%。

<br/>

## 场定义

该 YAML 文件将 `solenoid_map.txt` 作为圆柱 z 型 ASCII 场图加载：

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

场图的前两列是 %%transverse%% 和 %%longitudinal%%。接下来的两列是以特斯拉为单位的横向和纵向场分量。

<br/>

## 场显示

{% include figure.html
src="/assets/images/examples/solenoid/gemc_view.png"
caption="Solenoid ASCII-map display: a transparent tube with field lines from a cylindrical map."
%}

<br/>

## 用法

文件 `solenoid.yaml` 设置了 `n: 0`，因此此显示场景无需 `/run/beamOn`。添加
`-fieldAt` 可查看某一点处配置的场：

```shell
gemc solenoid.yaml -fieldAt="1*m 0*m 0*m"
```
