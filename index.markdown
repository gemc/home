---
layout: default

---

[test]: https://github.com/gemc/src/actions/workflows/test.yml

[test-badge]: https://github.com/gemc/src/actions/workflows/test.yml/badge.svg

[deploy]: https://github.com/gemc/src/actions/workflows/deploy.yml

[deploy-badge]: https://github.com/gemc/src/actions/workflows/deploy.yml/badge.svg

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

[PyPI]: https://pypi.org/project/pygemc/

[PyPI-badge]: https://img.shields.io/pypi/v/pygemc.svg?cacheSeconds=300

[PyGemc-Nightly]: https://github.com/gemc/pygemc/actions/workflows/dev_release.yml

[PyGemc-Nightly-badge]: https://github.com/gemc/pygemc/actions/workflows/dev_release.yml/badge.svg

[PyGemc-Publish]: https://github.com/gemc/pygemc/actions/workflows/publish_pypi.yml

[PyGemc-Publish-badge]: https://github.com/gemc/pygemc/actions/workflows/publish_pypi.yml/badge.svg

[PyGemc-Tests]: https://github.com/gemc/pygemc/actions/workflows/pygemc_tests.yml

[PyGemc-Tests-badge]: https://github.com/gemc/pygemc/actions/workflows/pygemc_tests.yml/badge.svg


{% include gemc-logo.svg %}

<small>This site documents **GEMC** version 3 and later.
For **CLAS12 simulations**, use the [GEMC2 clas12Tags repository](https://github.com/gemc/clas12Tags).</small>

<br/>

## Database-driven Geant4 simulations with a Python API

**GEMC** is a Python-friendly wrapper around [Geant4](https://geant4.web.cern.ch) that eliminates the C++/Geant4
learning curve. Users build complete detector systems in Python: geometry, materials, and digitization. The
API automatically populates the databases that GEMC uses to run the full simulation pipeline.

Highlights:

- Python API to create geometry and materials
- Geometry imports from ASCII, SQLite, GDML, and CAD mesh files
- Built-in sensitive detectors: %%dosimeter%%, %%flux%%, and %%particle_counter%%
- Output formats: ASCII, CSV, JSON, and [ROOT](https://root.cern)
- Built-in Python `analyzer` module for reading and plotting simulation output
- [`pyvista`](https://pyvista.org) geometry visualization
- Geometry variations and run-number-dependent configurations
- CI-tested builds and Docker deployment

<br/><br/>

## Try GEMC

No installation needed. Click a badge to launch a live **JupyterLab** session in your browser:

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

### Container image

For a local or HPC JupyterLab session, use the prebuilt multi-architecture image:

```shell
# Docker
docker run --rm -p 8888:8888 ghcr.io/gemc/binder-tutorials:latest

# Apptainer
apptainer pull gemc-binder-tutorials.sif docker://ghcr.io/gemc/binder-tutorials:latest
apptainer exec gemc-binder-tutorials.sif jupyter lab --ip=0.0.0.0 --no-browser
```

<br/><br/>

## Interactive Gallery

{% assign gallery_examples = site.data.examples | where: "gallery", true %}

<div class="gallery-grid">
  {% for example in gallery_examples %}
    <article class="gallery-card">
      <h3>{{ example.title }}</h3>
      <iframe src="/home/assets/vtkjs-viewer.html?fileURL={{ example.vtksz }}"
        title="Interactive VTK.js view of {{ example.title }}"
        loading="lazy"></iframe>
      <a href="{{ example.link }}">View example</a>
    </article>
  {% endfor %}
</div>

<br/><br/>

## `pygemc`: the Python API

The GEMC Python API, `pygemc`, provides geometry and material database builders, `pyvista` geometry visualization,
`gemc-system-template`, and `gemc-analyzer`. The analyzer can read GEMC CSV and ROOT output and plot
histograms from selected variables.

{% include figure.html
src="assets/images/gemc_showcase.gif"
alt="Python API example"
caption="  
The code fills the database with the world volume, a liquid hydrogen target, and a flux plane. <br/>
The `pyvista` option gives immediate geometry visualization. <br/>
In the GEMC simulation, hits are created from particles generated by a beam of protons impinging
on the liquid hydrogen target.<br/>
The total deposited energy is plotted with the `analyzer` module."
%}

The excerpt below defines the sensitive flux plane downstream of the target. GEMC records a %%flux%% hit each time
a generated track crosses this volume.

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

## Databases

Detector definitions are stored in databases. A typical workflow has one user-authored step:

{% include figure.html
src="assets/images/gemcArchitecture.svg"
alt="Database-driven architecture"
caption="
Users define detector databases through the Python API (Step 1).
GEMC then builds Geant4 objects, transports particles to create hits, applies digitization and electronics emulation,
and streams the output data (Steps 2–5).
"
%}

<br/>


> [!NOTE]
> Running simulations does not require previous knowledge of C++ or Geant4.
> Basic Python knowledge helps organize complex setups.
> Users can also **define their own hardware emulation routines**. In this case, basic C++ knowledge helps
> for complex digitizations.

<br/><br/>

## Geometry Variations

A detector can be reused across experiments, with configuration changes such as component shifts,
material changes, or volume additions and removals.
GEMC supports these geometry versions using %%variation%% strings and/or %%run%% numbers to adapt to different
simulation
setups.

{% include figure.html
src="assets/images/clas12v.gif"
alt="Python API example"
caption="The animation shows two variations of the CLAS12 Central Detector.
The geometries are identical except for the target position. Users select them
with a variation string or run number in the configuration file or command-line options."
%}

<br/><br/>

## Latest News

<div class="news-feed news-feed--compact news-feed--homepage">
  {% assign shown_posts = 0 %}

{% for post in site.posts %}
{% assign show_post = false %}
{% if post.categories contains "news" %}
{% assign show_post = true %}
{% elsif post.categories contains "release" %}
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
  <a href="{{ "/news/" | relative_url }}">All news</a>
  ·
  <a href="{{ "/feed.xml" | relative_url }}">RSS Feed</a>
</p>

<br/><br/>

## Continuous Integration

GEMC is built, tested, and deployed as Docker images by GitHub CI on several platforms and on both ARM64 and AMD64
architectures.

**gemc**

{:.zebra}

| Tests | [![test][test-badge]][test]                                  |
| Sanitizer | [![Sanitize][Sanitize-badge]][Sanitize]                      |
| Image Deploy | [![deploy][deploy-badge]][deploy]                            |
| Binary Tarballs | [![Binary Tarballs][Binary-Tarballs-badge]][Binary-Tarballs] |
| CodeQL | [![CodeQL][CodeQL-badge]][CodeQL]                            |
| Doxygen | [![Docs][Docs-badge]][Docs]                                  |
| Nightly Release | [![Nightly][Nightly-badge]][Nightly]                         |
| Homepage | [![Site][Site-badge]][Site]                                  |

**pygemc**

{:.zebra}

| Nightly Dev Release | [![Nightly Dev Release][PyGemc-Nightly-badge]][PyGemc-Nightly]   |
| Publish to PyPI | [![Publish PyPI][PyGemc-Publish-badge]][PyGemc-Publish]          |
| Tests | [![pygemc tests][PyGemc-Tests-badge]][PyGemc-Tests]              |
| PyPI | [![pygemc PyPI][PyPI-badge]][PyPI]                               |

<br/><br/>

## Reference

Please make sure to cite the following paper if you use GEMC:

{:.zebra}
| *M. Ungaro*, Geant4 Monte-Carlo (GEMC) A database-driven simulation program, \*EPJ Web of Conferences* [**295**, 05005
*(
2024)*](https://www.epj-conferences.org/articles/epjconf/abs/2024/05/epjconf_chep2024_05005/epjconf_chep2024_05005.html) |

BibTeX:

```bibtex 
@INPROCEEDINGS{2024EPJWC.29505005U,
author = { {Ungaro}, Maurizio,
 title = "{Geant4 Monte-Carlo (GEMC) A database-driven simulation program}",
 booktitle = {European Physical Journal Web of Conferences},
 year = 2024,
 series = {European Physical Journal Web of Conferences},
 volume = {295},
 month = may,
 eid = {05005},
 pages = {05005},
 doi = {10.1051/epjconf/202429505005},
 adsurl = {https://ui.adsabs.harvard.edu/abs/2024EPJWC.29505005U},
 adsnote = {Provided by the SAO/NASA Astrophysics Data System} }
}
```

Bibitem:

```latex
\bibitem{2024EPJWC.29505005U}
{Ungaro}, M.: Geant4 Monte-Carlo (GEMC) A database-driven simulation program.
\newblock European Physical Journal Web of Conferences \textbf{295}, 05005 (2024).
\newblock \doi{10.1051/epjconf/202429505005}
```

<br/><br/>

## Source Code and License

The [GEMC source code](https://github.com/gemc/src) is distributed under
an [open source license](/home/license/).

<br/><br/>

<hr/>
