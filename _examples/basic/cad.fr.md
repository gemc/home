---
layout: default
title: "CAD example"
permalink: /examples/basic/cad.html
lang: fr
human_reviewed: false
---

# Exemple CAD
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Cet exemple importe trois maillages STL d'organes avec la fabrique CAD de GEMC et modélise un traitement
médical de curiethérapie : une source d'**iridium-192** à haut débit de dose (HDR) est placée
*à l'intérieur du foie* et émet des photons de façon isotrope. Chaque organe est un détecteur sensible
%%flux%%, ce qui permet d'enregistrer l'énergie déposée par organe ; `plot_dose.py` la convertit en dose
absorbée et en temps d'irradiation équivalent pour l'Ir-192.

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant. Pour charger les définitions CAD, simuler 200 événements
avec une sortie CSV et tracer la dose dans chaque organe :

```shell
cp -r $GEMC_HOME/examples/basic/cad .
cd cad
./cad.py
gemc cad.yaml -n=200
./plot_dose.py
```

<br/>

## Géométrie

La géométrie est définie de façon déclarative dans `stls/cad__default.yaml` et chargée dans `gemc.db` par
`cad.py`.

Le système CAD nommé %%stls%% contient :

- %%heart_NIH3D%%, un maillage de cœur dont le matériau est le sang.
- %%respiratory_NIH3D%%, un maillage de poumon translucide constitué de %%G4_LUNG_ICRP%%.
- %%liver_NIH3D%%, un maillage de foie dont le matériau est le tissu mou.

Chaque entrée de `stls/cad__default.yaml` définit le fichier de maillage, le matériau, la couleur,
l'échelle, la position et l'identifiant. La valeur %%system%% doit correspondre à la fois au nom
`gsystem` dans `cad.yaml` et au répertoire qui contient les fichiers STL. Les trois organes sont centrés
sur l'axe y (chaque centroïde vérifie `x = z = 0`) et empilés le long de cet axe. Le maillage de poumon
— créé avec la trachée orientée vers le bas — possède une `rotation` de 180° autour de z qui le remet à
l'endroit.

Voir aussi la [documentation sur les importations CAD](/home/documentation/geometry/cad_imports) pour plus
d'informations.

Visualiseur interactif :

<iframe
  src="/home/assets/vtkjs-viewer.html?fileURL=/home/assets/images/examples/cad/cad.vtksz"
  title="Interactive VTK.js view of the CAD organ geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Liste de physique

`FTFP_BERT` est utilisée par défaut et sélectionnée dans le fichier YAML avec `phys_list: FTFP_BERT`.

{% include notes/physics-list-note.md %}

<br/>

## Générateur

La cinématique des particules est définie dans le fichier YAML :

```yaml
gparticle:
  - name: gamma
    p: 380*keV
    delta_p: 120*keV
    multiplicity: 300
    theta: 90*deg
    delta_theta: 90*deg
    randomThetaModel: cosine
    phi: 180*deg
    delta_phi: 180*deg
    vx: 0*mm
    vy: -140*mm
    vz: 0*mm
    delta_vx: 20*mm
    delta_vy: 20*mm
    delta_vz: 20*mm
    randomVertexModel: sphere
```

Cela modélise une **source clinique de curiethérapie HDR à l'iridium-192** introduite dans le foie :

- **Énergie** — l'Ir-192 émet un spectre de raies (raies dominantes entre 0,30 et 0,61 MeV). Ce spectre est
  approximé ici par des photons d'énergie moyenne d'environ 0,38 MeV, avec une dispersion en énergie
  définie par `delta_p` pour couvrir le spectre.
- **Position** — le vertex de génération est situé au centroïde du foie dans le repère global,
  `(0, -140, 0) mm`, avec une distribution uniforme dans une sphère d'environ 35 mm de rayon
  (`randomVertexModel: sphere` utilise `|delta_v|` comme rayon) pour reproduire la région où séjourne la
  source. Les organes sont empilés le long de l'axe y (`x = z = 0`), avec le cœur à l'origine, le foie
  juste en dessous et les poumons au-dessus.
- **Direction** — émission isotrope sur 4π : échantillonnage `cosine` de θ sur 0–180° combiné à une
  distribution uniforme de φ sur 0–360°.

Voir aussi la [documentation du générateur interne](/home/documentation/generator/internal) pour plus
d'informations.

<br/>

## Numérisation

Chaque organe est configuré comme détecteur sensible %%flux%% dans `stls/cad__default.yaml` :

```yaml
defaults:
  digitization: flux

volumes:
  - name: heart_NIH3D
    identifier: "organ: 1"
```

Le détecteur utilisant la numérisation %%flux%% fonctionne en **mode événement** : il écrit une ligne de
sortie par impact, contenant l'identifiant %%identifier%% de l'organe et l'énergie déposée %%totEdep%%.
Cela permet de distinguer les trois organes au cours d'une seule exécution.

> La numérisation intégrée %%dosimeter%% calculerait également la dose, mais son détecteur fonctionne en
> **mode exécution** : il cumule tous les impacts partageant le même nom de détecteur sensible dans un
> enregistrement unique. Comme les trois organes partagent le même nom `dosimeter`, leurs résultats
> seraient regroupés en une seule valeur. L'utilisation de %%flux%% conserve l'identité de l'organe pour
> chaque impact.

### Dose absorbée

`plot_dose.py` additionne l'énergie déposée par organe et la divise par la masse de l'organe pour obtenir
la dose absorbée :

$$
D_{\text{organ}} = \frac{\sum_i \mathrm{totEdep}_i}{m_{\text{organ}}},
\qquad
m_{\text{organ}} = \rho \, V_{\text{mesh}}
$$

où la somme porte sur les impacts dans l'organe, \\(\rho\\) est la masse volumique du matériau attribué
(`gemc cad.yaml -printSystemsMaterials` indique 1,06, 1,04 et 1,03 g/cm³ pour les matériaux représentant
le sang, le poumon et le tissu mou) et \\(V_{\text{mesh}}\\) est le volume du maillage CAD (volume signé
d'origine × le facteur d'échelle uniforme `scale`³). Un gray vaut un joule par kilogramme,
\\(1\,\mathrm{Gy} = 1\,\mathrm{J/kg}\\).

### Temps d'irradiation

La simulation émet un nombre fixe de photons ; le **temps d'irradiation réel** correspondant est le temps
nécessaire à une source d'Ir-192 d'activité \\(A\\) pour émettre ce nombre de photons. Avec un rendement
photonique \\(Y\\) (photons par désintégration), la source émet \\(R = A\,Y\\) photons par seconde, donc
pour \\(N_\gamma = N_{\text{events}} \times m\\) photons simulés (multiplicité \\(m\\)) :

$$
R = A \, Y,
\qquad
t_{\text{rad}} = \frac{N_\gamma}{A \, Y}
$$

`plot_dose.py` utilise par défaut une source HDR nominale, \\(A = 10\ \mathrm{Ci} = 3.7\times10^{11}\\) Bq,
et \\(Y = 2.3\\) photons par désintégration d'Ir-192 (la somme des intensités des raies gamma) ; ces deux
paramètres sont réglables avec `--activity` et `--yield`. Comme la dose et \\(t_{\text{rad}}\\) varient
tous deux linéairement avec \\(N_\gamma\\), la dose absorbée par unité de temps de traitement (le débit
de dose) est \\(D_{\text{organ}} / t_{\text{rad}}\\), et une dose thérapeutique complète est atteinte en
augmentant le nombre de photons (ou, de manière équivalente, le temps de séjour de la source).

Voir la [documentation du dosimètre](/home/documentation/sensitivity/dosimeter) pour plus d'informations.

<br/>

## Utilisation

### Construction du détecteur

Utilisez le script Python `cad.py` pour charger les définitions CAD. Le script lit
`stls/cad__default.yaml` et stocke la configuration dans un fichier SQLite nommé `gemc.db`.

```shell
./cad.py
```

{% include notes/python-api-note.md %}

Voir aussi la [construction de la géométrie](/home/documentation/geometry/geometry_building) pour plus
d'informations.

<br/>

### Exécution de GEMC

Le fichier `cad.yaml` permet d'exécuter la simulation avec cette configuration. Ajoutez `-gui` pour une
exécution interactive :

```shell
gemc cad.yaml -gui
```

Modifiez `cad.yaml` selon vos besoins, notamment pour ajouter des particules, contrôler le nombre de
threads ou modifier la sortie.

<br/>

## Simulation des événements

{% include figure.html
src="/assets/images/examples/cad/gemc_view.png"
caption="CAD simulation: an Iridium-192 brachytherapy source inside the liver emits photons
isotropically, depositing dose in the imported liver, heart, and lung meshes."
%}

<br/>

## Sortie

L'option %%gstreamer%% sélectionne le nom du fichier et le format de sortie :

```yaml
gstreamer:
  - format: csv
    filename: organs
```

{% include notes/output-note.md %}

Voir aussi la [documentation sur les sorties](/home/documentation/output) pour plus d'informations.

<br/>

## Tracé de la dose dans chaque organe

Exécutez d'abord GEMC pour que les flux de sortie CSV du détecteur %%flux%% soient écrits (davantage
d'événements améliorent les statistiques pour les organes à risque) :

```shell
gemc cad.yaml -n=200
```

Tracez ensuite la dose par organe avec `plot_dose.py`. Ce script lit `organs_t0_digitized.csv`, affiche
l'énergie déposée, la masse et la dose par organe, et trace le diagramme en barres :

```shell
./plot_dose.py                       # nominal 10 Ci Ir-192 source
./plot_dose.py --activity 5          # a weaker 5 Ci source (rescales the irradiation time)
./plot_dose.py --save organs_dose.png
```

![dose par organe dans l'exemple CAD][cad-dose_per_organ]{:width="70%"}

Le foie, qui contient la source, absorbe de loin la dose la plus élevée ; le cœur juste au-dessus et les
poumons au sommet de l'empilement reçoivent une dose due au rayonnement diffusé bien plus faible — une
localisation qui rend la curiethérapie intéressante. Le titre indique le temps d'irradiation par l'Ir-192
que représente le nombre de photons simulés (voir [Temps d'irradiation](#irradiation-time) ci-dessus).

[cad-dose_per_organ]: /home/assets/images/examples/cad/dose_per_organ.png


## Tracé avec l'analyseur GEMC

Exécutez d'abord GEMC avec 200 événements. Le fichier YAML par défaut écrit les flux CSV destinés à
l'analyseur.

```shell
gemc cad.yaml -n=200
```

Tracez l'énergie totale déposée par impact :

```shell
gemc-analyzer organs_t0_digitized.csv totEdep --kind csv
```

![énergie totale déposée par impact dans l'exemple CAD][cad-analyzer_totEdep]{:width="70%"}

[cad-analyzer_totEdep]: /home/assets/images/examples/cad/analyzer_totEdep.png
