---
layout: default
title: "CLAS12 FT"
permalink: /examples/clas12/ft.html
lang: fr
human_reviewed: false
---

# Exemple du Forward Tagger de CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple présente la géométrie du Forward Tagger (FT) de CLAS12 issue de `clas12-systems`. Le FT se situe
à de petits angles polaires et se compose de trois sous-systèmes : un calorimètre électromagnétique, un
hodoscope à scintillateurs et un trajectographe Micromegas.

La géométrie et la numérisation du FT sont disponibles dans `clas12-systems` 0.3 avec GEMC 0.5 et `pygemc` 0.5.0.

{% assign example = site.data.examples | where: "title", "FT" | first %}

<br/>

## Démarrage rapide

Depuis le dépôt `clas12-systems`, construisez la base de données de géométrie et lancez une courte simulation :

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ft
./ft.py
gemc ft.yaml -n=1
```

<br/>

## Géométrie

La géométrie, illustrée ci-dessous, est définie dans `geometry_src/ft/geometry.py` et construite par
`geometry_src/ft/ft.py`. Le constructeur du FT assemble les trois sous-systèmes dans un seul fichier `gemc.db` :

- le **calorimètre**, une matrice de cristaux de PbWO4, chacun enveloppé et couplé à une APD, nommés
  %%ft_cal_cr_h<ih>_v<iv>%%, ainsi que les volumes du boîtier en cuivre, de la carte mère et du blindage
- l'**hodoscope**, des tuiles de scintillateur nommées par secteur, couche et composant
- le **trajectographe**, des disques Micromegas avec des volumes de kapton, de photorésine et d'anneaux
  sur chaque couche et chaque côté

Le volume monde (une boîte nommée %%root%%) contient les trois sous-systèmes. Des détecteurs de flux sont ajoutés
au niveau du calorimètre et du trajectographe pour enregistrer le flux de particules incidentes.

Visualiseur interactif :

{% assign ft_vtksz = "/home/assets/images/examples/ft/ft.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ft_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 FT geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Liste de physique

`FTFP_BERT` est utilisée par défaut ; elle est sélectionnée dans le fichier YAML avec `phys_list: FTFP_BERT`.

{% include notes/physics-list-note.md %}

<br/>

## Générateur

La cinématique des particules est définie dans le fichier YAML :

```yaml
gparticle:
  - name: e-
    p: 2000*MeV
    theta: 3*deg
    phi: 10*deg
    delta_phi: 180*deg
```

Consultez aussi la [documentation du générateur interne]( /home/documentation/generator/internal ) pour en savoir plus.

<br/>

## Numérisation

Chaque sous-système du FT utilise son propre greffon de numérisation spécifique à CLAS12. Les cristaux du
calorimètre utilisent %%ft_cal%%, les tuiles de l'hodoscope utilisent %%ft_hodo%% et les disques du
trajectographe utilisent %%ft_trk%%. Les identifiants indiquent le composant lu, par exemple la ligne et
la colonne du cristal du calorimètre :

```python
digitization="ft_cal",
identifiers=("ih", ix, "iv", iy),
```

<br/>

## Utilisation

### Construction du détecteur

Utilisez `geometry_src/ft/ft.py` pour construire le détecteur. Par défaut, la configuration est enregistrée
dans un fichier SQLite nommé `gemc.db`.

Consultez aussi la [construction de la géométrie]( /home/documentation/geometry/geometry_building ) pour en savoir plus.

<br/>

### Exécution de GEMC

Le fichier `ft.yaml` peut être utilisé pour lancer la simulation avec cette configuration. Ajoutez `-gui`
pour une exécution interactive :

```shell
gemc ft.yaml -gui
```

Modifiez `ft.yaml` selon vos besoins, notamment pour ajouter des particules, contrôler le nombre de threads
ou changer la sortie.

<br/>

## Exécution d'événements

{% include figure.html
src="/assets/images/examples/ft/gemc_view.png"
caption="CLAS12 FT simulation: generated electrons crossing the forward tagger geometry."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne les noms de fichiers et les formats de sortie :

```yaml
gstreamer:
  - format: csv
    filename: ft
  - format: hipo
    filename: ft
```

Consultez aussi la [documentation des sorties]( /home/documentation/output ) pour en savoir plus.

Le Forward Tagger assure la lecture de trois détecteurs (%%ft_cal%%, %%ft_hodo%% et %%ft_trk%%) ayant des
structures d'identifiants différentes. L'exemple d'analyseur ci-dessous désactive la sortie des informations
de vérité de simulation et des données numérisées pour les détecteurs de flux, l'hodoscope et le trajectographe,
afin que le CSV contienne uniquement des données conformes au schéma %%ft_cal%%.


## Tracé avec l'analyseur GEMC

Exécutez d'abord GEMC avec 2 000 événements. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc ft.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build \
  -no_true_info="flux ft_hodo ft_trk" -no_digitized="flux ft_hodo ft_trk"
```

Tracez l'énergie totale déposée par impact :

```shell
gemc-analyzer ft_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![Énergie totale déposée par impact dans le FT][ft-analyzer_totEdep]{:width="70%"}

[ft-analyzer_totEdep]: /home/assets/images/examples/ft/analyzer_totEdep.png

Tracez les positions des impacts en y en fonction de x :

```shell
gemc-analyzer ft_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![Positions des impacts dans le FT en y en fonction de x][ft-analyzer_yvsx]{:width="70%"}

[ft-analyzer_yvsx]: /home/assets/images/examples/ft/analyzer_yvsx.png
