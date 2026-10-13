---
layout: default
title: "Scintillator Barrel"
permalink: /examples/basic/scintillator_barrel.html
lang: zh
human_reviewed: false
---

# 闪烁体桶形探测器
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

本示例构建了一个圆柱形闪烁体桶形探测器，由 48 个梯形闪烁条
排列成一个完整的环。它演示了如何使用 `distribute_on_circle` API 将
一个几何体沿圆周按相等的角度间隔复制，并展示了如何确定闪烁条的尺寸，
使相邻的面近乎彼此相接。


{% assign example = site.data.examples | where: "title", "Scintillator Barrel" | first %}
您可以在浏览器中运行本示例：[![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## 快速上手

将示例复制到当前目录。
创建几何并运行 3 个事件：

```shell
cp -r $GEMC_HOME/examples/basic/scintillator_barrel .
cd scintillator_barrel
./scintillator_barrel.py
gemc scintillator_barrel.yaml
```

<br/>

## 几何

几何在 `scintillator_barrel.py` 中定义。世界体（一个名为 %%root%% 的盒状几何体）包含
48 个完全相同的 %%paddle%% 几何体，排列成一个环：

- 每个 %%paddle%% 都是一个 `G4Trap` 通用梯形体（材料为 %%G4_PLASTIC_SC_VINYLTOLUENE%%），其
  较宽的面朝向径向外侧，较窄的面朝向束流轴。
- 闪烁条的尺寸按弦长公式确定，使相邻的外侧面彼此相接：
  - 外侧半宽：`pX  = (radius + pY) × sin(π/n)`
  - 内侧半宽：`pLTX = (radius − pY) × sin(π/n)`
- `distribute_on_circle(n=48, radius=400 mm, align=True, axis='z')` 以相等的 7.5° 步长，将每个副本
  绕 z 轴放置并旋转。

有关完整的 `distribute_on_circle` API 参考以及尺寸计算的几何原理，请参阅
[结构辅助工具](/home/documentation/geometry/structure)文档。

交互式查看器（包含全部 48 个闪烁条的桶形探测器）：

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/scintillator_barrel/scintillator_barrel.vtksz"
  title="Interactive VTK.js view of the scintillator_barrel geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## 物理列表

默认使用 `QBBC`，在 YAML 文件中通过 `phys_list: QBBC` 选择。

{% include notes/physics-list-note.md %}

<br/>

## 发生器

粒子的运动学参数在 YAML 文件中定义：

```yaml
gparticle:
  - name: proton
    p: 500*MeV
    theta: 90*deg
    delta_phi: 360*deg
    multiplicity: 3
```

更多信息另请参阅[内部发生器文档]( /home/documentation/generator/internal )。

<br/>

## 数字化

每个 %%paddle%% 都被指定使用 %%flux%% 数字化方式，并具有唯一的闪烁条标识符：

```python
paddle.digitization = "flux"
# ...
v.set_identifier("paddle", i)
```

更多信息请参阅 [Flux 文档]( /home/documentation/sensitivity/flux )。

<br/>

## `distribute_on_circle` API

`GVolume` 的 `distribute_on_circle` 方法会将模板几何体沿半径为 `radius` 的圆周
复制 `n` 次。当 `align=True` 时，每个副本还会绕所选的轴旋转其角位置 φᵢ 所对应的角度，
从而使每个闪烁条的局部坐标系保持径向对齐：

```python
for i, v in enumerate(paddle.distribute_on_circle(n, radius, align=True, axis='z')):
    v.set_identifier("paddle", i)
    v.publish(cfg)
```

该方法返回一个由相互独立的 `GVolume` 副本组成的列表，每个角度步长对应一个副本，各自命名为
`<name>_i`，并定位于 `(radius·cos φᵢ, radius·sin φᵢ, 0)`。
完整的 API 参考请见[结构辅助工具](/home/documentation/geometry/structure)文档。

<br/>

## 使用方法

### 构建探测器

使用 Python 脚本 `scintillator_barrel.py` 构建探测器。默认情况下，探测器配置
存储在一个名为 `gemc.db` 的 SQLite 文件中。命令行选项可以指定数据库类型、
变体和运行编号。

更多信息另请参阅[构建几何]( /home/documentation/geometry/geometry_building )。

<br/>

### 运行 GEMC

文件 `scintillator_barrel.yaml` 用于运行仿真。添加 `-gui` 可以交互式运行：

```shell
gemc scintillator_barrel.yaml -gui
```

可按需修改 `scintillator_barrel.yaml`，例如更改事件数量、
增加线程数或选择输出格式。

<br/>

## 运行事件

下图展示了运行一个事件后沿束流轴观察的桶形探测器端视图，其中 3 个质子
以 θ = 90° 沿径向向外发射。每个质子都穿过一个闪烁条。

{% include figure.html
src="/assets/images/examples/scintillator_barrel/gemc_view.png"
caption="Scintillator barrel viewed end-on along the beam axis. Three protons at θ = 90°
travel radially outward, each depositing energy in one paddle."
%}

<br/>

## 输出

%%gstreamer%% 选项用于选择输出文件名和格式：

```yaml
gstreamer:
  - format: csv
    filename: barrel
```

更多信息另请参阅[输出文档]( /home/documentation/output )。

<br/>

## 使用 GEMC 分析器绘图

首先使用 GEMC 运行 1,000 个事件。默认的 YAML 文件会将分析器所需的数据流写入 CSV 文件。

```shell
gemc scintillator_barrel.yaml -n=1000
```

绘制每次击中的总沉积能量：

```shell
gemc-analyzer barrel_t0_digitized.csv totEdep --kind csv
```

![scintillator_barrel 每次击中的总沉积能量][scintillator_barrel-analyzer_totEdep]{:width="70%"}

[scintillator_barrel-analyzer_totEdep]: /home/assets/images/examples/scintillator_barrel/analyzer_totEdep.png

绘制粒子径迹的真实能量：

```shell
gemc-analyzer barrel_t0_true_info.csv E --kind csv --data true_info
```

![scintillator_barrel 粒子径迹的真实能量][scintillator_barrel-analyzer_true_energy]{:width="70%"}

[scintillator_barrel-analyzer_true_energy]: /home/assets/images/examples/scintillator_barrel/analyzer_true_energy.png
