---
layout: default
title: "CLAS12 HTCC"
permalink: /examples/clas12/htcc.html
lang: fr
human_reviewed: false
---

# Exemple de compteur Cherenkov à seuil élevé de CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple présente la géométrie du compteur Cherenkov à seuil élevé (HTCC) de CLAS12 issue de
`clas12-systems`. Il combine l'optique native des miroirs GEMC avec des maillages CAO chargés via la
fonctionnalité `gcad`. Les deux systèmes sont stockés dans une seule base de données SQLite.

La géométrie et la numérisation du HTCC sont disponibles dans `clas12-systems` 0.3 avec GEMC 0.5 et
`pygemc` 0.5.0.

{% assign example = site.data.examples | where: "title", "HTCC" | first %}

<br/>

## Démarrage rapide

Depuis le dépôt `clas12-systems`, construisez la base de données de géométrie et lancez une courte simulation :

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/htcc
./htcc.py
gemc htcc.yaml -n=1
```

<br/>

## Géométrie

La géométrie, présentée ci-dessous, est définie dans `geometry_src/htcc/geometry.py` et orchestrée par
`geometry_src/htcc/htcc.py`. Les constructeurs natifs transposent les scripts Perl originaux de clas12Tags
(volume de gaz, fenêtres, 48 miroirs elliptiques et 48 tubes photomultiplicateurs), tandis que les trois cônes
de la ligne de faisceau sont importés sous forme de maillages CAO. Les enregistrements de géométrie native
utilisent le système SQLite %%htcc%% et les enregistrements de maillages utilisent le système CAO distinct
%%htcc_cad%%. Les deux partagent la même base de données, la même variation et le même numéro de run, de sorte
qu'un seul `gemc.db` charge le détecteur complet.

Le monde (une boîte nommée %%root%%) contient :

- le volume de gaz %%htcc%% construit par des opérations booléennes sur des polycônes, ainsi que les fenêtres
  %%htccEntryWindow%% et %%htccExitWindow%%
- 48 segments de miroirs elliptiques découpés dans une enveloppe en polycône et enregistrés avec la surface
  optique %%htcc_AlMgF2%%
- des tubes photomultiplicateurs nommés %%pmt_<ring>_sector<sector>_<half>%%, dont la lecture est organisée en
  deux demi-secteurs par secteur
- des coques paraboloïdales de cônes de Winston partageant le revêtement réfléchissant %%htcc_AlMgF2%%
- des cônes CAO de la ligne de faisceau (%%htccCone%%, %%htccMollerCone%%, %%htccMollerConeExt%%) placés sous
  %%root%%

Visualiseur interactif :

{% assign htcc_vtksz = "/home/assets/images/examples/htcc/htcc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ htcc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 HTCC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Liste de physique

Le HTCC est un détecteur Cherenkov ; les photons optiques doivent donc être produits et suivis. Le fichier YAML
sélectionne `FTFP_BERT + G4OpticalPhysics` avec `phys_list: FTFP_BERT + G4OpticalPhysics`.

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

Voir aussi la [documentation du générateur interne]( /home/documentation/generator/internal ) pour plus
d'informations.

<br/>

## Numérisation

Les tubes photomultiplicateurs utilisent le plugin de numérisation %%htcc%% spécifique à CLAS12. Les
identifiants enregistrent le secteur, l'anneau de miroirs et le demi-secteur dont le tube assure la lecture :

```python
pmt.digitization = "htcc"
pmt.set_identifier("sector", sector, "ring", ring, "half", hindex)
```

<br/>

## Utilisation

### Construction du détecteur

Utilisez `geometry_src/htcc/htcc.py` pour construire le détecteur. Le script définit les matériaux et les
surfaces des miroirs, publie les volumes natifs %%htcc%% et publie les trois cônes de la ligne de faisceau
sous forme de maillages CAO pour le système %%htcc_cad%%. Par défaut, les deux systèmes sont stockés dans un
fichier SQLite nommé `gemc.db`.

Voir aussi la [construction de la géométrie]( /home/documentation/geometry/geometry_building ) pour plus
d'informations.

<br/>

### Exécution de GEMC

Le fichier `htcc.yaml` peut être utilisé pour lancer la simulation. Ajoutez `-gui` pour une exécution
interactive :

```shell
gemc htcc.yaml -gui
```

Modifiez `htcc.yaml` selon vos besoins, en particulier pour ajouter des particules, contrôler le nombre de
threads ou changer la sortie.

<br/>

## Exécution d'événements

{% include figure.html
src="/assets/images/examples/htcc/gemc_view.png"
caption="CLAS12 HTCC simulation: generated electrons crossing the high-threshold Cherenkov counter geometry."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne les noms de fichiers et les formats de sortie :

```yaml
gstreamer:
  - format: csv
    filename: htcc
  - format: hipo
    filename: htcc
```

Voir aussi la [documentation sur la sortie]( /home/documentation/output ) pour plus d'informations.


## Tracé avec l'analyseur GEMC

Lancez d'abord GEMC avec 2 000 événements. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc htcc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Tracez l'énergie totale déposée par impact :

```shell
gemc-analyzer htcc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![énergie totale déposée par impact dans le HTCC][htcc-analyzer_totEdep]{:width="70%"}

[htcc-analyzer_totEdep]: /home/assets/images/examples/htcc/analyzer_totEdep.png

Tracez les positions des impacts en y en fonction de x :

```shell
gemc-analyzer htcc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![positions des impacts en y en fonction de x dans le HTCC][htcc-analyzer_yvsx]{:width="70%"}

[htcc-analyzer_yvsx]: /home/assets/images/examples/htcc/analyzer_yvsx.png
