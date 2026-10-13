---
layout: default
title: "CLAS12 HTCC"
permalink: /examples/clas12/htcc.html
lang: zh
human_reviewed: false
---

# CLAS12 高阈值切伦科夫计数器示例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

本示例展示了来自 `clas12-systems` 的 CLAS12 高阈值切伦科夫计数器（HTCC）几何结构。
它将 GEMC 原生反射镜光学系统与通过 `gcad` 功能加载的 CAD 网格相结合。
这两套系统都存储在同一个 SQLite 数据库中。

HTCC 几何结构和数字化功能在 `clas12-systems` 0.3 中提供，配合 GEMC 0.5 和 `pygemc` 0.5.0 使用。

{% assign example = site.data.examples | where: "title", "HTCC" | first %}

<br/>

## 快速开始

在 `clas12-systems` 仓库中，构建几何数据库并运行一次简短的模拟：

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/htcc
./htcc.py
gemc htcc.yaml -n=1
```

<br/>

## 几何结构

下图所示的几何结构定义在 `geometry_src/htcc/geometry.py` 中，由
`geometry_src/htcc/htcc.py` 统筹构建。原生构建器移植了原始 clas12Tags Perl 脚本（气体几何体、
窗、48 个椭圆反射镜和 48 个光电倍增管），而三个束流线锥体则作为 CAD 网格导入。
原生几何记录使用 %%htcc%% SQLite 系统，网格记录使用独立的 %%htcc_cad%% CAD 系统。
两者共享同一个数据库、变体和运行编号，因此单个 `gemc.db` 即可加载完整的探测器。

世界体（一个名为 %%root%% 的盒子）包含：

- 通过多锥体布尔运算构建的 %%htcc%% 气体几何体，以及 %%htccEntryWindow%% 和 %%htccExitWindow%%
- 从多锥体筒体中切割出的 48 个椭圆反射镜段，记录中指定了 %%htcc_AlMgF2%%
  光学表面
- 名为 %%pmt_<ring>_sector<sector>_<half>%% 的光电倍增管，每个扇区按两个半扇区分别读出
- 共用 %%htcc_AlMgF2%% 反射镜表层的 Winston 锥抛物面壳体
- 放置于 %%root%% 下的 CAD 束流线锥体（%%htccCone%%、%%htccMollerCone%%、%%htccMollerConeExt%%）

交互式查看器：

{% assign htcc_vtksz = "/home/assets/images/examples/htcc/htcc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ htcc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 HTCC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理列表

HTCC 是一种切伦科夫探测器，因此必须产生并跟踪光学光子。YAML 文件通过
`phys_list: FTFP_BERT + G4OpticalPhysics` 选择 `FTFP_BERT + G4OpticalPhysics`。

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
    phi: 60*deg
    delta_phi: 180*deg
```

更多信息另见[内部生成器文档]( /home/documentation/generator/internal )。

<br/>

## 数字化

光电倍增管使用 CLAS12 专用的 %%htcc%% 数字化插件。标识符记录
扇区、反射镜环以及该管所读出的半扇区：

```python
pmt.digitization = "htcc"
pmt.set_identifier("sector", sector, "ring", ring, "half", hindex)
```

<br/>

## 用法

### 构建探测器

使用 `geometry_src/htcc/htcc.py` 构建探测器。该脚本定义材料和反射镜表面，
发布原生 %%htcc%% 几何体，并将三个束流线锥体作为 CAD 网格发布到
%%htcc_cad%% 系统。默认情况下，两套系统都存储在一个名为 `gemc.db` 的 SQLite 文件中。

更多信息另见[构建几何结构]( /home/documentation/geometry/geometry_building )。

<br/>

### 运行 GEMC

可使用 `htcc.yaml` 文件运行此配置。添加 `-gui` 可交互式运行：

```shell
gemc htcc.yaml -gui
```

可根据需要修改 `htcc.yaml`，尤其是添加粒子、控制线程数或更改
输出。

<br/>

## 运行事件

{% include figure.html
src="/assets/images/examples/htcc/gemc_view.png"
caption="CLAS12 HTCC simulation: generated electrons crossing the high-threshold Cherenkov counter geometry."
%}

<br/>

## 输出

%%gstreamer%% 选项用于选择输出文件名和格式：

```yaml
gstreamer:
  - format: csv
    filename: htcc
  - format: hipo
    filename: htcc
```

更多信息另见[输出文档]( /home/documentation/output )。


## 使用 GEMC 分析器绘图

先运行 GEMC，模拟 2,000 个事件。默认的 YAML 文件会写出供分析器使用的 CSV 数据流。

```shell
gemc htcc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

绘制每次击中沉积的总能量：

```shell
gemc-analyzer htcc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![htcc 每次击中沉积的总能量][htcc-analyzer_totEdep]{:width="70%"}

[htcc-analyzer_totEdep]: /home/assets/images/examples/htcc/analyzer_totEdep.png

绘制击中位置的 y 对 x 分布：

```shell
gemc-analyzer htcc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![htcc 击中位置的 y 对 x 分布][htcc-analyzer_yvsx]{:width="70%"}

[htcc-analyzer_yvsx]: /home/assets/images/examples/htcc/analyzer_yvsx.png
