---
layout: default

---

[CI]: https://github.com/gemc/src/actions/workflows/dockers_deploy_and_test.yml

[CI-badge]: https://github.com/gemc/src/actions/workflows/dockers_deploy_and_test.yml/badge.svg

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


This site refers to the latest **GEMC** project (version 3 and above).
For **CLAS12 simulations** refer to [this page](https://github.com/gemc/clas12Tags).

{% include gemc-logo.svg %}

<br/>

{% capture left %}

## A database-driven Geant4 simulation application with Python geometry workflows

**GEMC** is a Python-friendly wrapper around [Geant4](https://geant4.web.cern.ch) that eliminates the C++/Geant4
learning curve. Users define geometry in Python, store it in a database, and GEMC handles the full simulation pipeline.

The goal is to lower the entry barrier for Geant4-based simulations, especially for users
who want to prototype detector or radiation-transport setups without writing C++ code.

Highlights:<br/>

- Python API to create geometry and materials
- `ASCII`, `SQLite` `GDML`, `CAD meshes` volume imports
- Built-in `dosimeter`, `flux`, `particle_counter` sensitive types
- `ASCII`, `CSV`, `JSON`, [`ROOT`](https://root.cern) output formats
- [`pyvista`](https://pyvista.org) geometry visualization
- Geometry variations and run-number-dependent configurations
- CI-tested builds and Docker deployment

{% endcapture %}

{% capture right %}

## Latest News

<div class="news-feed news-feed--compact">
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

{% endcapture %}

{% include two_col_md.html left="70%" right="20%" left_content=left right_content=right %}

<br/><br/>

## Try GEMC in Your Browser

No installation needed. Click the badge to launch a live **JupyterLab** session:

{% assign visible_examples = site.data.examples | where: "display", true %}



[qbadge]: https://img.shields.io/badge/mybinder-quickstart-579aca.svg?logo=data:image/png;base64,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
[lbadge]: https://mybinder.org/v2/gh/gemc/binder-tutorials/main?urlpath=lab/tree/notebooks/basic/quickstart.ipynb
[qcsbadge]: https://img.shields.io/badge/codespaces-quickstart-black.svg?logo=github
[qcslink]: https://codespaces.new/gemc/binder-tutorials?devcontainer_path=.devcontainer%2Fquickstart%2Fdevcontainer.json&quickstart=1

{:.zebra.compact-table}
| [![quickstart][qbadge]][lbadge] | [![codespaces][qcsbadge]][qcslink] | Creates a system with a simple detector and a target |

Other examples:

<table class="zebra compact-table">
  <thead>
    <tr>
      <th>Binder</th>
      <th>Codespaces</th>
      <th>Example</th>
    </tr>
  </thead>
  <tbody>
    {% for example in visible_examples %}
    <tr>
      <td>
        <a href="{{ example.binder }}" target="_blank" rel="noopener noreferrer">
          <img src="{{ example.badge }}" alt="{{ example.title }}">
        </a>
      </td>
      <td>
        <a href="{{ example.codespaces }}" target="_blank" rel="noopener noreferrer">
          <img src="{{ example.codespaces_badge }}" alt="{{ example.title }} Codespaces">
        </a>
      </td>
      <td>{{ example.header }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<br/><br/>

## Python API

`Python` is used to create and fill databases with the geometry, materials and mirrors definitions.
GEMC uses these databases to create the Geant4 world and does not need to be re-compiled when the geometry is changed.
The API supports [`pyvista`](https://pyvista.org) visualization of the geometry.

{% include figure.html
src="assets/images/gemc_showcase.gif"
alt="Python API example"
caption="  
The code that fills the database with the world volume, a liquid hydrogen target and a flux plane. <br/>
The pyvista option allows immediate visualization of the geometry. <br/>
In the GEMC simulation, hits are created from particles generated by a beam of protons impinging
on the liquid hydrogen target."
%}

```python
flux_z = 50
flux_dx = 1
flux_dim = world_size * 0.8
gvolume = GVolume("FluxPlane")
gvolume.mother = "root"
gvolume.description = "Flux Scoring Plane"
gvolume.make_box(flux_dim * 0.5, flux_dim * 0.5, flux_dx * 0.5)
gvolume.material = "G4_AIR"
gvolume.color = "FAFAD2"
gvolume.set_position(0, 0, flux_z)
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
gvolume.publish(cfg)
 ```

<p class='image-caption'>
The code used to create the flux plane shown above, showcasing the Python API. 
</p>


<br/><br/>

## Databases

Detector definitions are stored in databases. A typical workflow looks like this:

{% include figure.html
src="assets/images/gemcArchitecture.png"
alt="Database-driven architecture"
caption="
Using the Python API, users fill databases with detector definitions (Step 1).
The rest of the steps are executed by GEMC.
"
%}

<br/>


> [!NOTE]
> Running simulations does not require previous knowledge of C++ or Geant4.
> Basic Python knowledge helps organize complex setups.
> Users can also **define their own hardware emulation routines** - in this case basic C++ knowledge helps
> for complex digitizations.

<br/><br/>

## Geometry Variations

A detector can be re-used in multiple experiments, with configuration changes such as component shifts,
changes of materials, addition or removal of certain volumes.
GEMC supports these geometry versions using **variations** and/or run **numbers** to adapt to different simulation
setups

{% include figure.html
src="assets/images/clas12v.gif"
alt="Python API example"
caption="In the above animation two variations of the CLAS12 Central Detector are shown.
The geometries are identical except for the position of the target. They can be selected
by specifying a variation string or a run number in the configuration file or command line options."
%}

<br/><br/>

## Continuous Integration

GEMC is built, tested, and deployed as Docker images by GitHub CI on several platforms and on both arm64 and amd64
architectures.

{:.zebra}

| Deployment and Testing | [![CI][CI-badge]][CI]                |
| Doxygen | [![Docs][Docs-badge]][Docs]          |
| Nightly Release | [![Nightly][Nightly-badge]][Nightly] |
| Homepage | [![Site][Site-badge]][Site]          |
| Sanitizer | [![Sanitize][Sanitize-badge]][Sanitize]          |
| Code QL | [![CodeQL][CodeQL-badge]][CodeQL]          |

<br/><br/>

## Reference

Please make sure to cite the following paper if you use GEMC:

{:.zebra}
| *M. Ungaro*, Geant4 Monte-Carlo (GEMC) A database-driven simulation program, \*EPJ Web of Conferences* [**295**, 05005
*(
2024)*](https://www.epj-conferences.org/articles/epjconf/abs/2024/05/epjconf_chep2024_05005/epjconf_chep2024_05005.html) |

Bibtex:

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

The GEMC source code on [GitHub](https://github.com/gemc/src) is distributed under
an [open source license](/home/license/).

<br/><br/>

<hr/>
