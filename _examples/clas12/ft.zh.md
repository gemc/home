---
layout: default
title: "CLAS12 FT"
permalink: /examples/clas12/ft.html
lang: zh
human_reviewed: false
---

# CLAS12 前向标记器示例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

本示例展示了来自 `clas12-systems` 的 CLAS12 前向标记器（FT）几何结构。FT 位于小极角区域，
由三个子系统构成：电磁量能器、闪烁体径迹计（hodoscope），
以及 Micromegas 径迹探测器。

FT 的几何结构与数字化功能在 `clas12-systems` 0.3 中提供，需配合 GEMC 0.5 与 `pygemc` 0.5.0 使用。

{% assign example = site.data.examples | where: "title", "FT" | first %}

<br/>

## 快速开始

在 `clas12-systems` 仓库中，构建几何数据库并运行一次简短的模拟：

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ft
./ft.py
gemc ft.yaml -n=1
```

<br/>

## 几何结构

下图所示的几何结构在 `geometry_src/ft/geometry.py` 中定义，并由
`geometry_src/ft/ft.py` 构建。FT 构建器将三个子系统组装到同一个 `gemc.db` 中：

- **量能器**，由 PbWO4 晶体组成的阵列，每块晶体均有包覆层并与一个 APD 耦合，命名为
  %%ft_cal_cr_h<ih>_v<iv>%%，此外还包含铜制外壳、主板和屏蔽体
- **径迹计**，由闪烁体块组成，按扇区、层和组件命名
- **径迹探测器**，由 Micromegas 圆盘组成，每一层的每一侧均包含 Kapton、光刻胶和环形体

世界体积（一个名为 %%root%% 的盒子）包含全部三个子系统。在量能器
和径迹探测器处添加了通量探测器，以记录入射粒子通量。

交互式查看器：

{% assign ft_vtksz = "/home/assets/images/examples/ft/ft.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ft_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 FT geometry"
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
    p: 2000*MeV
    theta: 3*deg
    phi: 10*deg
    delta_phi: 180*deg
```

更多信息另请参阅[内部生成器文档]( /home/documentation/generator/internal )。

<br/>

## 数字化

每个 FT 子系统使用各自的 CLAS12 专用数字化插件。量能器晶体使用 %%ft_cal%%，
径迹计的闪烁体块使用 %%ft_hodo%%，径迹探测器圆盘使用 %%ft_trk%%。标识符记录
所读出的组件，例如量能器晶体的行和列：

```python
digitization="ft_cal",
identifiers=("ih", ix, "iv", iy),
```

<br/>

## 用法

### 构建探测器

使用 `geometry_src/ft/ft.py` 构建探测器。默认情况下，探测器配置存储在名为
`gemc.db` 的 SQLite 文件中。

更多信息另请参阅[构建几何结构]( /home/documentation/geometry/geometry_building )。

<br/>

### 运行 GEMC

可使用文件 `ft.yaml` 运行该探测器配置。添加 `-gui` 以交互方式运行：

```shell
gemc ft.yaml -gui
```

可根据需要修改 `ft.yaml`，尤其是添加粒子、控制线程数或更改
输出。

<br/>

## 运行事件

{% include figure.html
src="/assets/images/examples/ft/gemc_view.png"
caption="CLAS12 FT simulation: generated electrons crossing the forward tagger geometry."
%}

<br/>

## 输出

%%gstreamer%% 选项用于选择输出文件名和格式：

```yaml
gstreamer:
  - format: csv
    filename: ft
  - format: hipo
    filename: ft
```

更多信息另请参阅[输出文档]( /home/documentation/output )。

前向标记器读出三个探测器（%%ft_cal%%、%%ft_hodo%% 和 %%ft_trk%%），它们具有不同的
标识符结构。下面的分析器示例禁用了通量探测器、径迹计和径迹探测器的真实信息输出与数字化输出，
使 CSV 中的数据采用一致的 %%ft_cal%% 数据结构。


## 使用 GEMC 分析器绘图

先运行 GEMC，模拟 2,000 个事件。默认 YAML 文件会写出分析器所需的 CSV 数据流。

```shell
gemc ft.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build \
  -no_true_info="flux ft_hodo ft_trk" -no_digitized="flux ft_hodo ft_trk"
```

绘制每次击中的总沉积能量：

```shell
gemc-analyzer ft_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![FT 每次击中的总沉积能量][ft-analyzer_totEdep]{:width="70%"}

[ft-analyzer_totEdep]: /home/assets/images/examples/ft/analyzer_totEdep.png

绘制击中位置的 y 对 x 分布：

```shell
gemc-analyzer ft_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![FT 击中位置的 y 对 x 分布][ft-analyzer_yvsx]{:width="70%"}

[ft-analyzer_yvsx]: /home/assets/images/examples/ft/analyzer_yvsx.png
