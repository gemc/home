---
layout: default
title: "Boolean Solids"
permalink: /examples/basic/boolean_solids.html
lang: fr
human_reviewed: false
---

# Exemple de solides booléens
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple illustre les opérations booléennes de GEMC sur les solides. Il construit trois solides placés
à partir de volumes composants non placés : une plaque avec un trou obtenu par soustraction, une croix
formée par une union et une lentille formée par l'intersection de deux sphères.

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant.
Pour créer la géométrie et exécuter 10 événements :

```shell
cp -r $GEMC_HOME/examples/basic/boolean_solids .
cd boolean_solids
./boolean_solids.py
gemc boolean_solids.yaml -n=10
```

<br/>

## Géométrie

La géométrie est définie dans `boolean_solids.py`.

Le monde (une boîte nommée %%root%%) contient trois volumes booléens visibles :

| Volume | Opération | Composants |
|--------|-----------|------------|
| %%plate_with_hole%% | soustraction | %%plate_box - plate_hole%% |
| %%cross%% | union | %%bar + bar_rotated%% |
| %%lens%% | intersection | %%sphere_one * sphere_two%% |

Les volumes composants utilisent le matériau spécial %%Component%%. Ils définissent les opérandes de
l'expression booléenne, mais ne sont pas placés comme volumes visibles du détecteur. Les volumes booléens
résultants sont placés comme tout autre `GVolume`, avec leur matériau, leur couleur, leur position et leur rotation.

Visionneuse interactive :

{% assign boolean_solids_vtksz = "/assets/images/examples/boolean_solids/boolean_solids.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ boolean_solids_vtksz }}"
  title="Interactive VTK.js view of the boolean solids geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Expressions booléennes

Un solide booléen est sélectionné en attribuant une valeur à %%solidsOpr%% :

```python
plate.solidsOpr = 'plate_box - plate_hole'
cross.solidsOpr = 'bar + bar_rotated'
lens.solidsOpr = 'sphere_one * sphere_two'
```

Le premier opérande est évalué à sa propre origine. Le second utilise sa propre position et sa propre
rotation par rapport au premier. Par exemple, %%plate_hole%% est décalé de 30 mm avant d'être soustrait
de %%plate_box%%, de sorte que le trou est décentré.

<br/>

## Générateur

La cinématique des particules est définie dans le fichier YAML :

```yaml
gparticle:
  - name: e-
    p: 500*MeV
    theta: 90*deg
    vx: -40*cm
    delta_vx: 12*cm
    randomVertexModel: uniform
```

Voir aussi la [documentation du générateur interne]( /home/documentation/generator/internal ) pour en savoir plus.

<br/>

## Utilisation

### Construction du détecteur

Utilisez le script Python `boolean_solids.py` pour construire le détecteur. Par défaut, la configuration est
stockée dans un fichier SQLite nommé `gemc.db`.

```shell
./boolean_solids.py
```

Voir aussi [Construction de la géométrie]( /home/documentation/geometry/geometry_building ) pour en savoir plus.

<br/>

### Exécution de GEMC

Le fichier `boolean_solids.yaml` permet d'exécuter la configuration. Ajoutez `-gui` pour l'exécuter
en mode interactif :

```shell
gemc boolean_solids.yaml -gui
```

<br/>

## Exécution des événements

{% include figure.html
src="/assets/images/examples/boolean_solids/gemc_view.png"
caption="Boolean solids simulation: electrons crossing the subtraction, union, and intersection volumes."
%}
