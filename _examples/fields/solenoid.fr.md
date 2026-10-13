---
layout: default
title: "Solenoid ASCII Field Map"
permalink: /examples/fields/solenoid.html
lang: fr
human_reviewed: false
---

# Exemple de carte de champ ASCII pour solénoïde
<hr style="height:4px;border:0;background:#4a90e2;">

Cet exemple de champ affiche une carte de champ ASCII cylindrique chargée via le plugin de champ `asciimap`.
Le fichier de carte est volontairement petit, de sorte que l'exemple est facile à examiner et à modifier.

{% assign example = site.data.examples | where: "title", "Solenoid ASCII Field Map" | first %}

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant, construisez la base de données de géométrie, puis ouvrez
l'affichage du champ :

```shell
cp -r $GEMC_HOME/examples/fields/solenoid .
cd solenoid
./solenoid.py
gemc solenoid.yaml -gui
```

<br/>

## Géométrie

La géométrie est définie dans `solenoid.py`. Le volume monde %%root%% contient un tube transparent,
%%solenoid_field_tube%%, dont la propriété %%mfield%% est réglée sur %%solenoid%%.

<br/>

## Définition du champ

Le fichier YAML charge `solenoid_map.txt` comme carte ASCII cylindrique en z :

```yaml
gfields:
  - name: solenoid
    type: asciimap
    symmetry: cylindrical-z
    map: solenoid_map.txt
    field_unit: T
    interpolation: linear
    coordinate1: "transverse,   4, 0*m, 3*m"
    coordinate2: "longitudinal, 7, -3*m, 3*m"
```

Les deux premières colonnes de la carte sont %%transverse%% et %%longitudinal%%. Les deux colonnes suivantes sont
les composantes transverse et longitudinale du champ, en tesla.

<br/>

## Affichage du champ

{% include figure.html
src="/assets/images/examples/solenoid/gemc_view.png"
caption="Solenoid ASCII-map display: a transparent tube with field lines from a cylindrical map."
%}

<br/>

## Utilisation

Le fichier `solenoid.yaml` définit `n: 0`, de sorte qu'aucun `/run/beamOn` n'est nécessaire pour cette scène
d'affichage. Ajoutez `-fieldAt` pour inspecter le champ configuré en un point donné :

```shell
gemc solenoid.yaml -fieldAt="1*m 0*m 0*m"
```
