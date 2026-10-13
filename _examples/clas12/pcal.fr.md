---
layout: default
title: "CLAS12 PCAL"
permalink: /examples/clas12/pcal.html
lang: fr
human_reviewed: false
---

# Exemple du calorimètre Preshower de CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple présente la géométrie du calorimètre Preshower (PCAL) de CLAS12 issue de `clas12-systems`.

{% assign example = site.data.examples | where: "title", "PCAL" | first %}

<br/>

## Démarrage rapide

Depuis le dépôt `clas12-systems`, construisez la base de données de géométrie et lancez une courte simulation :

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/pcal
./pcal.py
gemc pcal.yaml -n=1
```

<br/>

## Géométrie

La géométrie, présentée ci-dessous, est définie dans `geometry_src/pcal/pcal.py` et
`geometry_src/pcal/geometry.py`. Le constructeur PCAL lit la fabrique de géométrie locale de coatjava,
convertit les secteurs du calorimètre preshower de CLAS12, les fenêtres, les couches de plomb, les couches
de scintillateur ainsi que les volumes de bandes U, V et W en volumes GEMC, et les stocke dans `gemc.db`.

Le monde (une boîte nommée %%root%%) contient, pour chacun des six secteurs :

- des volumes mères de secteur nommés %%pcal_s1%% à %%pcal_s6%%
- des fenêtres en acier inoxydable avant et arrière nommées %%Stainless_Steel_Front_...%% et
  %%Stainless_Steel_Back_...%%
- des fenêtres Last-a-Foam avant et arrière nommées %%Last-a-Foam_Front_...%% et %%Last-a-Foam_Back_...%%
- des couches de plomb nommées %%PCAL_Lead_Layer_<layer>_s<sector>%%
- des mères de couche de scintillateur U, V et W ainsi que des volumes de bandes simples/doubles

Le PCAL est une géométrie de grande taille, c'est pourquoi l'exemple définit `pyvista-fast: true` dans
`_data/examples.yml` afin d'utiliser le chemin de rendu rapide de PyVista lors de l'export de la vue
interactive ci-dessous.

Visualiseur interactif :

{% assign pcal_vtksz = "/home/assets/images/examples/pcal/pcal.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ pcal_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 PCAL geometry"
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
    delta_phi: 180*deg
```

Consultez également la [documentation du générateur interne]( /home/documentation/generator/internal ) pour
plus d'informations.

<br/>

## Numérisation

Les bandes de scintillateur utilisent le plugin de numérisation CLAS12 partagé %%ecal%%. Le PCAL écrit dans
les mêmes banques ECAL que le système EC, en utilisant les couches hipo 1 à 3. Les identifiants enregistrent
les numéros de secteur, de couche et de bande :

```python
gvolume.digitization = "ecal"
gvolume.set_identifier("sector", sector, "layer", layer, "strip", pcal_strip_id(uvw, kind, strip))
```

<br/>

## Utilisation

### Construction du détecteur

Utilisez `geometry_src/pcal/pcal.py` pour construire le détecteur. Par défaut, la configuration est stockée
dans un fichier SQLite nommé `gemc.db`.

Consultez également la [construction de la géométrie]( /home/documentation/geometry/geometry_building ) pour
plus d'informations.

<br/>

### Exécution de GEMC

Le fichier `pcal.yaml` peut être utilisé pour exécuter la configuration. Ajoutez `-gui` pour l'exécuter de
façon interactive :

```shell
gemc pcal.yaml -gui
```

Modifiez `pcal.yaml` selon vos besoins, en particulier pour ajouter des particules, contrôler le nombre de
threads ou changer la sortie.

<br/>

## Exécution des événements

{% include figure.html
src="/assets/images/examples/pcal/gemc_view.png"
caption="CLAS12 PCAL simulation: generated electrons crossing the preshower calorimeter geometry."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne les noms de fichiers et les formats de sortie :

```yaml
gstreamer:
  - format: csv
    filename: pcal
  - format: hipo
    filename: pcal
```

Consultez également la [documentation sur la sortie]( /home/documentation/output ) pour plus d'informations.


## Tracé de graphiques avec l'analyseur GEMC

Exécutez d'abord GEMC avec 2 000 événements. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc pcal.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Tracez l'énergie totale déposée par coup :

```shell
gemc-analyzer pcal_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![pcal total energy deposited per hit][pcal-analyzer_totEdep]{:width="70%"}

[pcal-analyzer_totEdep]: /home/assets/images/examples/pcal/analyzer_totEdep.png

Tracez les positions de coups y en fonction de x :

```shell
gemc-analyzer pcal_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![pcal y vs x hit positions][pcal-analyzer_yvsx]{:width="70%"}

[pcal-analyzer_yvsx]: /home/assets/images/examples/pcal/analyzer_yvsx.png
