---
layout: default
title: "CLAS12 LTCC"
permalink: /examples/clas12/ltcc.html
lang: fr
human_reviewed: false
---

# Exemple de compteur Cherenkov à bas seuil de CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple présente la géométrie du compteur Cherenkov à bas seuil (LTCC) de CLAS12 issue de
`clas12-systems`. Il combine l'optique native des miroirs de GEMC avec des maillages CAO chargés via la
fonctionnalité `gcad`. Les deux systèmes sont stockés dans une seule base de données SQLite.

La géométrie et la numérisation du LTCC sont disponibles dans `clas12-systems` 0.3 avec GEMC 0.5 et
`pygemc` 0.5.0.

{% assign example = site.data.examples | where: "title", "LTCC" | first %}

<br/>

## Démarrage rapide

Depuis le dépôt `clas12-systems`, construisez la base de données de géométrie et lancez une courte
simulation :

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ltcc
./ltcc.py
gemc ltcc.yaml -n=1
```

<br/>

## Géométrie

La géométrie, présentée ci-dessous, est définie dans `geometry_src/ltcc/geometry.py` et orchestrée par
`geometry_src/ltcc/ltcc.py`. Les constructeurs natifs portent les scripts perl originaux de clas12Tags
(formes des miroirs, PMT et blindages de fer), tandis que les cônes de Winston réfléchissants et le châssis
mécanique sont importés sous forme de maillages CAO. Les rangées natives utilisent le système SQLite
%%ltcc%% et les rangées de maillages utilisent le système CAO distinct %%ltcc_cad%%. Les deux partagent la
même base de données, la même variation et le même run, de sorte qu'un seul `gemc.db` charge le détecteur
complet.

Le monde (une boîte nommée %%root%%) contient, pour chacun des six secteurs :

- une cale mère de gaz nommée %%ltccS<sector>%% contenant l'optique de ce secteur
- des segments de miroir cylindriques, hyperboliques et elliptiques enregistrés avec la surface optique
  %%ltcc_AlMgF2%%
- des tubes photomultiplicateurs nommés %%pmt_s<sector><side>_<n>%%, lus à gauche et à droite de chaque
  segment
- des blindages de fer de 5 mm couvrant la face extérieure des cônes de Winston
- des cônes de Winston CAO (%%WC_S%%, %%WC_M%%, %%WC_L%%) et des maillages de châssis réutilisés comme
  placements %%copyOf%%

Visualiseur interactif :

{% assign ltcc_vtksz = "/home/assets/images/examples/ltcc/ltcc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ltcc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 LTCC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Liste de physique

Le LTCC est un détecteur Cherenkov ; les photons optiques doivent donc être produits et suivis. Le fichier
YAML sélectionne `FTFP_BERT + G4OpticalPhysics` avec `phys_list: FTFP_BERT + G4OpticalPhysics`.

{% include notes/physics-list-note.md %}

<br/>

## Générateur

Les cinématiques des particules sont définies dans le fichier YAML :

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

Consultez également la [documentation du générateur interne]( /home/documentation/generator/internal ) pour
plus d'informations.

<br/>

## Numérisation

Les tubes photomultiplicateurs utilisent le plugin de numérisation %%ltcc%% propre à CLAS12. Les
identifiants enregistrent le secteur, le côté du PMT et le segment de miroir que le tube lit :

```python
pmt.digitization = "ltcc"
pmt.set_identifier("sector", sector, "side", side_id, "segment", n)
```

<br/>

## Utilisation

### Construction du détecteur

Utilisez `geometry_src/ltcc/ltcc.py` pour construire le détecteur. Le script définit les matériaux et les
surfaces des miroirs, publie les volumes natifs %%ltcc%%, téléverse les définitions CAO du système
%%ltcc_cad%% depuis `stls/cad__default.yaml` et ajoute les placements CAO `copyOf`. Par défaut, les deux
systèmes sont stockés dans un fichier SQLite nommé `gemc.db`.

Consultez également la [construction de la géométrie]( /home/documentation/geometry/geometry_building ) pour
plus d'informations.

<br/>

### Exécution de GEMC

Le fichier `ltcc.yaml` peut être utilisé pour lancer la configuration. Ajoutez `-gui` pour l'exécuter de
manière interactive :

```shell
gemc ltcc.yaml -gui
```

Modifiez `ltcc.yaml` selon vos besoins, en particulier pour ajouter des particules, contrôler le nombre de
threads ou changer la sortie.

<br/>

## Exécution des événements

{% include figure.html
src="/assets/images/examples/ltcc/gemc_view.png"
caption="CLAS12 LTCC simulation: generated electrons crossing the low-threshold Cherenkov counter geometry."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne les noms de fichiers et les formats de sortie :

```yaml
gstreamer:
  - format: csv
    filename: ltcc
  - format: hipo
    filename: ltcc
```

Consultez également la [documentation sur la sortie]( /home/documentation/output ) pour plus d'informations.


## Tracé avec l'analyseur GEMC

Lancez d'abord GEMC avec 2 000 événements. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc ltcc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Tracez l'énergie totale déposée par coup :

```shell
gemc-analyzer ltcc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![ltcc total energy deposited per hit][ltcc-analyzer_totEdep]{:width="70%"}

[ltcc-analyzer_totEdep]: /home/assets/images/examples/ltcc/analyzer_totEdep.png

Tracez les positions des coups y en fonction de x :

```shell
gemc-analyzer ltcc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![ltcc y vs x hit positions][ltcc-analyzer_yvsx]{:width="70%"}

[ltcc-analyzer_yvsx]: /home/assets/images/examples/ltcc/analyzer_yvsx.png
