---
layout: default
title: "Dipole Field"
permalink: /examples/fields/dipole.html
lang: fr
human_reviewed: false
---

# Exemple de champ dipolaire
<hr style="height:4px;border:0;background:#4a90e2;">

Cet exemple de champ affiche un champ dipolaire transverse idéal issu de `gmultipoles`. Il est utile pour
vérifier l'association du champ sur un volume unique ainsi que les options visuelles de démarrage des lignes de
champ.

{% assign example = site.data.examples | where: "title", "Dipole Field" | first %}

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant, construisez la base de données de géométrie et ouvrez
l'affichage du champ :

```shell
cp -r $GEMC_HOME/examples/fields/dipole .
cd dipole
./dipole.py
gemc dipole.yaml -gui
```

<br/>

## Géométrie

La géométrie est définie dans `dipole.py`. Le volume monde %%root%% contient une boîte transparente,
%%dipole_field_box%%, dont la propriété %%mfield%% est réglée sur %%dipole%%.

<br/>

## Définition du champ

Le fichier YAML définit un dipôle de 2 T incliné de 30 degrés autour de l'axe z :

```yaml
gmultipoles:
  - name: dipole
    pole_number: 2
    strength: 2
    rotaxis: z
    rotation_angle: "30*deg"
```

Les options d'affichage demandent 80 lignes de champ ainsi que les arêtes de la géométrie auxiliaire :

```yaml
show_field_lines: 80
show_auxiliary_edges: true
```

<br/>

## Affichage du champ

{% include figure.html
src="/assets/images/examples/dipole/gemc_view.png"
caption="Dipole field display: a transparent field box with ideal transverse field lines."
%}

<br/>

## Utilisation

Le fichier `dipole.yaml` fixe `n: 0`, de sorte qu'aucun `/run/beamOn` n'est nécessaire pour cette scène
d'affichage. Ajoutez `-fieldAt` pour inspecter le champ configuré en un point :

```shell
gemc dipole.yaml -fieldAt="0*cm 0*cm 0*cm"
```
