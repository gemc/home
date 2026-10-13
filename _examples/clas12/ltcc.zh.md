---
layout: default
title: "CLAS12 LTCC"
permalink: /examples/clas12/ltcc.html
lang: zh
human_reviewed: false
---

# CLAS12 低阈值契伦科夫计数器示例
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

本示例展示来自 `clas12-systems` 的 CLAS12 低阈值契伦科夫计数器（LTCC）几何结构。它将原生的 GEMC
镜面光学系统与通过 `gcad` 功能加载的 CAD 网格结合在一起。两套系统都存储在同一个 SQLite 数据库中。

LTCC 的几何结构与数字化功能在 `clas12-systems` 0.3 中提供，需配合 GEMC 0.5 和 `pygemc` 0.5.0 使用。

{% assign example = site.data.examples | where: "title", "LTCC" | first %}

<br/>

## 快速上手

在 `clas12-systems` 仓库中，构建几何数据库并运行一次简短的模拟：

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ltcc
./ltcc.py
gemc ltcc.yaml -n=1
```

<br/>

## 几何结构

如下图所示，几何结构定义在 `geometry_src/ltcc/geometry.py` 中，并由 `geometry_src/ltcc/ltcc.py` 统筹编排。
原生构建器移植了最初的 clas12Tags perl 脚本（镜面形状、PMT 和铁屏蔽层），而反射式 Winston 锥和机械框架则作为
CAD 网格导入。原生行使用 %%ltcc%% SQLite 系统，网格行则使用独立的 %%ltcc_cad%% CAD 系统。两者共享同一个
数据库、variation 和 run，因此一个 `gemc.db` 即可加载完整的探测器。

世界（一个名为 %%root%% 的盒子）为六个扇区中的每一个包含：

- 一个名为 %%ltccS<sector>%% 的气体母楔形体，容纳该扇区的光学元件
- 以 %%ltcc_AlMgF2%% 光学表面记录的柱面、双曲面和椭球面镜段
- 名为 %%pmt_s<sector><side>_<n>%% 的光电倍增管，在每个镜段的左侧和右侧读出
- 覆盖 Winston 锥外表面的 5 mm 铁屏蔽层
- 作为 %%copyOf%% 放置复用的 CAD Winston 锥（%%WC_S%%、%%WC_M%%、%%WC_L%%）和框架网格

交互式查看器：

{% assign ltcc_vtksz = "/home/assets/images/examples/ltcc/ltcc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ltcc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 LTCC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理列表

LTCC 是一种契伦科夫探测器，因此必须产生并追踪光学光子。YAML 文件通过
`phys_list: FTFP_BERT + G4OpticalPhysics` 选择 `FTFP_BERT + G4OpticalPhysics`。

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
    phi: 60*deg
    delta_phi: 180*deg
```

更多信息另见[内部发生器文档]( /home/documentation/generator/internal )。

<br/>

## 数字化

光电倍增管使用 CLAS12 专用的 %%ltcc%% 数字化插件。标识符记录扇区、PMT 所在侧以及该管所读出的镜段：

```python
pmt.digitization = "ltcc"
pmt.set_identifier("sector", sector, "side", side_id, "segment", n)
```

<br/>

## 使用方法

### 构建探测器

使用 `geometry_src/ltcc/ltcc.py` 构建探测器。该脚本定义材料和镜面，发布原生的 %%ltcc%% 体积，从
`stls/cad__default.yaml` 上传 %%ltcc_cad%% 系统的 CAD 定义，并添加 CAD 的 `copyOf` 放置。默认情况下，
两套系统都存储在名为 `gemc.db` 的 SQLite 文件中。

更多信息另见[构建几何结构]( /home/documentation/geometry/geometry_building )。

<br/>

### 运行 GEMC

可使用 `ltcc.yaml` 文件运行该配置。添加 `-gui` 以交互方式运行：

```shell
gemc ltcc.yaml -gui
```

可按需修改 `ltcc.yaml`，特别是用于添加粒子、控制线程数或更改输出。

<br/>

## 运行事件

{% include figure.html
src="/assets/images/examples/ltcc/gemc_view.png"
caption="CLAS12 LTCC simulation: generated electrons crossing the low-threshold Cherenkov counter geometry."
%}

<br/>

## 输出

%%gstreamer%% 选项用于选择输出文件名和格式：

```yaml
gstreamer:
  - format: csv
    filename: ltcc
  - format: hipo
    filename: ltcc
```

更多信息另见[输出文档]( /home/documentation/output )。


## 使用 GEMC 分析器绘图

首先运行 GEMC 进行 2,000 次事件模拟。默认的 YAML 文件会写出分析器 CSV 流。

```shell
gemc ltcc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

绘制每次击中沉积的总能量：

```shell
gemc-analyzer ltcc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![ltcc total energy deposited per hit][ltcc-analyzer_totEdep]{:width="70%"}

[ltcc-analyzer_totEdep]: /home/assets/images/examples/ltcc/analyzer_totEdep.png

绘制击中位置的 y 对 x 分布：

```shell
gemc-analyzer ltcc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![ltcc y vs x hit positions][ltcc-analyzer_yvsx]{:width="70%"}

[ltcc-analyzer_yvsx]: /home/assets/images/examples/ltcc/analyzer_yvsx.png
