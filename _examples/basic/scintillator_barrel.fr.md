---
layout: default
title: "Scintillator Barrel"
permalink: /examples/basic/scintillator_barrel.html
lang: fr
human_reviewed: false
---

# Tonneau de scintillateurs
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple construit un détecteur cylindrique à scintillateur en tonneau composé de 48 lattes trapézoïdales
disposées en anneau complet. Il illustre l'API `distribute_on_circle` servant à répliquer un
volume à intervalles angulaires réguliers autour d'un cercle et montre comment dimensionner les
lattes pour que les faces adjacentes soient quasi jointives.


{% assign example = site.data.examples | where: "title", "Scintillator Barrel" | first %}
Vous pouvez exécuter cet exemple dans votre navigateur : [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant.
Pour créer la géométrie et exécuter 3 événements :

```shell
cp -r $GEMC_HOME/examples/basic/scintillator_barrel .
cd scintillator_barrel
./scintillator_barrel.py
gemc scintillator_barrel.yaml
```

<br/>

## Géométrie

La géométrie est définie dans `scintillator_barrel.py`. Le monde (une boîte nommée %%root%%) contient
48 volumes %%paddle%% identiques disposés en anneau :

- Chaque %%paddle%% est un solide trapézoïdal général `G4Trap` (%%G4_PLASTIC_SC_VINYLTOLUENE%%) dont la
  face la plus large est orientée radialement vers l'extérieur et la face la plus étroite vers l'axe du faisceau.
- Les lattes sont dimensionnées avec la formule de la corde afin que les faces externes adjacentes
  soient jointives :
  - demi-largeur externe : `pX  = (radius + pY) × sin(π/n)`
  - demi-largeur interne : `pLTX = (radius − pY) × sin(π/n)`
- `distribute_on_circle(n=48, radius=400 mm, align=True, axis='z')` place et fait pivoter chaque
  copie autour de l'axe z par pas égaux de 7,5°.

Consultez la documentation [Fonctions utilitaires de structure](/home/documentation/geometry/structure) pour
la référence complète de l'API `distribute_on_circle` et la géométrie de dimensionnement.

Visualiseur interactif (tonneau complet de 48 lattes) :

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/scintillator_barrel/scintillator_barrel.vtksz"
  title="Interactive VTK.js view of the scintillator_barrel geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Liste de physique

`QBBC` est utilisée par défaut, sélectionnée dans le fichier YAML avec `phys_list: QBBC`.

{% include notes/physics-list-note.md %}

<br/>

## Générateur

La cinématique des particules est définie dans le fichier YAML :

```yaml
gparticle:
  - name: proton
    p: 500*MeV
    theta: 90*deg
    delta_phi: 360*deg
    multiplicity: 3
```

Consultez aussi la [documentation du générateur interne]( /home/documentation/generator/internal ) pour en savoir plus.

<br/>

## Numérisation

Chaque %%paddle%% se voit attribuer la numérisation %%flux%% avec un identifiant de latte unique :

```python
paddle.digitization = "flux"
# ...
v.set_identifier("paddle", i)
```

Consultez la [documentation Flux]( /home/documentation/sensitivity/flux ) pour plus d'informations.

<br/>

## L'API `distribute_on_circle`

La méthode `distribute_on_circle` de `GVolume` réplique le volume modèle `n` fois
autour d'un cercle de rayon `radius` donné. Avec `align=True`, chaque copie subit en plus une rotation
autour de l'axe choisi selon sa position angulaire φᵢ, ce qui maintient le repère local de chaque latte
aligné radialement :

```python
for i, v in enumerate(paddle.distribute_on_circle(n, radius, align=True, axis='z')):
    v.set_identifier("paddle", i)
    v.publish(cfg)
```

La méthode renvoie une liste de copies `GVolume` indépendantes, une par pas angulaire, chacune nommée
`<name>_i` et positionnée en `(radius·cos φᵢ, radius·sin φᵢ, 0)`.
Référence complète de l'API : [Fonctions utilitaires de structure](/home/documentation/geometry/structure).

<br/>

## Utilisation

### Construction du détecteur

Utilisez le script Python `scintillator_barrel.py` pour construire le détecteur. Par défaut, la configuration
est stockée dans un fichier SQLite nommé `gemc.db`. Des options en ligne de commande permettent de définir le
type de base de données, les variations et le numéro de run.

Pour en savoir plus, consultez aussi [Construction de la géométrie]( /home/documentation/geometry/geometry_building ).

<br/>

### Exécution de GEMC

Le fichier `scintillator_barrel.yaml` lance la simulation. Ajoutez `-gui` pour l'exécuter de manière interactive :

```shell
gemc scintillator_barrel.yaml -gui
```

Modifiez `scintillator_barrel.yaml` selon vos besoins, en particulier pour changer le nombre d'événements,
ajouter des threads ou sélectionner les formats de sortie.

<br/>

## Exécution des événements

La vue ci-dessous montre le tonneau de face après un événement, avec 3 protons émis radialement
vers l'extérieur à θ = 90°. Chaque proton traverse une latte de scintillateur.

{% include figure.html
src="/assets/images/examples/scintillator_barrel/gemc_view.png"
caption="Scintillator barrel viewed end-on along the beam axis. Three protons at θ = 90°
travel radially outward, each depositing energy in one paddle."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne les noms de fichiers de sortie et le format :

```yaml
gstreamer:
  - format: csv
    filename: barrel
```

Consultez également la [documentation sur les sorties]( /home/documentation/output ) pour plus d'informations.

<br/>

## Tracé de graphiques avec l'analyseur GEMC

Exécutez d'abord GEMC avec 1 000 événements. Le fichier YAML par défaut écrit les flux CSV de l'analyseur.

```shell
gemc scintillator_barrel.yaml -n=1000
```

Tracez l'énergie totale déposée par hit :

```shell
gemc-analyzer barrel_t0_digitized.csv totEdep --kind csv
```

![scintillator_barrel : énergie totale déposée par hit][scintillator_barrel-analyzer_totEdep]{:width="70%"}

[scintillator_barrel-analyzer_totEdep]: /home/assets/images/examples/scintillator_barrel/analyzer_totEdep.png

Tracez l'énergie vraie de la particule le long de sa trajectoire :

```shell
gemc-analyzer barrel_t0_true_info.csv E --kind csv --data true_info
```

![scintillator_barrel : énergie vraie de la trajectoire de la particule][scintillator_barrel-analyzer_true_energy]{:width="70%"}

[scintillator_barrel-analyzer_true_energy]: /home/assets/images/examples/scintillator_barrel/analyzer_true_energy.png
