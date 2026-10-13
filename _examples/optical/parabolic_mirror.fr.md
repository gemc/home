---
layout: default
title: "Parabolic Mirror"
permalink: /examples/optical/parabolic_mirror.html
lang: fr
human_reviewed: false
---

# Exemple de miroir parabolique
<hr style="height:4px;border:0;background:#4a90e2;">

Cet exemple construit un miroir optique de type télescope à partir de deux solides
Geant4 `G4Paraboloid`. Un faisceau parallèle de photons optiques pénètre dans un
volume de vide optique, se réfléchit sur la surface interne de la coque du miroir,
puis est collecté par un petit panneau %%gPhotonDetector%% situé près du foyer nominal.

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant, créez la géométrie et exécutez un événement :

```shell
cp -r $GEMC_HOME/examples/optical/parabolic_mirror .
cd parabolic_mirror
./parabolic_mirror.py
gemc parabolic_mirror.yaml -n=1
```

<br/>

## Géométrie

Le miroir est une fine coque booléenne. Le script de géométrie définit deux opérandes
de construction :

* %%outer_dish%% - le `G4Paraboloid` extérieur ;
* %%inner_dish%% - un `G4Paraboloid` légèrement plus petit qui définit la cavité vide.

Les deux opérandes sont publiés avec %%exist%% réglé à %%0%%. Ils ne sont pas placés en
tant que volumes de détecteur, mais leurs solides restent disponibles pour l'opération
booléenne finale :

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

`G4Paraboloid` exige que le rayon à %%-dz%% soit plus petit que le rayon à %%+dz%%. La
coque finale est tournée de 180 degrés autour de x afin que le côté ouvert fasse face
aux photons incidents.

Visualiseur interactif :

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

## Surface du miroir

Le revêtement du miroir est une surface de type peau (skin surface) `GMirror`
attachée à la coque booléenne finale :

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

Consultez la [documentation sur les miroirs](/home/documentation/optical/mirrors) pour
les champs de la surface du miroir.

<br/>

## Détecteur de photons

Le détecteur est placé près du point focal nominal et utilise %%gPhotonDetector%% :

```python
detector = GVolume("focus_detector")
detector.make_tube(0, 60, 1, 0, 360)
detector.set_position(0, 0, focus_z)
detector.material = "opticalVacuum"
detector.digitization = "gPhotonDetector"
detector.set_identifier("panel", 1)
detector.publish(cfg)
```

La carte de pilotage active la physique optique et lance des photons optiques dans
l'ouverture du miroir :

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

Geant4 peut avertir que les photons optiques générés ont une polarisation nulle et
leur attribuer une polarisation aléatoire. Cet avertissement est attendu pour cette
source simple.
