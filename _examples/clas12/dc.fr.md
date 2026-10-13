---
layout: default
title: "CLAS12 DC"
permalink: /examples/clas12/dc.html
lang: fr
human_reviewed: false
---

# Exemple de chambre à dérive CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple présente la géométrie de la chambre à dérive CLAS12 issue de `clas12-systems`.

{% assign example = site.data.examples | where: "title", "DC" | first %}

<br/>

## Démarrage rapide

Depuis le dépôt `clas12-systems`, construisez la base de données de géométrie et lancez une courte simulation :

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/dc
./dc.py
gemc dc.yaml -n=1
```

<br/>

## Géométrie

La géométrie, présentée ci-dessous, est définie dans `geometry_src/dc/dc.py` et `geometry_src/dc/geometry.py`.
L'outil de construction DC lit la fabrique de géométrie locale de coatjava, convertit les régions et
supercouches de la chambre à dérive CLAS12 en volumes GEMC, puis les enregistre dans `gemc.db`.

Le monde (une boîte nommée %%root%%) contient :

- six secteurs de volumes mères des régions nommés %%region1_s1%% à %%region3_s6%%
- six secteurs de volumes de supercouches nommés %%sl1_s1%% à %%sl6_s6%%

Visualiseur interactif :

{% assign dc_vtksz = "/home/assets/images/examples/dc/dc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ dc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 DC geometry"
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

Consultez également la [documentation du générateur interne]( /home/documentation/generator/internal ) pour
plus d'informations.

<br/>

## Numérisation

Les volumes sensibles des supercouches utilisent le plugin de numérisation %%dc%% spécifique à CLAS12.
Les identifiants enregistrent les numéros de secteur, de supercouche, de couche et de fil :

```python
gvolume.digitization = "dc"
gvolume.set_identifier("sector", sector, "superlayer", superlayer, "layer", 1, "wire", 1)
```

<br/>

## Utilisation

### Construction du détecteur

Utilisez `geometry_src/dc/dc.py` pour construire le détecteur. Par défaut, la configuration est stockée dans un
fichier SQLite nommé `gemc.db`.

Consultez également la section [Construction de la géométrie]( /home/documentation/geometry/geometry_building )
pour plus d'informations.

<br/>

### Exécution de GEMC

Le fichier `dc.yaml` peut être utilisé pour exécuter la configuration. Ajoutez `-gui` pour une exécution
interactive :

```shell
gemc dc.yaml -gui
```

Modifiez `dc.yaml` selon vos besoins, en particulier pour ajouter des particules, contrôler le nombre de
threads ou modifier la sortie.

<br/>

## Exécution des événements

{% include figure.html
src="/assets/images/examples/dc/gemc_view.png"
caption="CLAS12 DC simulation: generated electrons crossing the drift chamber geometry."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne les noms de fichiers et les formats de sortie :

```yaml
gstreamer:
  - format: csv
    filename: dc
  - format: hipo
    filename: dc
```

Consultez également la [documentation sur la sortie]( /home/documentation/output ) pour plus d'informations.


## Tracé avec l'analyseur GEMC

Exécutez d'abord GEMC avec 2 000 événements. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc dc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Tracez l'énergie totale déposée par impact :

```shell
gemc-analyzer dc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![Énergie totale déposée par impact dans la DC][dc-analyzer_totEdep]{:width="70%"}

[dc-analyzer_totEdep]: /home/assets/images/examples/dc/analyzer_totEdep.png

Tracez les positions des impacts en y en fonction de x :

```shell
gemc-analyzer dc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![Positions des impacts dans la DC en y en fonction de x][dc-analyzer_yvsx]{:width="70%"}

[dc-analyzer_yvsx]: /home/assets/images/examples/dc/analyzer_yvsx.png

Tracez le temps TDC numérisé :

```shell
gemc-analyzer dc_t0_digitized.csv TDC_TDC --kind csv
```

![Temps TDC numérisé dans la DC][dc-analyzer_tdc]{:width="70%"}

[dc-analyzer_tdc]: /home/assets/images/examples/dc/analyzer_tdc.png
