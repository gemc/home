---
layout: default
title: "Cherenkov"
permalink: /examples/optical/cherenkov.html
lang: fr
human_reviewed: false
---

[low-img]: /home/assets/images/examples/cherenkov/low_index_radiator.png
[medium-img]: /home/assets/images/examples/cherenkov/medium_index_radiator.png
[high-img]: /home/assets/images/examples/cherenkov/high_index_radiator.png
[lowy-img]: /home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png
[mediumy-img]: /home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png
[highy-img]: /home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png


# Exemple Cherenkov
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple montre comment activer le rayonnement Cherenkov dans un détecteur GEMC.
Les trois noms de radiateurs sont des étiquettes de démonstration neutres. Leurs constantes optiques peuvent être
non physiques et ne doivent pas être interprétées comme des définitions de matériaux réels.

{% assign example = site.data.examples | where: "title", "Cherenkov" | first %}

Vous pouvez exécuter cet exemple dans votre navigateur : [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant.
Pour créer la géométrie, exécuter 1 événement et produire des fichiers de sortie ROOT et CSV :

```shell
cp -r $GEMC_HOME/examples/optical/cherenkov .
cd cherenkov
./cherenkov.py
gemc cherenkov.yaml -n=1
```

<br/>

## Géométrie

La géométrie, présentée ci-dessous, est définie dans `cherenkov.py`. Elle est produite en trois variations :
%%default%%, %%mediumIndexRadiator%% et %%highIndexRadiator%%.

Le monde (une boîte nommée %%root%%) contient une boîte %%radiator%%. Le matériau du radiateur dépend de la variation sélectionnée :

{:.zebra .compact-table}

| variation | matériau | couleur | plage d'indice de réfraction |
|-----------|----------|---------|------------------------------|
| %%default%% | %%lowIndexRadiator%% | rouge | 1.0010-1.0013 |
| %%mediumIndexRadiator%% | %%mediumIndexRadiator%% | bleu | 1.0110-1.0150 |
| %%highIndexRadiator%% | %%highIndexRadiator%% | vert | 1.0500-1.0530 |


- un détecteur %%gPhotonDetector%% composé de quatre boîtes (%%detector_left%%, %%detector_right%%, %%detector_top%% et %%detector_bottom%%). Cela laisse un petit trou au centre pour le faisceau.

Visualiseur interactif :

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/cherenkov/cherenkov.vtksz"
  title="Interactive VTK.js view of the Cherenkov geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="/assets/images/examples/cherenkov/high_index_radiator.png"
caption="Cherenkov geometry with 1 generated electron. The highIndexRadiator volume (green, style = 2 renders it as a cloud) is the medium generating Cherenkov radiation."
%}


<br/>

## Liste de physique

`FTFP_BERT + G4OpticalPhysics` est utilisée par défaut dans le fichier YAML. Le composant de physique optique est requis pour produire des photons optiques.

{% include notes/physics-list-note.md %}

<br/>

## Générateur

La cinématique des particules est définie dans le fichier YAML :

```yaml
gparticle:
  - name: e-
    p: 1000*MeV
    vz: -50*cm
```

Consultez également la [documentation du générateur interne]( /home/documentation/generator/internal ) pour plus d'informations.


<br/>


## Numérisation

Les sensibilités des volumes du détecteur sont spécifiées avec la numérisation %%gPhotonDetector%% (l'une des routines GEMC préintégrées disponibles)
dans `cherenkov.py`.

L'%%identifier%% est utilisé pour distinguer les différentes boîtes du détecteur :

```python
backplate.digitization = "gPhotonDetector"
backplate.set_identifier("detector", panel_id)
```

Consultez la [documentation sur le flux]( /home/documentation/sensitivity/gPhotonDetector ) pour plus d'informations.


<br/>

## Utilisation

### Construction du détecteur

Utilisez le script Python `cherenkov.py` pour construire le détecteur. Par défaut, la configuration est stockée dans un fichier SQLite
nommé `gemc.db`. Les options en ligne de commande peuvent définir le type de base de données, les variations et le numéro de run.

Consultez également la [construction de la géométrie]( /home/documentation/geometry/geometry_building ) pour plus d'informations.

<br/>

### Exécution de GEMC

Le fichier `cherenkov.yaml` peut être utilisé pour lancer la configuration. Ajoutez `-gui` pour un fonctionnement interactif :

```shell
gemc cherenkov.yaml -gui
```

Le YAML définit `g4view.cloudPoints: 60000` afin que les volumes de style nuage soient suffisamment denses pour les captures d'écran de la géométrie rendue.

Modifiez `cherenkov.yaml` selon vos besoins, en particulier pour ajouter des particules, contrôler le nombre de threads ou changer la sortie.
La numérisation %%gPhotonDetector%% enregistre les photons optiques même lorsqu'ils ne déposent aucune énergie, de sorte que %%recordZeroEdep%%
n'est pas requis pour cet exemple.

<br/>

### Variations

Dans le fichier YAML, la variation est définie sur %%mediumIndexRadiator%%. Vous pouvez la remplacer par %%default%% ou %%highIndexRadiator%%
pour changer le matériau. Par exemple :

```yaml
gsystem:
  - name: cherenkov
    variation: highIndexRadiator
```

Différents matériaux de radiateur produisent différents rendements et angles de photons, comme illustré ci-dessous.
Leurs constantes optiques sont des valeurs de démonstration et peuvent être non physiques.
Utilisez le nom de la variation dans le nom de fichier %%gstreamer%% lorsque vous souhaitez des fichiers de sortie distincts pour chaque variation.


<br/>

|:---:|:---:|:---:|
| ![low index radiator](/home/assets/images/examples/cherenkov/low_index_radiator.png) | ![medium index radiator](/home/assets/images/examples/cherenkov/medium_index_radiator.png) | ![high index radiator](/home/assets/images/examples/cherenkov/high_index_radiator.png) |
| ![low index radiator y vs x](/home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png) | ![medium index radiator y vs x](/home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png) | ![high index radiator y vs x](/home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png) |

<p class="image-caption">
  Gauche : <span class="gstring">lowIndexRadiator</span>, Centre : <span class="gstring">mediumIndexRadiator</span>, Droite : <span class="gstring">highIndexRadiator</span>.
</p>

<br/>

## Exécution des événements

{% include figure.html
src="/assets/images/examples/cherenkov/gemc_view.png"
caption="Cherenkov simulation: electron beam entering the radiator volume."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne les noms de fichiers de sortie et le format :


```yaml
gstreamer:
  - format: csv
    filename: cherenkov
```

Comme %%gPhotonDetector%% est une numérisation par événement, GEMC produira un fichier de sortie par thread.
Pour les fichiers ROOT, vous pouvez utiliser `hadd` pour fusionner les fichiers.

Consultez également la [documentation sur la sortie]( /home/documentation/output ) pour plus d'informations.

<br/>

## Tracé avec l'analyseur GEMC

Exécutez d'abord GEMC avec 1 événement. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc cherenkov.yaml -n=1
```

Tracez l'énergie totale déposée par coup :

```shell
gemc-analyzer cherenkov_t0_digitized.csv totEdep --kind csv
```

![cherenkov total energy deposited per hit][cherenkov-analyzer_totEdep]{:width="70%"}

[cherenkov-analyzer_totEdep]: /home/assets/images/examples/cherenkov/analyzer_totEdep.png

Tracez les positions des coups y en fonction de x :

```shell
gemc-analyzer cherenkov_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![cherenkov y vs x hit positions][cherenkov-analyzer_yvsx]{:width="70%"}

[cherenkov-analyzer_yvsx]: /home/assets/images/examples/cherenkov/analyzer_yvsx.png
