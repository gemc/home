---
layout: default
title: "Constant Field"
permalink: /examples/fields/constant.html
lang: fr
human_reviewed: false
---

# Exemple de champ constant
<hr style="height:4px;border:0;background:#4a90e2;">

Cet exemple de champ affiche un champ magnétique longitudinal uniforme à l'aide de `gmultipoles`. Il
s'agit d'une scène minimale permettant de vérifier la visualisation des lignes de champ sans exécuter
d'événements.

{% assign example = site.data.examples | where: "title", "Constant Field" | first %}

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant, construisez la base de données de géométrie, puis ouvrez
l'affichage du champ :

```shell
cp -r $GEMC_HOME/examples/fields/constant .
cd constant
./constant.py
gemc constant.yaml -gui
```

<br/>

## Géométrie

La géométrie est définie dans `constant.py`. Le volume monde %%root%% contient une boîte transparente,
%%constant_field_box%%, dont la propriété %%mfield%% est réglée sur %%constant%%.

<br/>

## Définition du champ

Le fichier YAML définit un champ uniforme longitudinal à l'aide de `gmultipoles` :

```yaml
gmultipoles:
  - name: constant
    pole_number: 2
    strength: 1
    rotaxis: z
    longitudinal: true
```

Les options d'affichage demandent 30 lignes de champ ainsi que les arêtes de géométrie auxiliaires :

```yaml
show_field_lines: 30
show_auxiliary_edges: true
```

<br/>

## Affichage du champ

{% include figure.html
src="/assets/images/examples/constant/gemc_view.png"
caption="Constant field display: a transparent box with uniform field lines."
%}

<br/>

## Utilisation

Le fichier `constant.yaml` définit `n: 0`, de sorte qu'aucun `/run/beamOn` n'est nécessaire pour cette
scène d'affichage. Ajoutez `-fieldAt` pour inspecter le champ configuré en un point donné :

```shell
gemc constant.yaml -fieldAt="0*cm 0*cm 0*cm"
```
