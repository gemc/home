---
layout: default
title: "CLAS12 DC"
permalink: /examples/clas12/dc.html
lang: zh
human_reviewed: false
---

# CLAS12 漂移室示例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

本示例展示来自 `clas12-systems` 的 CLAS12 漂移室几何。

{% assign example = site.data.examples | where: "title", "DC" | first %}

<br/>

## 快速开始

在 `clas12-systems` 仓库中，构建几何数据库并运行一次简短的模拟：

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/dc
./dc.py
gemc dc.yaml -n=1
```

<br/>

## 几何

下图所示的几何定义于 `geometry_src/dc/dc.py` 和 `geometry_src/dc/geometry.py` 中。
DC 构建器读取本地 coatjava 几何工厂，将 CLAS12 漂移室的区域和
超层转换为 GEMC 几何体，并将它们存储在 `gemc.db` 中。

世界体积（一个名为 %%root%% 的长方体）包含：

- 六个扇区的区域母体积，命名为 %%region1_s1%% 至 %%region3_s6%%
- 六个扇区的超层体积，命名为 %%sl1_s1%% 至 %%sl6_s6%%

交互式查看器：

{% assign dc_vtksz = "/home/assets/images/examples/dc/dc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ dc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 DC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理过程列表

默认使用 `FTFP_BERT`，在 YAML 文件中通过 `phys_list: FTFP_BERT` 选择。

{% include notes/physics-list-note.md %}

<br/>

## 粒子发生器

粒子的运动学参数在 YAML 文件中定义：

```yaml
gparticle:
  - name: e-
    p: 5000*MeV
    delta_p: 1*GeV
    theta: 25*deg
    delta_theta: 15*deg
    randomThetaModel: cosine
    delta_phi: 180*deg
```

更多信息另见[内部发生器文档]( /home/documentation/generator/internal )。

<br/>

## 数字化

超层的灵敏探测设置使用 CLAS12 专用的 %%dc%% 数字化插件。标识符记录扇区、
超层、层和丝的编号：

```python
gvolume.digitization = "dc"
gvolume.set_identifier("sector", sector, "superlayer", superlayer, "layer", 1, "wire", 1)
```

<br/>

## 用法

### 构建探测器

使用 `geometry_src/dc/dc.py` 构建探测器。默认情况下，该配置存储在名为
`gemc.db` 的 SQLite 文件中。

更多信息另见[构建几何]( /home/documentation/geometry/geometry_building )。

<br/>

### 运行 GEMC

文件 `dc.yaml` 可用于运行该配置。添加 `-gui` 以交互方式运行：

```shell
gemc dc.yaml -gui
```

可根据需要修改 `dc.yaml`，特别是添加粒子、控制线程数量或更改输出。

<br/>

## 运行事例

{% include figure.html
src="/assets/images/examples/dc/gemc_view.png"
caption="CLAS12 DC simulation: generated electrons crossing the drift chamber geometry."
%}

<br/>

## 输出

%%gstreamer%% 选项用于选择输出文件名和格式：

```yaml
gstreamer:
  - format: csv
    filename: dc
  - format: hipo
    filename: dc
```

更多信息另见[输出文档]( /home/documentation/output )。


## 使用 GEMC 分析器绘图

先运行 GEMC 模拟 2,000 个事例。默认 YAML 文件会写出分析器所需的 CSV 数据流。

```shell
gemc dc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

绘制每次击中的总能量沉积：

```shell
gemc-analyzer dc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![dc 每次击中的总能量沉积][dc-analyzer_totEdep]{:width="70%"}

[dc-analyzer_totEdep]: /home/assets/images/examples/dc/analyzer_totEdep.png

绘制击中位置的 y 与 x 关系图：

```shell
gemc-analyzer dc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![dc 击中位置的 y 与 x 关系图][dc-analyzer_yvsx]{:width="70%"}

[dc-analyzer_yvsx]: /home/assets/images/examples/dc/analyzer_yvsx.png

绘制数字化后的 TDC 时间：

```shell
gemc-analyzer dc_t0_digitized.csv TDC_TDC --kind csv
```

![dc 数字化后的 TDC 时间][dc-analyzer_tdc]{:width="70%"}

[dc-analyzer_tdc]: /home/assets/images/examples/dc/analyzer_tdc.png
