---
layout: default
title: "Parabolic Mirror"
permalink: /examples/optical/parabolic_mirror.html
lang: ja
human_reviewed: false
---

# 放物面鏡の例
<hr style="height:4px;border:0;background:#4a90e2;">

この例では、2つのGeant4 `G4Paraboloid` ソリッドから望遠鏡のような光学鏡を構築します。光学光子の平行
ビームが光学真空ボリュームに入射し、鏡シェルの内面で反射して、公称焦点付近にある小さな
%%gPhotonDetector%% パネルに集められます。

<br/>

## クイックスタート

この例を現在のディレクトリにコピーし、ジオメトリを作成して、1イベントを実行します:

```shell
cp -r $GEMC_HOME/examples/optical/parabolic_mirror .
cd parabolic_mirror
./parabolic_mirror.py
gemc parabolic_mirror.yaml -n=1
```

<br/>

## ジオメトリ

この鏡は薄いブール演算シェルです。ジオメトリスクリプトは、2つの構築オペランドを定義します:

* %%outer_dish%% - 外側の `G4Paraboloid`;
* %%inner_dish%% - 空のキャビティを定義する、やや小さい `G4Paraboloid`。

どちらのオペランドも %%exist%% を %%0%% に設定して公開されます。これらは検出器ボリュームとして配置され
ませんが、そのソリッドは最終的なブール演算で引き続き利用できます:

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

`G4Paraboloid` では、%%-dz%% での半径が %%+dz%% での半径よりも小さい必要があります。最終的なシェルは、
開いた側が入射する光子に面するように、x軸まわりに180度回転されます。

インタラクティブビューア:

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

## 鏡面

鏡のコーティングは、最終的なブール演算シェルに取り付けられた `GMirror` スキンサーフェスです:

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

鏡面のフィールドについては、[鏡のドキュメント](/home/documentation/optical/mirrors)を参照してください。

<br/>

## 光子検出器

検出器は公称焦点付近に配置され、%%gPhotonDetector%% を使用します:

```python
detector = GVolume("focus_detector")
detector.make_tube(0, 60, 1, 0, 360)
detector.set_position(0, 0, focus_z)
detector.material = "opticalVacuum"
detector.digitization = "gPhotonDetector"
detector.set_identifier("panel", 1)
detector.publish(cfg)
```

ステアリングカードは光学物理を有効にし、光学光子を鏡の開口部に向けて発射します:

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

Geant4は、生成された光学光子の偏光がゼロであると警告し、ランダムな偏光を割り当てる場合があります。この
警告は、この単純な光源では想定内のものです。
