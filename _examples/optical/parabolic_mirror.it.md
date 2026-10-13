---
layout: default
title: "Parabolic Mirror"
permalink: /examples/optical/parabolic_mirror.html
lang: it
human_reviewed: false
---

# Esempio di Specchio Parabolico
<hr style="height:4px;border:0;background:#4a90e2;">

Questo esempio costruisce uno specchio ottico simile a un telescopio a partire da due solidi
`G4Paraboloid` di Geant4. Un fascio parallelo di fotoni ottici entra in un volume di vuoto ottico,
si riflette dalla superficie interna del guscio dello specchio e viene raccolto da un piccolo
pannello %%gPhotonDetector%% in prossimità del fuoco nominale.

<br/>

## Avvio rapido

Copia l'esempio nella tua directory corrente, crea la geometria ed esegui un evento:

```shell
cp -r $GEMC_HOME/examples/optical/parabolic_mirror .
cd parabolic_mirror
./parabolic_mirror.py
gemc parabolic_mirror.yaml -n=1
```

<br/>

## Geometria

Lo specchio è un sottile guscio booleano. Lo script della geometria definisce due operandi di
costruzione:

* %%outer_dish%% - il `G4Paraboloid` esterno;
* %%inner_dish%% - un `G4Paraboloid` leggermente più piccolo che definisce la cavità vuota.

Entrambi gli operandi vengono pubblicati con %%exist%% impostato a %%0%%. Non vengono collocati come
volumi rivelatore, ma i loro solidi restano disponibili per l'operazione booleana finale:

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

`G4Paraboloid` richiede che il raggio a %%-dz%% sia minore del raggio a %%+dz%%. Il guscio finale viene
ruotato di 180 gradi attorno a x in modo che il lato aperto sia rivolto verso i fotoni in arrivo.

Visualizzatore interattivo:

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

## Superficie dello specchio

Il rivestimento dello specchio è una superficie di tipo skin `GMirror` applicata al guscio booleano
finale:

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

Consulta la [documentazione sugli specchi](/home/documentation/optical/mirrors) per i campi della
superficie dello specchio.

<br/>

## Rivelatore di fotoni

Il rivelatore è collocato in prossimità del punto focale nominale e utilizza %%gPhotonDetector%%:

```python
detector = GVolume("focus_detector")
detector.make_tube(0, 60, 1, 0, 360)
detector.set_position(0, 0, focus_z)
detector.material = "opticalVacuum"
detector.digitization = "gPhotonDetector"
detector.set_identifier("panel", 1)
detector.publish(cfg)
```

La steering card abilita la fisica ottica e lancia fotoni ottici nell'apertura dello specchio:

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

Geant4 potrebbe avvisare che i fotoni ottici generati hanno polarizzazione nulla e assegnare una
polarizzazione casuale. Tale avviso è previsto per questa semplice sorgente.
