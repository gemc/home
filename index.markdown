---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
# See https://github.com/jekyll/minima#readme

layout: default

database_description:  "{::nomarkdown} 
GEMC reads databases to create Geant4 objects (solids, volumes, materials, etc).
<br/><br/>
<div style=\"text-align: center;\">
    <img src=\"assets/images/gemcArchitecture.png\" style=\"width: 90%;\" />
</div>
{:/}"

database_caption: "Typical gemc usage: detectors can be loaded from several databases sources: ASCII, SQLite, GDML, CAD files.
Geant4 volumes, materials, mirrors, optical properties are created. Particles are transported through materials by Geant4. 
Hits are collected and digitized. Disk output(s) are created."

api:  "Geant4 volumes are built using the python API: no code compilation is needed, and no previous knowledge of Geant4 or C++ is required.
An example geometry: a flux scintillator paddle collects hits from protons impinging on a liquid hydrogen target"
api_caption:  "The [snippet above](https://gist.github.com/maureeungaro/8e8616b388d65df0c8168a6b205f0c43) builds the geometry 
on the left and assigns the built in flux detector to record the tracks hitting the paddle."

variations: "<br/><br/><br/> A detector can be re-used in multiple experiments, 
with configuration changes such as components shifts, changes of materials, addition or removal of certain volumes.<br/><br/>
GEMC can manage these changes by using `variations`. This has the advantages:<br/>
{::nomarkdown}<li>Seamless organization of multiple versions of a detector</li>
<li>Easiness to select the desired configuration</li><br/>
In the YAML steering card the two variations of clas12CD are loaded by specifying the variation name: <br/><br/> 
<font size=\"4\"> { \"system\": \"clas12CD\", \"variation\": \"nominal\" } <br/>  { \"system\": \"clas12CD\", \"variation\": \"targetShift\" }</font>
{:/}"

var_caption: "In the above animation two variations of the CLAS12 Central Detector (*clas12CD*) are shown. 
The geometries are identical except for the position of the target. <br/>"

copy_ex: |
  
    def buildGeometry(configuration):

    	# target volume: a G4Tubs (make_tube)
    	# Constructor pars: inner_radius, outer_radius, half-length, starting_angle, total angle
    	gvolume = GVolume('target')
    	gvolume.description = 'Liquid Hydrogen Target'
    	gvolume.make_tube(0, 20, 40, 0, 360)
    	gvolume.material    = 'G4_lH2'	# from GEANT4 materials database
    	gvolume.color       = 'ff0000'
    	gvolume.publish(configuration)

---

{% include mynotes.html %}


![gemcLogo]

<br/>

This site refers to the latest **GEMC** project (version 3 and above). 

For **CLAS12 simulations** please visit [this page](https://github.com/gemc/clas12Tags). 
For previous GEMC version, please visit [this page](https://gemc.jlab.org/gemc/html/index.html).

<br/>

---

<br/>

**GEMC** (**GE**ant **M**onte-**C**arlo) reads databases and
 [Geant4](https://geant4.web.cern.ch) to run simulations of particles through user setups.  

Key features include:<br/>

- Python API
- Databases support for geometry, materials, optical properties and more
- Support for geometry variations and run numbers to adapt to different simulation setups
- Custom extensibility includes fieldmaps, hardware electronics and signal digitization
- Built-in ASCII and [ROOT](https://root.cern) output formats

<br/>


| Databases             |             
|-----------------------|
| {{ page.database_description }} |
| *{{ page.database_caption }}* |

<br/><br/>

|     Python API     |  
|:------------------:|
| ![gemcExamplePic]  | 
|   {{ page.api }}   |


```python
{{ page.copy_ex }}
```
*{{ page.api_caption }}*

<br/><br/>

| Geometry Variations      |                       |
|--------------------------|-----------------------|
| ![clas12v]               | {{ page.variations }} |
| *{{ page.var_caption }}* | {{ page.v6 }}         |


<br/><br/>

---

<br/>

**Continuous Integration**:

[![Almalinux Build](https://github.com/gemc/src/actions/workflows/build_gemc_almalinux.yml/badge.svg)](https://github.com/gemc/src/actions/workflows/build_gemc_almalinux.yml)
[![Fedora Build](https://github.com/gemc/src/actions/workflows/build_gemc_fedora.yml/badge.svg)](https://github.com/gemc/src/actions/workflows/build_gemc_fedora.yml)
[![Ubuntu Build](https://github.com/gemc/src/actions/workflows/build_gemc_ubuntu.yml/badge.svg)](https://github.com/gemc/src/actions/workflows/build_gemc_ubuntu.yml)
[![Doxygen](https://github.com/gemc/src/actions/workflows/doxygen.yaml/badge.svg)](https://github.com/gemc/src/actions/workflows/doxygen.yaml)
[![Sanitize](https://github.com/gemc/src/actions/workflows/sanitize.yaml/badge.svg)](https://github.com/gemc/src/actions/workflows/sanitize.yaml)
[![Nightly Dev Release](https://github.com/gemc/src/actions/workflows/dev_release.yml/badge.svg)](https://github.com/gemc/src/actions/workflows/dev_release.yml)
[![GEMC Homepage Deployment](https://github.com/gemc/home/actions/workflows/jekyll.yml/badge.svg)](https://github.com/gemc/home/actions/workflows/jekyll.yml)


<br/><br/>

---

<br/>

**Reference**:
<br/>

*M. Ungaro*, Geant4 Monte-Carlo (GEMC) A database-driven simulation program, *EPJ Web of Conferences* [**295**, 05005 *(2024)*](https://www.epj-conferences.org/articles/epjconf/abs/2024/05/epjconf_chep2024_05005/epjconf_chep2024_05005.html)

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
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
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

---

<br/>


**Source Code and Licence**:

<br/>

The GEMC source code on ([GitHub](https://github.com/gemc/src)) is distributed under an [open source license](/home/license/).


<br/><br/>

---

<br/>


[gemcCodeExample]: assets/images/pythonAPI.png

[gemcExamplePic]: assets/images/pythonAPIGeo.png

[clas12v]: assets/images/clas12v.gif

[gemcLogo]: assets/images/gemcLogo.png