---
layout: default
title: "Parabolic Mirror"
permalink: /examples/optical/parabolic_mirror.html
lang: zh
human_reviewed: false
---

# 抛物面镜示例
<hr style="height:4px;border:0;background:#4a90e2;">

本示例使用两个 Geant4 `G4Paraboloid` 实体构建一个类似望远镜的光学反射镜。一束平行的光学光子进入一个光学真空
体，从镜壳的内表面反射，并由位于标称焦点附近的一小块 %%gPhotonDetector%% 面板收集。

<br/>

## 快速开始

将示例复制到当前目录，创建几何结构，并运行一个事件：

```shell
cp -r $GEMC_HOME/examples/optical/parabolic_mirror .
cd parabolic_mirror
./parabolic_mirror.py
gemc parabolic_mirror.yaml -n=1
```

<br/>

## 几何结构

反射镜是一个薄的布尔壳体。几何脚本定义了两个构造操作数：

* %%outer_dish%% —— 外侧的 `G4Paraboloid`；
* %%inner_dish%% —— 一个略小的 `G4Paraboloid`，用于定义空腔。

两个操作数发布时都将 %%exist%% 设为 %%0%%。它们不会作为探测器体被放置，但其实体仍可用于最终的布尔运算：

```python
mirror = GVolume("parabolic_dish")
mirror.mother = "optical_space"
mirror.solidsOpr = "outer_dish - inner_dish"
mirror.set_position(0, 0, mirror_z)
mirror.set_rotation(180, 0, 0)
mirror.material = "G4_Al"
mirror.mirror = "parabolic_reflector"
mirror.publish(cfg)
```

`G4Paraboloid` 要求 %%-dz%% 处的半径小于 %%+dz%% 处的半径。最终的壳体绕 x 轴旋转 180 度，使开口面朝向入射的
光子。

交互式查看器：

{% assign parabolic_mirror_vtk = "/assets/images/examples/parabolic_mirror/parabolic_mirror.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ parabolic_mirror_vtk }}"
  title="Interactive VTK.js view of the parabolic mirror geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="/assets/images/examples/parabolic_mirror/gemc_view.png"
caption="Parabolic mirror simulation with 1 generated optical-photon event."
%}

<br/>

## 反射镜表面

反射镜镀层是一个附着在最终布尔壳体上的 `GMirror` 表皮表面（skin surface）：

```python
reflector = GMirror("parabolic_reflector")
reflector.type = "dielectric_metal"
reflector.finish = "polished"
reflector.model = "unified"
reflector.border = "SkinSurface"
reflector.photonEnergy = "2.0*eV 3.0*eV 4.0*eV 5.0*eV 6.0*eV"
reflector.reflectivity = "0.95 0.95 0.95 0.95 0.95"
reflector.publish(cfg)
```

```python
mirror.mirror = "parabolic_reflector"
```

有关反射镜表面字段，请参阅[反射镜文档](/home/documentation/optical/mirrors)。

<br/>

## 光子探测器

探测器放置在标称焦点附近，并使用 %%gPhotonDetector%%：

```python
detector = GVolume("focus_detector")
detector.make_tube(0, 60, 1, 0, 360)
detector.set_position(0, 0, focus_z)
detector.material = "opticalVacuum"
detector.digitization = "gPhotonDetector"
detector.set_identifier("panel", 1)
detector.publish(cfg)
```

该控制卡启用光学物理，并将光学光子射入反射镜孔径：

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics

gparticle:
  - name: opticalphoton
    multiplicity: 200
    p: 3*eV
    vz: -42*cm
    delta_vx: 17*cm
    delta_vy: 17*cm
```

Geant4 可能会警告生成的光学光子偏振为零，并为其分配随机偏振。对于这个简单的光源，该警告是预期之中的。
