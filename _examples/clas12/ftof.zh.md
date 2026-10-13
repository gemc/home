---
layout: default
title: "CLAS12 FTOF"
permalink: /examples/clas12/ftof.html
lang: zh
human_reviewed: false
---

# CLAS12 前向飞行时间示例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

本示例展示来自 `clas12-systems` 的 CLAS12 前向飞行时间（FTOF）探测器几何。

{% assign example = site.data.examples | where: "title", "FTOF" | first %}

<br/>

## 快速上手

在 `clas12-systems` 仓库中，构建几何数据库并运行一次简短的模拟：

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ftof
./ftof.py
gemc ftof.yaml -n=1
```

<br/>

## 几何

下图所示的几何定义于 `geometry_src/ftof/ftof.py` 和 `geometry_src/ftof/geometry.py`。
FTOF 构建器读取本地 coatjava 几何工厂，将 CLAS12 前向 TOF 面板和
闪烁体条转换为 GEMC 几何体，并将它们存入 `gemc.db`。

世界体（一个名为 %%root%% 的盒状几何体）在六个扇区中的每个扇区内包含：

- 三个面板母体，命名为 %%ftof_p1a_s<sector>%%、%%ftof_p1b_s<sector>%% 和 %%ftof_p2_s<sector>%%
- 闪烁体条，命名为 %%panel1a_sector<sector>_paddle_<n>%%（23 条）、%%panel1b_...%%（62 条）和
  %%panel2_...%%（5 条）
- 位于面板 1a 和 2 后方的铅屏蔽，命名为 %%ftof_shield_p1a_sector<sector>%% 和
  %%ftof_shield_p2_sector<sector>%%

交互式查看器：

{% assign ftof_vtksz = "/home/assets/images/examples/ftof/ftof.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ftof_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 FTOF geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理列表

默认使用 `FTFP_BERT`，在 YAML 文件中通过 `phys_list: FTFP_BERT` 选择。

{% include notes/physics-list-note.md %}

<br/>

## 生成器

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

更多信息请参见[内置生成器文档]( /home/documentation/generator/internal )。

<br/>

## 数字化

闪烁体条使用 CLAS12 专用的 %%ftof%% 数字化插件。每根闪烁体条的两端均进行读出，
因此该插件会将每次命中拆分为左、右两个 PMT 通道。标识符记录
扇区、面板、闪烁体条以及 PMT 所在的一端：

```python
gvolume.digitization = "ftof"
gvolume.set_identifier("sector", sector, "panel", layer, "paddle", paddle, "side", 0)
```

<br/>

## 用法

### 构建探测器

使用 `geometry_src/ftof/ftof.py` 构建探测器。默认情况下，探测器配置存储在名为
`gemc.db` 的 SQLite 文件中。

更多信息请参见[构建几何]( /home/documentation/geometry/geometry_building )。

<br/>

### 运行 GEMC

可使用 `ftof.yaml` 文件运行该探测器配置。添加 `-gui` 可交互式运行：

```shell
gemc ftof.yaml -gui
```

按需修改 `ftof.yaml`，尤其是添加粒子、控制线程数或更改
输出时。

<br/>

## 运行事件

{% include figure.html
src="/assets/images/examples/ftof/gemc_view.png"
caption="CLAS12 FTOF simulation: generated electrons crossing the forward time-of-flight geometry."
%}

<br/>

## 输出

%%gstreamer%% 选项用于选择输出文件名和格式：

```yaml
gstreamer:
  - format: csv
    filename: ftof
  - format: hipo
    filename: ftof
```

更多信息请参见[输出文档]( /home/documentation/output )。


## 使用 GEMC 分析器绘图

先运行 GEMC，模拟 2,000 个事件。默认 YAML 文件会输出供分析器使用的 CSV 数据流。

```shell
gemc ftof.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

绘制每次命中的总沉积能量：

```shell
gemc-analyzer ftof_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![ftof 每次命中的总沉积能量][ftof-analyzer_totEdep]{:width="70%"}

[ftof-analyzer_totEdep]: /home/assets/images/examples/ftof/analyzer_totEdep.png

绘制命中位置的 y 与 x 关系图：

```shell
gemc-analyzer ftof_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![ftof 命中位置的 y 与 x 关系图][ftof-analyzer_yvsx]{:width="70%"}

[ftof-analyzer_yvsx]: /home/assets/images/examples/ftof/analyzer_yvsx.png
