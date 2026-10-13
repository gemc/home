---
layout: default
title: "Mirrors"
permalink: /examples/optical/mirrors.html
lang: zh
human_reviewed: false
---

# 镜面示例
<hr style="height:4px;border:0;background:#4a90e2;">

本示例展示 GEMC 的光学表面（"镜面"）。三个完全相同的 1 GeV 电子穿过一段低折射率气体辐射体，
每个电子都瞄准一块反射板的中心。切伦科夫光子沿每个电子保持在一个狭窄的前向锥内，并落在该电子对应的
反射板上。每块板演示一种不同的镜面定义：

* %%polished_metal%% —— 带有显式反射率表的 `dielectric_metal` / `polished` / `unified` 皮肤表面
  （skin surface）：典型的金属镀膜镜面；
* %%rough_metal%% —— 同样的皮肤表面，但采用 `ground` 抛光方式：反射进入一个镜面反射瓣
  （%%specularlobe%% = 1），其模糊程度由 %%sigmaAlpha%% 设定；
* %%semi_transparent%% —— 一面半镀银镜面，定义为辐射体与其反射板之间的**边界表面**
  （border surface）：60% 的光子被反射，30% 的光子透过反射板（%%transmittance%%），10% 被吸收。

每块板将其光子反射回它自己上游的光子探测器面板（使用 %%gPhotonDetector%% 数字化，并以其镜面的
颜色绘制），因此各面板看到的条件完全相同，仅反射方式不同。第四块面板在光子穿越半透明板后面一段大间隙
后统计透射的光子。典型的相对光子计数（以平板面板为 1）：

| 面板 | 表面 | 相对计数 |
|---|---|---|
| 平板（金色） | polished，R = 0.90 | 1.00 |
| 粗糙（番茄红） | 镜面反射瓣，sigmaAlpha = 0.03 | 约 0.99（图像模糊，略有泄漏） |
| 半透明（蓝色） | 反射，R = 0.60 | 约 0.69（= 0.60 / 0.90） |
| 后方（蓝色） | 透射，T = 0.30 | 约 0.37（= 0.30 / 0.90） |

<br/>

## 快速开始

将示例复制到当前目录。
要创建几何体、运行 10 个事例并生成 CSV 输出文件，请运行：

```shell
cp -r $GEMC_HOME/examples/optical/mirrors .
cd mirrors
./mirrors.py
gemc mirrors.yaml -n=10
```

<br/>

## 几何

几何体在 `mirrors.py` 中定义。世界体 %%root%% 包含一个 1 m^3 的气体辐射体
（%%radiatorGas%%，一种折射率约为 1.001 的演示用气体）。辐射体内部包含：

* 位于辐射体中部的三块薄板：两块承载皮肤镜面的铝板，以及半透明板 —— 由辐射体气体制成，以便透射的
  光子可以不受干扰地继续前进 —— 由 %%semi_transparent%% 边界表面作用于其上；
* 三块上游光子探测器面板，每块与一块反射板对齐，并以其镜面的颜色绘制，收集该板反射的光子；
* 半透明板后面一段长长的透射间隙，填充光学真空（折射率为 1），使电子在间隙中不辐射切伦科夫光，
  从而可以看到透射的光子穿越该间隙；
* 位于间隙末端的第四块面板，收集透射的光子。

交互式查看器：

{% assign mirrors_vtk = "/assets/images/examples/mirrors/mirrors.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ mirrors_vtk }}"
  title="Interactive VTK.js view of the mirrors geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="/assets/images/examples/mirrors/gemc_view.png"
caption="Mirrors simulation with 1 generated event."
%}

<br/>

## 镜面定义

每面镜面都是一个随几何体一同发布的 `GMirror`：

```python
polished = GMirror("polished_metal")
polished.type = "dielectric_metal"
polished.finish = "polished"
polished.model = "unified"
polished.border = "SkinSurface"
polished.photonEnergy = "2.0*eV 3.0*eV 4.0*eV 5.0*eV 6.0*eV"
polished.reflectivity = "0.90 0.90 0.89 0.88 0.87"
polished.publish(cfg)
```

各体积通过名称引用它们：

```python
plate.mirror = "polished_metal"
```

完整的字段参考请参阅[镜面文档](/home/documentation/optical/mirrors)。

<br/>

## 物理

steering card 启用光学物理：

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics
```

运行该示例会打印 GEMC 创建的表面：

```text
G4World: created optical surface <mirrors/polished_metal> type <dielectric_metal>,
finish <polished>, model <unified>
G4World: created 3 optical surfaces, attached to 2 skin and 1 border logical surfaces
```


## 使用 GEMC Analyzer 绘图

请先用 10 个事例运行 GEMC。默认的 YAML 文件会写出 analyzer 的 CSV 数据流。

```shell
gemc mirrors.yaml -n=10
```

### 各面板的 y 对 x

下面的图将光学光子的击中位置按 %%panel%% 拆分。后方的透射面板单独作为一幅图展示，不与半透明反射
面板的图合并。每幅图上显示的计数是从真信息数据流（true-information stream）中选出的行数。

| | |
|:---:|:---:|
| ![flat panel y vs x][mirrors-flat-panel-yvsx] | ![rough panel y vs x][mirrors-rough-panel-yvsx] |
| 平板反射面板<br>计数 = 2,445 | 粗糙反射面板<br>计数 = 2,269 |
| ![semi panel y vs x][mirrors-semi-panel-yvsx] | ![back panel y vs x][mirrors-back-panel-yvsx] |
| 半透明反射面板<br>计数 = 1,681 | 后方透射面板<br>计数 = 918 |

[mirrors-flat-panel-yvsx]: /home/assets/images/examples/mirrors/flat_panel_y_vs_x.png
[mirrors-rough-panel-yvsx]: /home/assets/images/examples/mirrors/rough_panel_y_vs_x.png
[mirrors-semi-panel-yvsx]: /home/assets/images/examples/mirrors/semi_panel_y_vs_x.png
[mirrors-back-panel-yvsx]: /home/assets/images/examples/mirrors/back_panel_y_vs_x.png
