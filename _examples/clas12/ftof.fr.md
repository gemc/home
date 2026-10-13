---
layout: default
title: "CLAS12 FTOF"
permalink: /examples/clas12/ftof.html
lang: fr
human_reviewed: false
---

# Exemple du détecteur de temps de vol avant de CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple présente la géométrie du détecteur de temps de vol avant (FTOF) de CLAS12 issue de `clas12-systems`.

{% assign example = site.data.examples | where: "title", "FTOF" | first %}

<br/>

## Démarrage rapide

Depuis le dépôt `clas12-systems`, construisez la base de données de géométrie et lancez une courte simulation :

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ftof
./ftof.py
gemc ftof.yaml -n=1
```

<br/>

## Géométrie

La géométrie, présentée ci-dessous, est définie dans `geometry_src/ftof/ftof.py` et `geometry_src/ftof/geometry.py`.
L'outil de construction FTOF lit la fabrique de géométrie locale de coatjava, convertit les panneaux du détecteur
de temps de vol avant de CLAS12 et les barreaux scintillants en volumes GEMC, puis les enregistre dans `gemc.db`.

Le monde (une boîte nommée %%root%%) contient, pour chacun des six secteurs :

- trois volumes mères de panneau nommés %%ftof_p1a_s<sector>%%, %%ftof_p1b_s<sector>%% et %%ftof_p2_s<sector>%%
- des barreaux scintillants nommés %%panel1a_sector<sector>_paddle_<n>%% (23 barreaux), %%panel1b_...%% (62) et
  %%panel2_...%% (5)
- un blindage en plomb derrière les panneaux 1a et 2 nommé %%ftof_shield_p1a_sector<sector>%% et
  %%ftof_shield_p2_sector<sector>%%

Visualiseur interactif :

{% assign ftof_vtksz = "/home/assets/images/examples/ftof/ftof.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ftof_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 FTOF geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Liste de physique

`FTFP_BERT` est utilisée par défaut et sélectionnée dans le fichier YAML avec `phys_list: FTFP_BERT`.

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
    delta_phi: 180*deg
```

Voir aussi la [documentation du générateur interne]( /home/documentation/generator/internal ) pour en savoir plus.

<br/>

## Numérisation

Les barreaux scintillants utilisent le plugin de numérisation %%ftof%% propre à CLAS12. Chaque barreau est lu
aux deux extrémités : le plugin répartit donc chaque impact entre deux canaux de photomultiplicateurs (PMT),
gauche (Left) et droit (Right). Les identifiants indiquent le secteur, le panneau, le barreau et le côté du PMT :

```python
gvolume.digitization = "ftof"
gvolume.set_identifier("sector", sector, "panel", layer, "paddle", paddle, "side", 0)
```

<br/>

## Utilisation

### Construction du détecteur

Utilisez `geometry_src/ftof/ftof.py` pour construire le détecteur. Par défaut, la configuration est stockée
dans un fichier SQLite nommé `gemc.db`.

Voir aussi la [construction de la géométrie]( /home/documentation/geometry/geometry_building ) pour en savoir plus.

<br/>

### Exécution de GEMC

Le fichier `ftof.yaml` peut être utilisé pour lancer la simulation. Ajoutez `-gui` pour une exécution interactive :

```shell
gemc ftof.yaml -gui
```

Modifiez `ftof.yaml` selon vos besoins, en particulier pour ajouter des particules, contrôler le nombre de
threads ou modifier la sortie.

<br/>

## Simulation d'événements

{% include figure.html
src="/assets/images/examples/ftof/gemc_view.png"
caption="CLAS12 FTOF simulation: generated electrons crossing the forward time-of-flight geometry."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne les noms de fichiers et les formats de sortie :

```yaml
gstreamer:
  - format: csv
    filename: ftof
  - format: hipo
    filename: ftof
```

Voir aussi la [documentation sur la sortie]( /home/documentation/output ) pour en savoir plus.


## Tracé avec l'analyseur GEMC

Lancez d'abord GEMC avec 2 000 événements. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc ftof.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Tracez l'énergie totale déposée par impact :

```shell
gemc-analyzer ftof_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![Énergie totale déposée par impact dans le FTOF][ftof-analyzer_totEdep]{:width="70%"}

[ftof-analyzer_totEdep]: /home/assets/images/examples/ftof/analyzer_totEdep.png

Tracez les coordonnées y des impacts en fonction de leurs coordonnées x :

```shell
gemc-analyzer ftof_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![Positions des impacts dans le FTOF : y en fonction de x][ftof-analyzer_yvsx]{:width="70%"}

[ftof-analyzer_yvsx]: /home/assets/images/examples/ftof/analyzer_yvsx.png
