---
layout: default
title: "Materials"
permalink: /examples/basic/materials.html
lang: fr
human_reviewed: false
---

# Exemple sur les matériaux
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple illustre les quatre façons de définir un matériau dans GEMC : utiliser un matériau intégré à
Geant4, composer un matériau à partir d'éléments par nombre d'atomes, composer un matériau à partir de
matériaux existants par fraction massique, et ajouter des propriétés optiques pour la scintillation ou le
rayonnement Tcherenkov.

<br/>

{% assign example = site.data.examples | where: "title", "Materials" | first %}
Vous pouvez exécuter cet exemple dans votre navigateur : [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant.
Pour créer la géométrie et exécuter 10 événements :

```shell
cp -r $GEMC_HOME/examples/basic/material .
cd material
./materials.py
gemc materials.yaml -n=10
```

<br/>

## Géométrie

La géométrie est définie dans `materials.py`.

Le monde (une boîte nommée %%root%%) contient cinq tubes identiques placés le long de l'axe z.
Tous les tubes ont la même forme : 10 cm de diamètre et 1 cm d'épaisseur. Ils sont disposés à partir de
z = 0, avec un espace de 3 cm entre eux.
Ils ne diffèrent que par leur couleur et la définition de leur matériau :

| Tube | Nom du volume | Matériau | Méthode de définition |
|------|-------------|----------|-------------------|
| 1 | %%tube_carbon%% | %%G4_C%% | Intégré à Geant4 (graphite) |
| 2 | %%tube_water%% | %%custom_water%% | Composition moléculaire (H2O) |
| 3 | %%tube_mixture%% | %%air_water_mixture%% | Fractions massiques (80 % d'air, 20 % d'eau) |
| 4 | %%tube_scintillator%% | %%my_scintillator%% | Type NaI avec propriétés de scintillation |
| 5 | %%tube_optical%% | %%optical_glass%% | SiO2 avec indice de réfraction |


Visualiseur interactif :

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/materials/material.vtksz"
  title="Interactive VTK.js view of the materials geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>


## Définitions des matériaux

### Tube 1 — Matériau intégré à Geant4

Le cas le plus simple : affecter directement un nom de la
[base de données de matériaux de Geant4](https://geant4.web.cern.ch/documentation/dev/bfad_html/ForApplicationDevelopers/Appendix/materialNames.html)
à `gvolume.material` :

```python
tube1.material = "G4_C"
```

Aucun objet `GMaterial` n'est nécessaire ; GEMC résout le nom au moment de l'exécution.

<br/>

### Tube 2 — Composition moléculaire

Utilisez `GMaterial` et `addNAtoms` pour spécifier les atomes et leur nombre dans la formule chimique :

```python
water = GMaterial("custom_water")
water.description = "Water defined by molecular composition (H2O)"
water.density = 1.0          # g/cm3
water.addNAtoms("H", 2)
water.addNAtoms("O", 1)
water.publish(cfg)
```

Le nombre total d'atomes doit être supérieur à 1.

<br/>

### Tube 3 — Fractions massiques

Utilisez `addMaterialWithFractionalMass` pour mélanger des matériaux existants selon leurs fractions massiques.
La somme des fractions doit être exactement égale à 1 :

```python
mixture = GMaterial("air_water_mixture")
mixture.description = "80% air / 20% water mixture"
mixture.density = 0.9601     # g/cm3
mixture.addMaterialWithFractionalMass("G4_AIR",   0.80)
mixture.addMaterialWithFractionalMass("G4_WATER", 0.20)
mixture.publish(cfg)
```

<br/>

### Tube 4 — Propriétés de scintillation

Définissez `photonEnergy` et les champs de scintillation pour activer l'émission de photons optiques.
Toutes les grandeurs dépendant de l'énergie doivent comporter le même nombre d'entrées que `photonEnergy` :

```python
scintillator = GMaterial("my_scintillator")
scintillator.density = 3.67   # g/cm3
scintillator.addNAtoms("Na", 1)
scintillator.addNAtoms("I",  1)
scintillator.photonEnergy       = "2.0*eV 2.5*eV 3.0*eV 3.5*eV 4.0*eV"
scintillator.fastcomponent      = "1.0 0.9 0.8 0.7 0.6"
scintillator.slowcomponent      = "0.5 0.4 0.3 0.2 0.1"
scintillator.scintillationyield = 38000   # photons/MeV
scintillator.resolutionscale    = 1.0
scintillator.fasttimeconstant   = 6       # ns
scintillator.slowtimeconstant   = 88      # ns
scintillator.yieldratio         = 0.8
scintillator.birksConstant      = 0.00152
scintillator.publish(cfg)
```


<br/>

### Tube 5 — Indice de réfraction (Tcherenkov)

Définissez `photonEnergy`, `indexOfRefraction` et, éventuellement, `absorptionLength` pour activer le
rayonnement Tcherenkov dans le matériau. Cela reprend l'approche utilisée dans cet
[exemple de rayonnement Tcherenkov](/home/examples/optical/cherenkov) :

```python
optical_glass = GMaterial("optical_glass")
optical_glass.density = 2.5   # g/cm3
optical_glass.addNAtoms("Si", 1)
optical_glass.addNAtoms("O",  2)
optical_glass.photonEnergy      = "2.0*eV 3.0*eV 4.0*eV 5.0*eV"
optical_glass.indexOfRefraction = "1.458 1.466 1.476 1.490"
optical_glass.absorptionLength  = "3*m 3*m 3*m 3*m"
optical_glass.publish(cfg)
```

<br/>

## Liste de physique

`FTFP_BERT + G4OpticalPhysics` est sélectionné dans le fichier YAML afin que les photons optiques issus de la
scintillation et du rayonnement Tcherenkov soient suivis.

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics
```

{% include notes/physics-list-note.md %}

<br/>

## Générateur

La cinématique des particules est définie dans le fichier YAML :

```yaml
gparticle:
  - name: proton
    p: 2000*MeV
    vz: -2*cm
    delta_vx: 0.1*cm
    delta_vy: 0.1*cm
    multiplicity: 1
```

Consultez également la [documentation du générateur interne]( /home/documentation/generator/internal ) pour
plus d'informations.

<br/>

## Utilisation

### Construction du détecteur

```shell
./materials.py
```

Consultez également la [documentation sur la construction de la géométrie]( /home/documentation/geometry/geometry_building )
pour plus d'informations.

<br/>

### Exécution de GEMC

```shell
gemc materials.yaml -n=10
```

Les annotations et décorations de la scène sont conservées dans `annotations.yaml`. Exécutez le fichier YAML
principal seul pour une vue épurée, ou passez les deux fichiers YAML pour inclure les étiquettes et
l'indication d'échelle :

```shell
gemc materials.yaml -n=10
gemc materials.yaml annotations.yaml -n=10
```

Ajoutez `-gui` pour exécuter en mode interactif.

<br/>

## Exécution des événements

{% include figure.html
src="/assets/images/examples/materials/gemc_view.png"
caption="Materials simulation: particles traversing the material samples."
%}

<br/>

## Sortie

Deux flux de sortie sont configurés dans le fichier YAML :

```yaml
gstreamer:
  - format: csv
    filename: material
```

Consultez également la [documentation sur les sorties]( /home/documentation/output ) pour plus d'informations.
