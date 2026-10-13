---
layout: default
title: "Simple flux"
permalink: /examples/basic/simple_flux.html
lang: fr
human_reviewed: false
---

# Détecteur de flux simple
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple utilise la numérisation %%flux%% pour enregistrer les informations de vérité et les informations
numérisées dans la sortie.

{% assign example = site.data.examples | where: "title", "Simple Flux" | first %}

Vous pouvez exécuter cet exemple dans votre navigateur : [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant.
Pour créer la géométrie, exécuter 10 événements et produire des fichiers de sortie ROOT et CSV :

```shell
cp -r $GEMC_HOME/examples/basic/simple_flux .
cd simple_flux
./simple_flux.py
gemc simple_flux.yaml -n=10
```

<br/>

## Géométrie

La géométrie, présentée ci-dessous, est définie dans `simple_flux.py`.

Le monde (une boîte nommée %%root%%) contient :

- %%target%%, une cible cylindrique d'hydrogène liquide (%%G4_lH2%%)
- %%FluxPlane%%, une boîte constituée d'air (%%G4_AIR%%) à laquelle est affectée la numérisation %%flux%%


Visualiseur interactif :

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/simple_flux/simple_flux.vtksz"
  title="Interactive VTK.js view of the simple_flux geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>


<br/>

## Liste de physique

`QBBC` est utilisée par défaut et sélectionnée dans le fichier YAML avec `phys_list: QBBC`.

{% include notes/physics-list-note.md %}

<br/>


## Générateur

La cinématique des particules est définie dans le fichier YAML :

```yaml
gparticle:
  - name: proton
    p: 2000*MeV
    vz: -3*cm
    delta_vx: 0.1*cm
    delta_vy: 0.1*cm
    multiplicity: 10
```

Consultez également la [documentation du générateur interne]( /home/documentation/generator/internal )
pour plus d'informations.

<br/>


## Numérisation

La sensibilité de %%FluxPlane%% est définie dans `simple_flux.py` par la numérisation %%flux%%
(l'une des routines prédéfinies disponibles dans GEMC), avec l'identifiant %%flux_plane = 1%%.

```python
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
```

Dans ce cas, %%identifier%% contient un seul nom : %%flux_plane%%.

Consultez la [documentation du flux]( /home/documentation/sensitivity/flux ) pour plus d'informations.


En plus des variables numérisées, les informations de vérité sont enregistrées dans le flux de sortie.

{% include notes/true_info-note.md %}


<br/>

## Utilisation

### Construction du détecteur

Utilisez le script Python `simple_flux.py` pour construire le détecteur. Par défaut, la configuration est stockée
dans un fichier SQLite nommé `gemc.db`. Les options en ligne de commande permettent de définir le type de base de
données, les variations et le numéro de run.

Consultez également la [documentation sur la construction de la géométrie]( /home/documentation/geometry/geometry_building )
pour plus d'informations.


<br/>

### Exécution de GEMC

Le fichier `simple_flux.yaml` permet d'exécuter la configuration. Ajoutez `-gui` pour une exécution interactive :

```shell
gemc simple_flux.yaml -gui
```

Modifiez `simple_flux.yaml` selon vos besoins, en particulier pour ajouter des particules, contrôler le nombre de
threads ou modifier la sortie.

<br/>

## Exécution des événements

{% include figure.html
src="/assets/images/examples/simple_flux/gemc_view.png"
caption="Simple flux simulation: proton tracks traversing the flux detector volumes."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne les noms des fichiers de sortie et le format :

```yaml
gstreamer:
  - format: csv
    filename: simple_flux
```

Comme %%flux%% est une numérisation par événement, GEMC produira un fichier de sortie par thread.
Pour les fichiers ROOT, vous pouvez utiliser `hadd` pour fusionner les fichiers.


Consultez également la [documentation sur les sorties]( /home/documentation/output ) pour plus d'informations.


<br/>

## Tracé avec l'analyseur GEMC

Exécutez d'abord GEMC avec 10 000 événements. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc simple_flux.yaml -n=10000
```

Tracez l'énergie totale déposée par hit :

```shell
gemc-analyzer simple_flux_t0_digitized.csv totEdep --kind csv
```

![simple_flux : énergie totale déposée par hit][simple_flux-analyzer_totEdep]{:width="70%"}

[simple_flux-analyzer_totEdep]: /home/assets/images/examples/simple_flux/analyzer_totEdep.png

Tracez l'énergie vraie associée à la trajectoire de la particule :

```shell
gemc-analyzer simple_flux_t0_true_info.csv E --kind csv --data true_info
```

![simple_flux : énergie vraie associée à la trajectoire de la particule][simple_flux-analyzer_true_energy]{:width="70%"}

[simple_flux-analyzer_true_energy]: /home/assets/images/examples/simple_flux/analyzer_true_energy.png
