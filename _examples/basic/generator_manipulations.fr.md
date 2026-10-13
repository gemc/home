---
layout: default
title: "Generator manipulations"
permalink: /examples/basic/generator_manipulations.html
lang: fr
human_reviewed: false
---

# Manipulations du générateur
<hr style="height:4px;border:0;background:#4a90e2;">

Utilisez GEMC 0.5 ou une version ultérieure pour ces exemples.
Consultez le [guide d'installation]({{ site.baseurl }}/installation/) pour l'exécutable et l'environnement Python.

Onze cartes de pilotage indépendantes isolent la dispersion des vertex, les angles fixes et l'échantillonnage
angulaire.
Chacune génère un geantino de 1 GeV à l'intérieur de la même petite cible tubulaire pour représenter un
événement dans la cible.
Les graphiques ci-dessous proviennent de nouvelles simulations :
5 000 tirages par carte, vérifiés à partir des enregistrements des particules générées avant le tracé. Chaque cas
comprend également sa propre vue GEMC de 100 événements.

{% assign source = "https://github.com/gemc/src/tree/main/examples/basic/generator_manipulations" %}
{% assign source_files = source | replace: "/tree/", "/blob/" %}
{% assign cases = site.data.generator_cases %}

[Consultez le code source de l'exemple]({{ source }}), comprenant la géométrie, les cartes YAML complètes et les
vérifications automatisées.

## Démarrage rapide

Copiez l'exemple depuis votre installation GEMC et générez sa géométrie ASCII :

```shell
cp -r "$GEMC_HOME/examples/basic/generator_manipulations" .
cd generator_manipulations
python generator_manipulations.py -f ascii
gemc uniform_z.yaml -gui
```

Générez des événements avec la commande beam-on de l'interface graphique, puis ouvrez l'Analyzer. Les cartes de
dispersion XY préparent un seul graphique 2D de Y en fonction de X. La dispersion en Z et les angles fixes
préparent trois histogrammes ; les autres cartes préparent quatre graphiques.
Toutes les cartes activent l'accumulation entre les appels beam-on. Qt Charts est requis pour l'Analyzer de
l'interface graphique.
Exécutez n'importe quelle carte sans %%-gui%% pour produire à la place un échantillon CSV de 5 000 événements
avec une graine aléatoire fixée :

```shell
gemc uniform_z.yaml
```

Chaque carte possède son propre préfixe de sortie. Par exemple, %%uniform_z%% produit les flux CSV des
particules générées et des informations de vérité utilisés pour vérifier que la cible enregistre exactement les
vertex tirés.

## Géométrie et grandeurs enregistrées

Le volume monde sous vide contient un tube d'hydrogène liquide, centré à l'origine, de rayon 25 mm et de longueur
totale 40 mm, affiché avec une opacité de 20 % pour que les trajectoires restent visibles à travers lui.
Sa sensibilité %%flux%% enregistre les particules créées à l'intérieur. La dispersion représente les vertex de
production des événements dans la cible.
Les geantinos ne subissent pas de diffusion et ne créent pas de particules secondaires ; %%recordZeroEdep: true%%
conserve leurs hits dans la cible.
On obtient ainsi un hit par particule tirée pour ces configurations.

{% include figure.html
src="/assets/images/examples/generator_manipulations/gemc_view.png"
alt="Geantinos originating at smeared vertices inside the transparent cylindrical target"
caption="The shared tube target with 100 events from the uniform-Z card, rendered by GEMC."
%}

{% assign vtk = "/assets/images/examples/generator_manipulations/generator_manipulations.vtksz" %}
<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ vtk }}"
  title="Interactive view of the tube target"
  width="100%" height="420" loading="lazy"
  style="border:1px solid #d0d7de;">
</iframe>

Les graphiques des vertex utilisent %%vx%%, %%vy%% et %%vz%% issus des informations de vérité de la cible, en mm.
Il s'agit des vertex d'origine des trajectoires. Les champs %%avgx%%, %%avgy%% et %%avgz%% décrivent, quant à eux,
les positions à l'intérieur de la cible.
Les graphiques angulaires utilisent les composantes conservées de l'impulsion %%px%%, %%py%% et %%pz%%, en MeV/c.

Les figures du site web utilisent les fonctions de tracé de l'Analyzer de `pygemc` avec les variables et la
disposition définies dans le bloc %%ganalysis%% de chaque carte. Ce sont des graphiques produits hors ligne à
partir des mêmes champs de données que ceux affichés dans l'interface graphique. Les figures de dispersion en Z
du site web placent X et Y au-dessus d'un histogramme de Z couvrant les deux colonnes ; la figure des angles
fixes utilise une rangée de trois histogrammes. L'interface graphique utilise sa disposition à un seul panneau
ou à quatre emplacements.

## Cas de dispersion des vertex

Les cartes de dispersion utilisent le centre décalé (2, -3, 0) mm pour montrer que des décalages aléatoires sont
ajoutés à la position nominale. La dispersion en Z utilise theta = 90 degrés ; les dispersions dans le plan XY
et dans une sphère utilisent theta = 45 degrés.
Toutes les cartes de dispersion des vertex utilisent phi = 90 degrés.
Les dispersions uniforme et gaussienne dans le plan XY font varier les deux coordonnées transverses
indépendamment et affichent des cartes 2D de Y en fonction de X. Des cartes distinctes de dispersion uniforme
et gaussienne en Z isolent l'étalement longitudinal.

- %%uniform%% : chaque %%delta_vx%%, %%delta_vy%% ou %%delta_vz%% non nul est une demi-largeur autour de son centre.
- %%gaussian%% : chaque delta est un écart type. Les fenêtres des graphiques unidimensionnels couvrent cinq sigma ;
  ces limites d'affichage ne tronquent pas la génération. La dispersion gaussienne en Z utilise sigma = 3 mm :
  la demi-longueur de la cible couvre donc plus de six sigma. Les queues gaussiennes ne sont pas bornées ;
  on vérifie que les échantillons générés avec une graine fixée restent à l'intérieur de la cible.
- %%sphere%% : les points sont répartis uniformément dans tout le volume d'une sphère de rayon
  %%sqrt(delta_vx^2 + delta_vy^2 + delta_vz^2)%%. Des dispersions de (1, 2, 2) mm donnent un rayon de 3 mm,
  plutôt que trois axes d'ellipsoïde. Les projections sur les coordonnées sont paraboliques et la fonction de
  répartition radiale est %%(r/R)^3%%.

{% assign vertex_cases = cases | where: "group", "Vertices" %}
{% for case in vertex_cases %}
### {{ case.title }}

{{ case.expected }}

[{{ case.name }}.yaml complet]({{ source_files }}/{{ case.name }}.yaml)

<details markdown="1">
<summary>Paramètres de la particule</summary>

{% highlight yaml %}{{ case.particle }}{% endhighlight %}

</details>

{% capture event_caption %}GEMC : {{ case.view_events }} événements pour {{ case.title }}.{% endcapture %}
{% include figure.html src=case.event_image alt=case.title caption=event_caption link=case.event_image %}
{% include figure.html src=case.image alt=case.title caption=case.expected link=case.image %}
{% endfor %}

## Cas angulaires

Les cartes angulaires fixent le vertex au centre de la cible, (0, 0, 0) mm. %%randomThetaModel%% prend en charge
%%uniform%%, %%gaussian%% et %%cosine%%.
Pour %%uniform%%, %%delta_theta%% est une demi-largeur ; pour %%gaussian%%, c'est un écart type.
Le modèle %%cosine%% est uniforme en cos(theta) dans l'intervalle theta +/- delta_theta, ce qui donne une densité
proportionnelle à sin(theta), restreinte à [0, 180] degrés.
Les cartes de dispersion de theta utilisent %%delta_theta: 20*deg%% et une valeur nominale de theta de 2 degrés.
L'échantillonnage uniforme couvre [-18, 22] degrés ; l'échantillonnage gaussien a une moyenne de 2 degrés et un
écart type de 20 degrés. Un theta négatif inverse l'impulsion transverse : l'angle polaire reconstruit est
positif ou nul, avec un azimut décalé de 180 degrés.
L'échantillonnage selon le modèle cosinus couvre [0, 22] degrés, car ses tirages sont limités aux angles polaires
physiques.
Phi utilise toujours un échantillonnage uniforme de demi-largeur %%delta_phi%% ; il n'y a pas de
%%randomPhiModel%%.

Pour une impulsion p, les composantes attendues sont :

```text
px = p sin(theta) cos(phi)
py = p sin(theta) sin(phi)
pz = p cos(theta)
```

La carte à theta et phi fixes définit ces angles à 3 et 45 degrés, respectivement, et affiche uniquement les trois
histogrammes d'impulsion. Les cartes de theta uniforme, gaussien et selon le modèle cosinus affichent %%px%% sur
l'axe vertical en fonction de %%pz%% sur l'axe horizontal dans leurs graphiques 2D. Le cas de theta selon le
modèle cosinus donne également une distribution uniforme de
%%pz%%. Un theta fixe avec une dispersion de phi trace un arc
dans la projection %%px%%/%%py%%. Le cas de passage par 360 degrés ne présente aucune discontinuité de l'impulsion.
Les angles de la banque des particules générées sont stockés en radians ; les cartes de pilotage utilisent
explicitement des degrés.

{% assign angular_cases = cases | where: "group", "Angles" %}
{% for case in angular_cases %}
### {{ case.title }}

{{ case.expected }}

[{{ case.name }}.yaml complet]({{ source_files }}/{{ case.name }}.yaml)

<details markdown="1">
<summary>Paramètres de la particule</summary>

{% highlight yaml %}{{ case.particle }}{% endhighlight %}

</details>

{% capture event_caption %}GEMC : {{ case.view_events }} événements pour {{ case.title }}.{% endcapture %}
{% include figure.html src=case.event_image alt=case.title caption=event_caption link=case.event_image %}
{% include figure.html src=case.image alt=case.title caption=case.expected link=case.image %}
{% endfor %}

## Vérifier et reproduire

Depuis une arborescence source GEMC configurée, exécutez les 11 vérifications :

```shell
meson test -C build --suite generator_manipulations --print-errorlogs
```

Les vérifications exigent que chaque vertex se trouve à l'intérieur de la cible et qu'il y ait un hit dans la
cible par tirage. Elles vérifient la correspondance des identifiants d'événements et des vertex, comparent les
composantes de l'impulsion, reconstruisent theta et phi modulo 360 degrés et testent les distributions de
probabilité attendues.
Les vérifications XY contrôlent aussi l'absence de corrélation entre les échantillons transverses. Les tests
génèrent une nouvelle géométrie et de nouvelles données de sortie dans des répertoires temporaires, de sorte que
chaque cas fonctionne également de manière isolée.

Pour régénérer les images et les paramètres des particules de cette page depuis le dépôt du site web :

```shell
python3 scripts/generate_example_assets.py generator_manipulations
```

Le [guide des ressources]({{ site.baseurl }}/assets/assets.md) du site web décrit les environnements locaux requis.
Consultez aussi le [guide du générateur interne]({{ site.baseurl }}/documentation/generator/internal).
