---
layout: default
title: "CLAS12 EC"
permalink: /examples/clas12/ec.html
lang: fr
human_reviewed: false
---

# Exemple du calorimètre électromagnétique de CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple présente la géométrie du calorimètre électromagnétique (EC) de CLAS12 issue de `clas12-systems`.

{% assign example = site.data.examples | where: "title", "EC" | first %}

<br/>

## Démarrage rapide

Depuis le dépôt `clas12-systems`, construisez la base de données de géométrie et lancez une courte simulation :

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ec
./ec.py
gemc ec.yaml -n=1
```

<br/>

## Géométrie

La géométrie, présentée ci-dessous, est définie dans `geometry_src/ec/ec.py` et `geometry_src/ec/geometry.py`.
Le constructeur de l'EC lit la fabrique de géométrie locale de coatjava, convertit les secteurs, les couvercles,
les absorbeurs en plomb et les bandes de scintillateur du calorimètre de CLAS12 en volumes GEMC, puis les
enregistre dans `gemc.db`.

Le monde (une boîte nommée %%root%%) contient :

- six volumes parents de secteur nommés %%ec_s1%% à %%ec_s6%%
- trois couches de couvercle par secteur (%%eclid1%% à %%eclid3%%) : deux peaux en acier inoxydable et une âme
  en Last-a-Foam
- des couches d'absorbeur en plomb nommées %%lead_<layer>_s<sector>_view_<view>_stack_<stack>%%
- des bandes de scintillateur U, V et W nommées %%U_strip_...%%, %%V_strip_...%% et %%W_strip_...%%

La géométrie de l'EC est de grande taille ; l'exemple définit donc `pyvista-fast: true` dans `_data/examples.yml`
pour utiliser le mode de rendu rapide de PyVista lors de l'exportation de la vue interactive ci-dessous.

Visionneuse interactive :

{% assign ec_vtksz = "/home/assets/images/examples/ec/ec.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ec_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 EC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Liste de physique

`FTFP_BERT` est utilisée par défaut, sélectionnée dans le fichier YAML avec `phys_list: FTFP_BERT`.

{% include notes/physics-list-note.md %}

<br/>

## Générateur

La cinématique des particules est définie dans le fichier YAML :

```yaml
gparticle:
  - name: e-
    p: 5000*MeV
    delta_p: 1*GeV
    theta: 25*deg
    delta_theta: 15*deg
    randomThetaModel: cosine
    phi: 60*deg
    delta_phi: 180*deg
```

Consultez aussi la [documentation du générateur interne]( /home/documentation/generator/internal ) pour plus
d'informations.

<br/>

## Numérisation

Les bandes de scintillateur utilisent le plugin de numérisation %%ec%% propre à CLAS12. Les identifiants
enregistrent les numéros de secteur, de couche et de bande :

```python
gvolume.digitization = "ec"
gvolume.set_identifier("sector", sector, "layer", hipo_layer, "strip", strip)
```

<br/>

## Utilisation

### Construction du détecteur

Utilisez `geometry_src/ec/ec.py` pour construire le détecteur. Par défaut, la configuration est stockée dans
un fichier SQLite nommé `gemc.db`.

Consultez aussi la [documentation sur la construction de la géométrie]( /home/documentation/geometry/geometry_building )
pour plus d'informations.

<br/>

### Exécution de GEMC

Le fichier `ec.yaml` permet d'exécuter la simulation avec cette configuration. Ajoutez `-gui` pour l'exécuter
en mode interactif :

```shell
gemc ec.yaml -gui
```

Modifiez `ec.yaml` selon vos besoins, notamment pour ajouter des particules, contrôler le nombre de threads
ou changer la sortie.

<br/>

## Simulation des événements

{% include figure.html
src="/assets/images/examples/ec/gemc_view.png"
caption="CLAS12 EC simulation: generated electrons showering in the electromagnetic calorimeter geometry."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne les noms et les formats des fichiers de sortie :

```yaml
gstreamer:
  - format: csv
    filename: ec
  - format: hipo
    filename: ec
```

Consultez aussi la [documentation sur la sortie]( /home/documentation/output ) pour plus d'informations.


## Tracé de graphiques avec l'analyseur GEMC

Lancez d'abord GEMC avec 2 000 événements. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc ec.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Tracez l'énergie totale déposée par impact :

```shell
gemc-analyzer ec_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![Énergie totale déposée par impact dans l'EC][ec-analyzer_totEdep]{:width="70%"}

[ec-analyzer_totEdep]: /home/assets/images/examples/ec/analyzer_totEdep.png

Tracez les positions des impacts en y en fonction de x :

```shell
gemc-analyzer ec_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![Positions des impacts dans l'EC en y en fonction de x][ec-analyzer_yvsx]{:width="70%"}

[ec-analyzer_yvsx]: /home/assets/images/examples/ec/analyzer_yvsx.png
