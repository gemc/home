---
layout: default
title: "CLAS12 PCAL"
permalink: /examples/clas12/pcal.html
lang: zh
human_reviewed: false
---

# CLAS12 预簇射量能器示例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

本示例展示了来自 `clas12-systems` 的 CLAS12 预簇射量能器（PCAL）几何结构。

{% assign example = site.data.examples | where: "title", "PCAL" | first %}

<br/>

## 快速上手

在 `clas12-systems` 仓库中，构建几何数据库并运行一次简短的模拟：

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/pcal
./pcal.py
gemc pcal.yaml -n=1
```

<br/>

## 几何结构

如下图所示，几何结构定义于 `geometry_src/pcal/pcal.py` 和 `geometry_src/pcal/geometry.py` 中。
PCAL 构建器读取本地的 coatjava 几何工厂，将 CLAS12 预簇射量能器的扇区、窗口、铅层、
闪烁体层以及 U、V、W 条带体积转换为 GEMC 体积，并将它们存储在 `gemc.db` 中。

世界（一个名为 %%root%% 的盒子）中为六个扇区中的每一个包含：

- 名为 %%pcal_s1%% 到 %%pcal_s6%% 的扇区母体积
- 名为 %%Stainless_Steel_Front_...%% 和 %%Stainless_Steel_Back_...%% 的前后不锈钢窗口
- 名为 %%Last-a-Foam_Front_...%% 和 %%Last-a-Foam_Back_...%% 的前后 Last-a-Foam 窗口
- 名为 %%PCAL_Lead_Layer_<layer>_s<sector>%% 的铅层
- U、V、W 闪烁体层母体积以及单条/双条带体积

PCAL 是一个大型几何结构，因此本示例在 `_data/examples.yml` 中设置了 `pyvista-fast: true`，
以便在导出下方的交互式视图时使用快速 PyVista 渲染路径。

交互式查看器：

{% assign pcal_vtksz = "/home/assets/images/examples/pcal/pcal.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ pcal_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 PCAL geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理列表

默认使用 `FTFP_BERT`，通过 YAML 文件中的 `phys_list: FTFP_BERT` 选定。

{% include notes/physics-list-note.md %}

<br/>

## 发生器

粒子运动学在 YAML 文件中定义：

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

更多信息另请参阅[内部发生器文档]( /home/documentation/generator/internal )。

<br/>

## 数字化

闪烁体条带使用共享的 CLAS12 %%ecal%% 数字化插件。PCAL 与 EC 系统一样写入相同的 ECAL banks，
使用 hipo 层 1 到 3。标识符记录扇区、层和条带编号：

```python
gvolume.digitization = "ecal"
gvolume.set_identifier("sector", sector, "layer", layer, "strip", pcal_strip_id(uvw, kind, strip))
```

<br/>

## 用法

### 构建探测器

使用 `geometry_src/pcal/pcal.py` 构建探测器。默认情况下，该配置存储在一个名为 `gemc.db`
的 SQLite 文件中。

更多信息另请参阅[构建几何结构]( /home/documentation/geometry/geometry_building )。

<br/>

### 运行 GEMC

可以使用 `pcal.yaml` 文件来运行该配置。添加 `-gui` 以交互方式运行：

```shell
gemc pcal.yaml -gui
```

根据需要修改 `pcal.yaml`，特别是添加粒子、控制线程数或更改输出。

<br/>

## 运行事件

{% include figure.html
src="/assets/images/examples/pcal/gemc_view.png"
caption="CLAS12 PCAL simulation: generated electrons crossing the preshower calorimeter geometry."
%}

<br/>

## 输出

%%gstreamer%% 选项用于选择输出文件名和格式：

```yaml
gstreamer:
  - format: csv
    filename: pcal
  - format: hipo
    filename: pcal
```

更多信息另请参阅[输出文档]( /home/documentation/output )。


## 使用 GEMC 分析器绘图

首先运行 GEMC 生成 2,000 个事件。默认的 YAML 文件会写入分析器 CSV 流。

```shell
gemc pcal.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

绘制每次击中沉积的总能量：

```shell
gemc-analyzer pcal_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![pcal total energy deposited per hit][pcal-analyzer_totEdep]{:width="70%"}

[pcal-analyzer_totEdep]: /home/assets/images/examples/pcal/analyzer_totEdep.png

绘制 y 与 x 的击中位置关系：

```shell
gemc-analyzer pcal_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![pcal y vs x hit positions][pcal-analyzer_yvsx]{:width="70%"}

[pcal-analyzer_yvsx]: /home/assets/images/examples/pcal/analyzer_yvsx.png
