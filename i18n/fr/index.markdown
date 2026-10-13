---
layout: default
permalink: /
lang: fr
human_reviewed: false
---

[test]: https://github.com/gemc/src/actions/workflows/test.yml

[test-badge]: https://github.com/gemc/src/actions/workflows/test.yml/badge.svg

[deploy]: https://github.com/gemc/src/actions/workflows/deploy.yml

[deploy-badge]: https://github.com/gemc/src/actions/workflows/deploy.yml/badge.svg

[DockerHub]: https://hub.docker.com/r/gemc/gemc

[DockerHub-badge]: https://img.shields.io/docker/pulls/gemc/gemc.svg

[Docs]: https://github.com/gemc/src/actions/workflows/doxygen.yml

[Docs-badge]: https://github.com/gemc/src/actions/workflows/doxygen.yml/badge.svg

[Nightly]: https://github.com/gemc/src/actions/workflows/dev_release.yml

[Nightly-badge]: https://github.com/gemc/src/actions/workflows/dev_release.yml/badge.svg

[Site]: https://github.com/gemc/home/actions/workflows/jekyll.yml

[Site-badge]: https://github.com/gemc/home/actions/workflows/jekyll.yml/badge.svg

[Sanitize]: https://github.com/gemc/src/actions/workflows/sanitize.yml

[Sanitize-badge]: https://github.com/gemc/src/actions/workflows/sanitize.yml/badge.svg

[CodeQL]: https://github.com/gemc/src/actions/workflows/codeql.yml

[CodeQL-badge]: https://github.com/gemc/src/actions/workflows/codeql.yml/badge.svg

[Binary-Tarballs]: https://github.com/gemc/src/actions/workflows/binary_tarballs.yml

[Binary-Tarballs-badge]: https://github.com/gemc/src/actions/workflows/binary_tarballs.yml/badge.svg

[macOS-Tarball]: https://github.com/gemc/src/actions/workflows/macos_tarball.yml

[macOS-Tarball-badge]: https://github.com/gemc/src/actions/workflows/macos_tarball.yml/badge.svg

[Release-Tarballs]: https://github.com/gemc/src/actions/workflows/release_tarballs.yml

[Release-Tarballs-badge]: https://github.com/gemc/src/actions/workflows/release_tarballs.yml/badge.svg?event=release

[PyPI]: https://pypi.org/project/pygemc/

[PyPI-badge]: https://img.shields.io/pypi/v/pygemc.svg?cacheSeconds=300

[PyGemc-Nightly]: https://github.com/gemc/pygemc/actions/workflows/dev_release.yml

[PyGemc-Nightly-badge]: https://github.com/gemc/pygemc/actions/workflows/dev_release.yml/badge.svg

[PyGemc-Publish]: https://github.com/gemc/pygemc/actions/workflows/publish_pypi.yml

[PyGemc-Publish-badge]: https://github.com/gemc/pygemc/actions/workflows/publish_pypi.yml/badge.svg

[PyGemc-Tests]: https://github.com/gemc/pygemc/actions/workflows/pygemc_tests.yml

[PyGemc-Tests-badge]: https://github.com/gemc/pygemc/actions/workflows/pygemc_tests.yml/badge.svg


{% include gemc-logo.svg %}

<small>Ce site documente **GEMC** à partir de la version 3.
Pour les **simulations CLAS12**, utilisez le [dépôt GEMC2 clas12Tags](https://github.com/gemc/clas12Tags).</small>

<br/>

## Simulations Geant4 pilotées par des bases de données, avec une API Python

**GEMC** est une surcouche de [Geant4](https://geant4.web.cern.ch) facile à utiliser depuis Python, qui évite
d'avoir à apprendre le C++ et Geant4. Les utilisateurs construisent des systèmes de détecteurs complets en
Python : géométrie, matériaux et numérisation. L'API alimente automatiquement les bases de données que GEMC
utilise pour exécuter l'ensemble de la chaîne de simulation.

Points forts :

- API Python pour créer la géométrie et les matériaux
- Importation de géométries depuis des fichiers ASCII, SQLite, GDML et des fichiers de maillage CAO
- Détecteurs sensibles intégrés : %%flux%%, %%dosimeter%%, %%particle_counter%% et %%gPhotonDetector%%
- Formats de sortie : ASCII, CSV, JSON et [ROOT](https://root.cern)
- Module Python `analyzer` intégré pour lire les sorties de simulation et les représenter graphiquement
- Visualisation de la géométrie avec [`pyvista`](https://pyvista.org)
- Variations de géométrie et configurations dépendant du numéro de run
- Compilations testées en intégration continue et déploiement avec Docker

<br/><br/>

## Essayer GEMC

Aucune installation requise. Cliquez sur un badge pour lancer une session **JupyterLab** interactive dans votre
navigateur :

{% assign visible_examples = site.data.examples | where: "display", true %}


<table class="zebra compact-table">
  <tbody>
    {% for example in visible_examples %}
    <tr>
      <td>
        <a href="{{ example.binder }}" target="_blank" rel="noopener noreferrer">
          <img src="{{ example.badge }}" alt="{{ example.title }}">
        </a>
      </td>
      <td>{{ example.header }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<br/>

### Image de conteneur

Pour une session JupyterLab locale ou sur une infrastructure HPC, utilisez l'image multi-architecture prête à
l'emploi :

```shell
# Docker
docker run --rm -p 8888:8888 ghcr.io/gemc/binder-tutorials:latest

# Apptainer
apptainer pull gemc-binder-tutorials.sif docker://ghcr.io/gemc/binder-tutorials:latest
apptainer exec gemc-binder-tutorials.sif jupyter lab --ip=0.0.0.0 --no-browser
```

<br/><br/>

## Galerie 3D interactive

Faites pivoter la caméra avec la molette de la souris ou utilisez les touches fléchées dans chaque vignette.
Cliquez sur le lien du titre pour accéder à la documentation.

{% assign gallery_examples = site.data.examples | where: "gallery", true %}

<div class="gallery-grid">
  {% for example in gallery_examples %}
    <article class="gallery-card">
      <h3 class="gallery-card-title"><a href="{{ example.link }}">{{ example.title }}</a></h3>
      <iframe src="/home/assets/vtkjs-viewer.html?fileURL={{ example.vtksz }}"
        title="Interactive VTK.js view of {{ example.title }}"
        loading="lazy"></iframe>
      {% if example.header %}
        <p class="gallery-card-desc meta">{{ example.header }}</p>
      {% endif %}
    </article>
  {% endfor %}
</div>

<br/><br/>

## `pygemc` : l'API Python

L'API Python de GEMC, `pygemc`, fournit des outils de création de bases de données de géométrie et de matériaux,
la visualisation de la géométrie avec `pyvista`, `gemc-system-template` et `gemc-analyzer`. L'analyseur peut lire
les sorties CSV et ROOT de GEMC et tracer des histogrammes à partir de variables sélectionnées.

{% include figure.html
src="/assets/images/gemc_showcase.gif"
alt="Python API example"
caption="  
The code fills the database with the world volume, a liquid hydrogen target, and a flux plane. <br/>
The `pyvista` option gives immediate geometry visualization. <br/>
In the GEMC simulation, hits are created from particles generated by a beam of protons impinging
on the liquid hydrogen target.<br/>
The total deposited energy is plotted with the `analyzer` module."
%}

L'extrait ci-dessous définit le plan de flux sensible en aval de la cible. GEMC enregistre un hit %%flux%% chaque
fois qu'une trajectoire générée traverse ce volume.

```python
# Place a thin scoring plane downstream of the target.
flux_z = 50
flux_dx = 1
flux_dim = world_size * 0.8

# Define the plane as an air box inside the world volume.
gvolume = GVolume("FluxPlane")
gvolume.mother = "root"
gvolume.description = "Flux Scoring Plane"
gvolume.make_box(flux_dim * 0.5, flux_dim * 0.5, flux_dx * 0.5)
gvolume.material = "G4_AIR"
gvolume.color = "FAFAD2"
gvolume.set_position(0, 0, flux_z)

# Turn the volume into a GEMC flux detector and tag its output column.
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
gvolume.publish(cfg)
 ```

<br/><br/>

## Bases de données

Les définitions de détecteurs sont stockées dans des bases de données. Un processus de travail typique comporte
une seule étape réalisée par l'utilisateur :

{% include figure.html
src="/assets/images/gemcArchitecture.svg"
alt="Database-driven architecture"
caption="
Users define detector databases through the Python API (Step 1).
GEMC then builds Geant4 objects, transports particles to create hits, applies digitization and electronics emulation,
and streams the output data (Steps 2–5).
"
%}

<br/>


> [!NOTE]
> L'exécution de simulations ne nécessite aucune connaissance préalable du C++ ou de Geant4.
> Des notions de base en Python aident à organiser les configurations complexes.
> Les utilisateurs peuvent aussi **définir leurs propres routines d'émulation matérielle**. Dans ce cas, des
> notions de base en C++ sont utiles pour les numérisations complexes.

<br/><br/>

## Variations de géométrie

Un détecteur peut être réutilisé d'une expérience à l'autre, avec des changements de configuration tels que des
déplacements de composants, des changements de matériaux ou l'ajout et la suppression de volumes.
GEMC prend en charge ces versions de géométrie à l'aide de chaînes %%variation%% et/ou de numéros %%run%% pour
s'adapter aux différentes configurations de
simulation.

{% include figure.html
src="/assets/images/clas12v.gif"
alt="Python API example"
caption="The animation shows two variations of the CLAS12 Central Detector.
The geometries are identical except for the target position. Users select them
with a variation string or run number in the configuration file or command-line options."
%}

<br/><br/>

## Dernières actualités

<div class="news-feed news-feed--compact news-feed--homepage">
  {% assign shown_posts = 0 %}

{% for post in site.posts %}
{% assign show_post = false %}
{% if post.categories contains "news" %}
{% assign show_post = true %}
{% elsif post.categories contains "release" %}
{% assign show_post = true %}
{% elsif post.categories contains "roadmap" %}
{% assign show_post = true %}
{% endif %}

    {% if show_post %}
      {% include news-card.html post=post compact=true %}
      {% assign shown_posts = shown_posts | plus: 1 %}
    {% endif %}

    {% if shown_posts == 3 %}
      {% break %}
    {% endif %}

{% endfor %}
</div>

<p class="news-links">
  <a href="{{ "/news/" | relative_url }}">Toutes les actualités</a>
  ·
  <a href="{{ "/feed.xml" | relative_url }}">Flux RSS</a>
</p>

<br/><br/>

## Intégration continue

GEMC est compilé, testé et déployé sous forme d'images Docker par l'intégration continue de GitHub sur plusieurs
plateformes et sur les architectures ARM64 et AMD64.

**gemc**

{:.zebra}

| Tests      | [![test][test-badge]][test]                                  |
| Sanitizer  | [![Sanitize][Sanitize-badge]][Sanitize]                      |
| CodeQL | [![CodeQL][CodeQL-badge]][CodeQL]                            |
| Déploiement d'images | [![deploy][deploy-badge]][deploy]                            |
| Archives binaires | [![Binary Tarballs][Binary-Tarballs-badge]][Binary-Tarballs] |
| Archive macOS | [![macOS Tarball][macOS-Tarball-badge]][macOS-Tarball]       |
| Version nocturne | [![Nightly][Nightly-badge]][Nightly]                         |
| Page d'accueil | [![Site][Site-badge]][Site]                                  |
| Téléchargements Docker | [![Docker Pulls][DockerHub-badge]][DockerHub]                |
| Doxygen | [![Docs][Docs-badge]][Docs]                                  |
| Archives de version | [![Release Tarballs][Release-Tarballs-badge]][Release-Tarballs] |

**pygemc**

{:.zebra}

| Version de développement nocturne | [![Nightly Dev Release][PyGemc-Nightly-badge]][PyGemc-Nightly] |
| Publication sur PyPI     | [![Publish PyPI][PyGemc-Publish-badge]][PyGemc-Publish]          |
| Tests | [![pygemc tests][PyGemc-Tests-badge]][PyGemc-Tests]               |
| PyPI | [![pygemc PyPI][PyPI-badge]][PyPI]                               |

<br/><br/>

## Référence

Veuillez citer l'article suivant si vous utilisez GEMC :

> M. Ungaro et la collaboration CLAS, "The CLAS12 Geant4 simulation," *Nuclear Instruments and
> Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated
> Equipment* **959**, 163422 (2020). <https://doi.org/10.1016/j.nima.2020.163422>

BibTeX :

```bibtex
@article{UNGARO2020163422,
  title = {The CLAS12 Geant4 simulation},
  journal = {Nuclear Instruments and Methods in Physics Research Section A: Accelerators,
             Spectrometers, Detectors and Associated Equipment},
  volume = {959},
  pages = {163422},
  year = {2020},
  issn = {0168-9002},
  doi = {https://doi.org/10.1016/j.nima.2020.163422},
  url = {https://www.sciencedirect.com/science/article/pii/S0168900220300279},
  author = {M. Ungaro and {CLAS Collaboration}},
  keywords = {Geant4, GEMC, Simulation, Software, Database, Monte Carlo, CAD, STL, GDML, MYSQL, C++}
}
```

Bibitem :

```latex
\bibitem{UNGARO2020163422}
M. Ungaro and the CLAS Collaboration,
\newblock The CLAS12 Geant4 simulation.
\newblock Nuclear Instruments and Methods in Physics Research Section A \textbf{959}, 163422 (2020).
\newblock \doi{10.1016/j.nima.2020.163422}
```

<br/><br/>

## Code source et licence

Le [code source de GEMC](https://github.com/gemc/src) est distribué sous la
[licence Apache, version 2.0](/home/license/) ; voir [NOTICE](/home/license/#notice) pour les mentions
d'attribution et les remerciements aux tiers. Le logiciel dépend également de composants tiers sous des
licences distinctes, notamment Geant4, CLHEP, Qt, ROOT, SQLite et Assimp.

<br/><br/>

<hr/>
