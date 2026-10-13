---
layout: default
title: "Mirrors"
permalink: /examples/optical/mirrors.html
lang: fr
human_reviewed: false
---

# Exemple des miroirs
<hr style="height:4px;border:0;background:#4a90e2;">

Cet exemple met en valeur les surfaces optiques (« miroirs ») de GEMC. Trois électrons identiques de 1 GeV
traversent un radiateur gazeux à faible indice, chacun visant le centre d'une plaque réflectrice. Les photons
Cherenkov restent dans un cône étroit vers l'avant autour de chaque électron et atteignent la plaque de cet
électron. Chaque plaque illustre une définition de miroir différente :

* %%polished_metal%% - surface de type peau (skin surface) `dielectric_metal` / `polished` / `unified` avec une
  table de réflectivité explicite : un miroir typique revêtu de métal ;
* %%rough_metal%% - la même surface de type peau avec une finition `ground` : la réflexion se fait dans un lobe
  spéculaire (%%specularlobe%% = 1) dont le flou est fixé par %%sigmaAlpha%% ;
* %%semi_transparent%% - un miroir semi-réfléchissant défini comme **surface de bord** (border surface) entre le
  radiateur et sa plaque : 60 % des photons sont réfléchis, 30 % sont transmis à travers la plaque
  (%%transmittance%%) et 10 % sont absorbés.

Chaque plaque réfléchit ses photons vers son propre panneau détecteur de photons situé en amont (en utilisant la
numérisation %%gPhotonDetector%% et dessiné dans la couleur de son miroir), de sorte que les panneaux voient des
conditions identiques et que seule la réflexion diffère. Un quatrième panneau compte les photons transmis après
qu'ils ont franchi un large espace derrière la plaque semi-transparente. Comptages relatifs de photons typiques
(panneau plat = 1) :

| Panneau | Surface | Comptage relatif |
|---|---|---|
| plat (or) | polished, R = 0,90 | 1,00 |
| rugueux (tomate) | lobe spéculaire, sigmaAlpha = 0,03 | environ 0,99 (image floue, légère fuite) |
| semi (bleu) | réfléchi, R = 0,60 | environ 0,69 (= 0,60 / 0,90) |
| derrière (bleu) | transmis, T = 0,30 | environ 0,37 (= 0,30 / 0,90) |

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant.
Pour créer la géométrie, exécuter 10 événements et produire des fichiers de sortie CSV :

```shell
cp -r $GEMC_HOME/examples/optical/mirrors .
cd mirrors
./mirrors.py
gemc mirrors.yaml -n=10
```

<br/>

## Géométrie

La géométrie est définie dans `mirrors.py`. Le volume monde %%root%% contient un radiateur gazeux de 1 m^3
(%%radiatorGas%%, un gaz de démonstration dont l'indice de réfraction est d'environ 1,001). À l'intérieur du
radiateur :

* trois plaques fines au milieu du radiateur : deux plaques en aluminium portant les miroirs de type peau, et la
  plaque semi-transparente - faite de gaz radiateur afin que les photons transmis continuent sans être perturbés
  - visée par la surface de bord %%semi_transparent%% ;
* trois panneaux détecteurs de photons en amont, chacun aligné avec une plaque et dessiné dans la couleur de son
  miroir, collectant les photons réfléchis par cette plaque ;
* un long espace de transmission derrière la plaque semi-transparente, rempli d'un vide optique (indice de
  réfraction 1) afin que l'électron ne rayonne aucune lumière Cherenkov dans l'espace et que l'on puisse voir
  les photons transmis le traverser ;
* un quatrième panneau à l'extrémité de l'espace, collectant les photons transmis.

Visualiseur interactif :

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

## Définitions des miroirs

Chaque miroir est un `GMirror` publié aux côtés de la géométrie :

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

et les volumes y font référence par leur nom :

```python
plate.mirror = "polished_metal"
```

Consultez la [documentation des miroirs](/home/documentation/optical/mirrors) pour la référence complète des
champs.

<br/>

## Physique

La carte de pilotage active la physique optique :

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics
```

L'exécution de l'exemple affiche les surfaces créées par GEMC :

```text
G4World: created optical surface <mirrors/polished_metal> type <dielectric_metal>,
finish <polished>, model <unified>
G4World: created 3 optical surfaces, attached to 2 skin and 1 border logical surfaces
```


## Tracés avec l'analyseur GEMC

Exécutez d'abord GEMC avec 10 événements. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc mirrors.yaml -n=10
```

### y en fonction de x par panneau

Les tracés ci-dessous répartissent les positions des impacts de photons optiques par %%panel%%. Le panneau de
transmission arrière est présenté comme son propre tracé, et non fusionné avec le tracé du panneau réfléchi
semi-transparent. Le comptage affiché sur chaque image correspond au nombre de lignes sélectionnées dans le flux
d'informations vraies.

| | |
|:---:|:---:|
| ![flat panel y vs x][mirrors-flat-panel-yvsx] | ![rough panel y vs x][mirrors-rough-panel-yvsx] |
| panneau réfléchi plat<br>comptages = 2 445 | panneau réfléchi rugueux<br>comptages = 2 269 |
| ![semi panel y vs x][mirrors-semi-panel-yvsx] | ![back panel y vs x][mirrors-back-panel-yvsx] |
| panneau réfléchi semi-transparent<br>comptages = 1 681 | panneau transmis arrière<br>comptages = 918 |

[mirrors-flat-panel-yvsx]: /home/assets/images/examples/mirrors/flat_panel_y_vs_x.png
[mirrors-rough-panel-yvsx]: /home/assets/images/examples/mirrors/rough_panel_y_vs_x.png
[mirrors-semi-panel-yvsx]: /home/assets/images/examples/mirrors/semi_panel_y_vs_x.png
[mirrors-back-panel-yvsx]: /home/assets/images/examples/mirrors/back_panel_y_vs_x.png
