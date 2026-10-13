---
layout: default
permalink: /
lang: it
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

<small>Questo sito documenta **GEMC** dalla versione 3 in poi.
Per le **simulazioni CLAS12**, utilizza il [repository GEMC2 clas12Tags](https://github.com/gemc/clas12Tags).</small>

<br/>

## Simulazioni Geant4 basate su database con un'API Python

**GEMC** è un wrapper di [Geant4](https://geant4.web.cern.ch) facilmente utilizzabile da Python che elimina la
necessità di apprendere C++ e Geant4. Gli utenti costruiscono sistemi di rivelatori completi in Python: geometria,
materiali e digitizzazione. L'API popola automaticamente i database che GEMC usa per eseguire l'intera simulazione.

Caratteristiche principali:

- API Python per creare geometria e materiali
- Importazione della geometria da ASCII, SQLite, GDML e file di mesh CAD
- Rivelatori sensibili integrati: %%flux%%, %%dosimeter%%, %%particle_counter%% e %%gPhotonDetector%%
- Formati di output: ASCII, CSV, JSON e [ROOT](https://root.cern)
- Modulo Python `analyzer` integrato per leggere l'output della simulazione e rappresentarlo graficamente
- Visualizzazione della geometria con [`pyvista`](https://pyvista.org)
- Variazioni della geometria e configurazioni dipendenti dal numero di run
- Build verificate tramite CI e distribuzione con Docker

<br/><br/>

## Prova GEMC

Non è necessaria alcuna installazione. Fai clic su un badge per avviare una sessione **JupyterLab** nel browser:

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

### Immagine del container

Per una sessione JupyterLab locale o in un ambiente HPC, usa l'immagine precompilata per più architetture:

```shell
# Docker
docker run --rm -p 8888:8888 ghcr.io/gemc/binder-tutorials:latest

# Apptainer
apptainer pull gemc-binder-tutorials.sif docker://ghcr.io/gemc/binder-tutorials:latest
apptainer exec gemc-binder-tutorials.sif jupyter lab --ip=0.0.0.0 --no-browser
```

<br/><br/>

## Galleria 3D interattiva

Ruota la camera con la rotellina del mouse o usa i tasti freccia all'interno di ciascuna miniatura. Fai clic sul
link del titolo per consultare la documentazione.

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

## `pygemc`: l'API Python

L'API Python di GEMC, `pygemc`, offre strumenti per creare database di geometria e materiali, la visualizzazione
della geometria con `pyvista`, `gemc-system-template` e `gemc-analyzer`. L'analizzatore legge l'output CSV e ROOT
di GEMC e traccia istogrammi delle variabili selezionate.

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

L'estratto seguente definisce il piano di flusso sensibile a valle del bersaglio. GEMC registra un hit %%flux%%
ogni volta che una traccia generata attraversa questo volume.

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

## Database

Le definizioni dei rivelatori sono memorizzate in database. Il flusso di lavoro tipico ha un solo passo a cura dell'utente:

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
> L'esecuzione delle simulazioni non richiede conoscenze pregresse di C++ o Geant4.
> Una conoscenza di base di Python aiuta a organizzare configurazioni complesse.
> Gli utenti possono anche **definire le proprie routine di emulazione dell'hardware**. In questo caso, conoscere
> le basi del C++ aiuta a realizzare digitizzazioni complesse.

<br/><br/>

## Variazioni della geometria

Un rivelatore può essere riutilizzato in diversi esperimenti, con modifiche alla configurazione quali
spostamenti dei componenti, cambi di materiale o aggiunte e rimozioni di volumi.
GEMC supporta queste versioni della geometria usando stringhe %%variation%% e/o numeri di %%run%% per adattarsi
a diverse configurazioni di
simulazione.

{% include figure.html
src="/assets/images/clas12v.gif"
alt="Python API example"
caption="The animation shows two variations of the CLAS12 Central Detector.
The geometries are identical except for the target position. Users select them
with a variation string or run number in the configuration file or command-line options."
%}

<br/><br/>

## Ultime notizie

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
  <a href="{{ "/news/" | relative_url }}">Tutte le notizie</a>
  ·
  <a href="{{ "/feed.xml" | relative_url }}">Feed RSS</a>
</p>

<br/><br/>

## Integrazione continua

GEMC viene compilato, testato e distribuito sotto forma di immagini Docker tramite la CI di GitHub su diverse
piattaforme e su entrambe le architetture ARM64 e AMD64.

**gemc**

{:.zebra}

| Test | [![test][test-badge]][test] |
| Sanitizer | [![Sanitize][Sanitize-badge]][Sanitize] |
| CodeQL | [![CodeQL][CodeQL-badge]][CodeQL] |
| Distribuzione delle immagini | [![distribuzione][deploy-badge]][deploy] |
| Archivi tar dei binari | [![Archivi tar dei binari][Binary-Tarballs-badge]][Binary-Tarballs] |
| Archivio tar per macOS | [![Archivio tar per macOS][macOS-Tarball-badge]][macOS-Tarball] |
| Rilascio notturno | [![Rilascio notturno][Nightly-badge]][Nightly] |
| Pagina iniziale | [![Sito][Site-badge]][Site] |
| Download da Docker | [![Download da Docker][DockerHub-badge]][DockerHub] |
| Doxygen | [![Documentazione][Docs-badge]][Docs] |
| Archivi tar dei rilasci | [![Archivi tar dei rilasci][Release-Tarballs-badge]][Release-Tarballs] |

**pygemc**

{:.zebra}

| Rilascio notturno di sviluppo | [![Rilascio notturno di sviluppo][PyGemc-Nightly-badge]][PyGemc-Nightly] |
| Pubblicazione su PyPI | [![Pubblicazione su PyPI][PyGemc-Publish-badge]][PyGemc-Publish] |
| Test | [![test di pygemc][PyGemc-Tests-badge]][PyGemc-Tests] |
| PyPI | [![pygemc su PyPI][PyPI-badge]][PyPI] |

<br/><br/>

## Riferimento bibliografico

Assicurati di citare il seguente articolo se utilizzi GEMC:

> M. Ungaro e la collaborazione CLAS, "The CLAS12 Geant4 simulation," *Nuclear Instruments and
> Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated
> Equipment* **959**, 163422 (2020). <https://doi.org/10.1016/j.nima.2020.163422>

BibTeX:

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

Bibitem:

```latex
\bibitem{UNGARO2020163422}
M. Ungaro and the CLAS Collaboration,
\newblock The CLAS12 Geant4 simulation.
\newblock Nuclear Instruments and Methods in Physics Research Section A \textbf{959}, 163422 (2020).
\newblock \doi{10.1016/j.nima.2020.163422}
```

<br/><br/>

## Codice sorgente e licenza

Il [codice sorgente di GEMC](https://github.com/gemc/src) è distribuito secondo i termini della
[Licenza Apache, versione 2.0](/home/license/); consulta [NOTICE](/home/license/#notice) per le attribuzioni e i
riconoscimenti relativi a terze parti. Il software dipende anche da componenti di terze parti con licenze separate,
tra cui Geant4, CLHEP, Qt, ROOT, SQLite e Assimp.

<br/><br/>

<hr/>
