---
layout: default
title: "Simple flux"
permalink: /examples/basic/simple_flux.html
lang: zh
human_reviewed: false
---

# 简单通量探测器
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

本示例使用 %%flux%% 数字化处理将真值信息和数字化信息保存到输出中。

{% assign example = site.data.examples | where: "title", "Simple Flux" | first %}

你可以在浏览器中运行本示例：[![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## 快速开始

将示例复制到当前目录。
要创建几何结构、运行 10 个事例并生成 ROOT 和 CSV 输出文件：

```shell
cp -r $GEMC_HOME/examples/basic/simple_flux .
cd simple_flux
./simple_flux.py
gemc simple_flux.yaml -n=10
```

<br/>

## 几何结构

如下所示的几何结构定义在 `simple_flux.py` 中。

世界体（一个名为 %%root%% 的长方体）包含：

- %%target%%，一个圆柱形液氢靶（%%G4_lH2%%）
- %%FluxPlane%%，一个由空气（%%G4_AIR%%）构成并指定使用 %%flux%% 数字化处理的长方体


交互式查看器：

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/simple_flux/simple_flux.vtksz"
  title="Interactive VTK.js view of the simple_flux geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>


<br/>

## 物理过程列表

默认使用 `QBBC`，在 YAML 文件中通过 `phys_list: QBBC` 选择。

{% include notes/physics-list-note.md %}

<br/>


## 发生器

粒子的运动学参数在 YAML 文件中定义：

```yaml
gparticle:
  - name: proton
    p: 2000*MeV
    vz: -3*cm
    delta_vx: 0.1*cm
    delta_vy: 0.1*cm
    multiplicity: 10
```

更多信息请参阅[内部发生器文档]( /home/documentation/generator/internal )。

<br/>


## 数字化

%%FluxPlane%% 的灵敏探测器响应通过 %%flux%% 数字化处理（GEMC 预置例程之一）
在 `simple_flux.py` 中指定，其标识符为 %%flux_plane = 1%%。

```python
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
```

在本例中，%%identifier%% 包含一个名称：%%flux_plane%%。

更多信息请参阅[通量文档]( /home/documentation/sensitivity/flux )。


除数字化变量外，真值信息也会保存到输出流中。

{% include notes/true_info-note.md %}


<br/>

## 用法

### 构建探测器

使用 Python 脚本 `simple_flux.py` 构建探测器。默认情况下，探测器配置存储在名为
`gemc.db` 的 SQLite 文件中。命令行选项可以指定数据库类型、变体和运行编号。

更多信息请参阅[构建几何结构]( /home/documentation/geometry/geometry_building )。


<br/>

### 运行 GEMC

可以使用文件 `simple_flux.yaml` 来运行该探测器配置。添加 `-gui` 以交互方式运行：

```shell
gemc simple_flux.yaml -gui
```

根据需要修改 `simple_flux.yaml`，尤其是添加粒子、控制线程数或更改输出。

<br/>

## 运行事例

{% include figure.html
src="/assets/images/examples/simple_flux/gemc_view.png"
caption="Simple flux simulation: proton tracks traversing the flux detector volumes."
%}

<br/>

## 输出

%%gstreamer%% 选项用于选择输出文件名和格式：

```yaml
gstreamer:
  - format: csv
    filename: simple_flux
```

由于 %%flux%% 按事例进行数字化处理，GEMC 将为每个线程生成一个输出文件。
对于 ROOT 文件，你可以使用 `hadd` 来合并这些文件。


更多信息请参阅[输出文档]( /home/documentation/output )。


<br/>

## 使用 GEMC 分析器绘图

请先使用 GEMC 运行 10,000 个事例。默认的 YAML 文件会输出供分析器使用的 CSV 数据流。

```shell
gemc simple_flux.yaml -n=10000
```

绘制每次击中所沉积的总能量：

```shell
gemc-analyzer simple_flux_t0_digitized.csv totEdep --kind csv
```

![simple_flux 每次击中所沉积的总能量][simple_flux-analyzer_totEdep]{:width="70%"}

[simple_flux-analyzer_totEdep]: /home/assets/images/examples/simple_flux/analyzer_totEdep.png

绘制粒子径迹的真实能量：

```shell
gemc-analyzer simple_flux_t0_true_info.csv E --kind csv --data true_info
```

![simple_flux 粒子径迹的真实能量][simple_flux-analyzer_true_energy]{:width="70%"}

[simple_flux-analyzer_true_energy]: /home/assets/images/examples/simple_flux/analyzer_true_energy.png
