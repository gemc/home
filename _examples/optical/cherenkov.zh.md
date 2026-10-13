---
layout: default
title: "Cherenkov"
permalink: /examples/optical/cherenkov.html
lang: zh
human_reviewed: false
---

[low-img]: /home/assets/images/examples/cherenkov/low_index_radiator.png
[medium-img]: /home/assets/images/examples/cherenkov/medium_index_radiator.png
[high-img]: /home/assets/images/examples/cherenkov/high_index_radiator.png
[lowy-img]: /home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png
[mediumy-img]: /home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png
[highy-img]: /home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png


# Cherenkov 示例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

本示例展示如何在 GEMC 探测器中激活切伦科夫辐射。
三个辐射体名称只是中性的演示标签。它们的光学常数可能并不符合物理实际，不应被当作真实材料的定义来理解。

{% assign example = site.data.examples | where: "title", "Cherenkov" | first %}

你可以在浏览器中运行本示例：[![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## 快速开始

将示例复制到当前目录。
要创建几何结构、运行 1 个事件并生成 ROOT 和 CSV 输出文件：

```shell
cp -r $GEMC_HOME/examples/optical/cherenkov .
cd cherenkov
./cherenkov.py
gemc cherenkov.yaml -n=1
```

<br/>

## 几何结构

几何结构（如下所示）定义在 `cherenkov.py` 中。它共产生三种变体：
%%default%%、%%mediumIndexRadiator%% 和 %%highIndexRadiator%%。

世界（一个名为 %%root%% 的立方体）包含一个 %%radiator%% 立方体。辐射体材料取决于所选的变体：

{:.zebra .compact-table}

| variation | material | color | refractive-index range |
|-----------|----------|-------|------------------------|
| %%default%% | %%lowIndexRadiator%% | 红色 | 1.0010-1.0013 |
| %%mediumIndexRadiator%% | %%mediumIndexRadiator%% | 蓝色 | 1.0110-1.0150 |
| %%highIndexRadiator%% | %%highIndexRadiator%% | 绿色 | 1.0500-1.0530 |


- 一个 %%gPhotonDetector%% 探测器，由四个立方体组成（%%detector_left%%、%%detector_right%%、%%detector_top%% 和 %%detector_bottom%%）。这样在中心留出一个小孔供束流通过。

交互式查看器：

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/cherenkov/cherenkov.vtksz"
  title="Interactive VTK.js view of the Cherenkov geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="/assets/images/examples/cherenkov/high_index_radiator.png"
caption="Cherenkov geometry with 1 generated electron. The highIndexRadiator volume (green, style = 2 renders it as a cloud) is the medium generating Cherenkov radiation."
%}


<br/>

## 物理过程列表

YAML 文件默认使用 `FTFP_BERT + G4OpticalPhysics`。其中的光学物理组件是产生光学光子所必需的。

{% include notes/physics-list-note.md %}

<br/>

## 发生器

粒子运动学在 YAML 文件中定义：

```yaml
gparticle:
  - name: e-
    p: 1000*MeV
    vz: -50*cm
```

更多信息另请参阅[内部发生器文档]( /home/documentation/generator/internal )。


<br/>


## 数字化

探测器体的灵敏度在 `cherenkov.py` 中通过 %%gPhotonDetector%% 数字化（GEMC 预置例程之一）来指定。

%%identifier%% 用于区分不同的探测器立方体：

```python
backplate.digitization = "gPhotonDetector"
backplate.set_identifier("detector", panel_id)
```

更多信息请参阅 [Flux 文档]( /home/documentation/sensitivity/gPhotonDetector )。


<br/>

## 使用方法

### 构建探测器

使用 Python 脚本 `cherenkov.py` 构建探测器。默认情况下，设置会存储在一个名为 `gemc.db` 的 SQLite 文件中。命令行选项可以指定数据库类型、变体和运行编号。

更多信息另请参阅[构建几何结构]( /home/documentation/geometry/geometry_building )。

<br/>

### 运行 GEMC

可以使用 `cherenkov.yaml` 文件来运行该设置。添加 `-gui` 可进行交互式运行：

```shell
gemc cherenkov.yaml -gui
```

该 YAML 设置了 `g4view.cloudPoints: 60000`，使云状风格的体足够稠密，以便渲染几何结构的屏幕截图。

可根据需要修改 `cherenkov.yaml`，特别是用于添加粒子、控制线程数或更改输出。
%%gPhotonDetector%% 数字化即使在光学光子未沉积能量时也会记录它们，因此本示例不需要 %%recordZeroEdep%%。

<br/>

### 变体

在 YAML 文件中，变体被设置为 %%mediumIndexRadiator%%。你可以将其替换为 %%default%% 或 %%highIndexRadiator%%
来更改材料。例如：

```yaml
gsystem:
  - name: cherenkov
    variation: highIndexRadiator
```

不同的辐射体材料会产生不同的光子产额和角度，如下所示。
它们的光学常数均为演示数值，可能并不符合物理实际。
当你希望为每个变体生成单独的输出文件时，可在 %%gstreamer%% 文件名中使用变体名称。


<br/>

|:---:|:---:|:---:|
| ![low index radiator](/home/assets/images/examples/cherenkov/low_index_radiator.png) | ![medium index radiator](/home/assets/images/examples/cherenkov/medium_index_radiator.png) | ![high index radiator](/home/assets/images/examples/cherenkov/high_index_radiator.png) |
| ![low index radiator y vs x](/home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png) | ![medium index radiator y vs x](/home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png) | ![high index radiator y vs x](/home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png) |

<p class="image-caption">
  左：<span class="gstring">lowIndexRadiator</span>，中：<span class="gstring">mediumIndexRadiator</span>，右：<span class="gstring">highIndexRadiator</span>。
</p>

<br/>

## 运行事件

{% include figure.html
src="/assets/images/examples/cherenkov/gemc_view.png"
caption="Cherenkov simulation: electron beam entering the radiator volume."
%}

<br/>

## 输出

%%gstreamer%% 选项用于选择输出文件名和格式：


```yaml
gstreamer:
  - format: csv
    filename: cherenkov
```

由于 %%gPhotonDetector%% 是逐事件的数字化，GEMC 会为每个线程生成一个输出文件。
对于 ROOT 文件，你可以使用 `hadd` 来合并这些文件。

更多信息另请参阅[输出文档]( /home/documentation/output )。

<br/>

## 使用 GEMC Analyzer 绘图

请先运行 GEMC 1 个事件。默认的 YAML 文件会写入 analyzer 的 CSV 数据流。

```shell
gemc cherenkov.yaml -n=1
```

绘制每次击中所沉积的总能量：

```shell
gemc-analyzer cherenkov_t0_digitized.csv totEdep --kind csv
```

![cherenkov total energy deposited per hit][cherenkov-analyzer_totEdep]{:width="70%"}

[cherenkov-analyzer_totEdep]: /home/assets/images/examples/cherenkov/analyzer_totEdep.png

绘制击中位置的 y 对 x 分布：

```shell
gemc-analyzer cherenkov_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![cherenkov y vs x hit positions][cherenkov-analyzer_yvsx]{:width="70%"}

[cherenkov-analyzer_yvsx]: /home/assets/images/examples/cherenkov/analyzer_yvsx.png
