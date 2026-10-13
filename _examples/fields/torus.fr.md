---
layout: default
title: "Torus ASCII Field Map"
permalink: /examples/fields/torus.html
lang: fr
human_reviewed: false
---

# Exemple de Carte de Champ ASCII en Tore
<hr style="height:4px;border:0;background:#4a90e2;">

Cet exemple de champ affiche une carte de champ ASCII segmentée en phi, chargée via le plugin de champ
`asciimap`. Il utilise un volume transparent en forme de tore pour rendre la région du champ facile à
repérer.

{% assign example = site.data.examples | where: "title", "Torus ASCII Field Map" | first %}

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant, construisez la base de données de géométrie, puis ouvrez
l'affichage du champ :

```shell
cp -r $GEMC_HOME/examples/fields/torus .
cd torus
./torus.py
gemc torus.yaml -gui
```

<br/>

## Géométrie

La géométrie est définie dans `torus.py`. Le volume monde %%root%% contient un tore transparent,
%%torus_field_volume%%, dont la propriété %%mfield%% est définie à %%torus%%.

<br/>

## Définition du champ

Le fichier YAML charge `torus_map.txt` comme carte ASCII segmentée en phi :

```yaml
gfields:
  - name: torus
    type: asciimap
    symmetry: phi-segmented
    map: torus_map.txt
    field_unit: kilogauss
    interpolation: none
    integration_stepper: G4ClassicalRK4
    minimum_step: 1*mm
    coordinate1: "azimuthal,    4, 0*deg,  30*deg"
    coordinate2: "transverse,   6, 0*cm,   500*cm"
    coordinate3: "longitudinal, 6, 100*cm, 600*cm"
```

Les trois premières colonnes de la carte sont %%azimuthal%%, %%transverse%% et %%longitudinal%%. Les trois
colonnes suivantes sont %%Bx%%, %%By%% et %%Bz%% en kilogauss.

<br/>

## Affichage du champ

{% include figure.html
src="/assets/images/examples/torus/gemc_view.png"
caption="Torus ASCII-map display: a transparent torus with field lines from a phi-segmented map."
%}

<br/>

## Utilisation

Le fichier `torus.yaml` définit `n: 0`, donc aucun `/run/beamOn` n'est nécessaire pour cette scène
d'affichage. Ajoutez `-fieldAt` pour inspecter le champ configuré en un point :

```shell
gemc torus.yaml -fieldAt="250*cm 0*cm 350*cm"
```
