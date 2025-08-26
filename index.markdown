---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
# See https://github.com/jekyll/minima#readme

layout: default

description:  "{::nomarkdown} GEMC utilizes databases to create Geant4 
 objects (solids, volumes, materials, etc).
Detectors can be created using the python API. 
<br/><br/>
<div style=\"text-align: center;\">
    <img src=\"assets/images/gemcArchitecture.png\" style=\"width: 90%;\" />
</div>
{:/}"

arc_caption: "Typical gemc usage: detectors can be loaded from several databases sources: ASCII, SQLite, GDML, CAD files.
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
    	gvolume.material    = 'G4_lH2'	# from GEANT4 materials database
    	gvolume.color       = 'ff0000'
    	gvolume.publish(configuration)


    	# target volume: a G4Box (make_box)
    	# Constructor pars: x, y, z half-lengths
    	gvolume = GVolume('paddle')
    	gvolume.description = 'Scintillator paddle'
    	gvolume.make_box(5, 0.5, 5, 'cm')
    	gvolume.material = 'G4_PLASTIC_SC_VINYLTOLUENE'	# from GEANT4 materials database
    	gvolume.set_rotation(90, 0, 0)         # default unit is 'deg'
    	gvolume.set_position(0, 2, 10, 'cm')   # overwriting default unit of 'mm'
    	gvolume.color        = 'f4f4ff'
    	gvolume.digitization = 'flux'
    	gvolume.set_identifier('paddleid', 5)  # identifier for this paddle
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

**GEMC** (**GE**ant **M**onte-**C**arlo) leverages databases and
 [Geant4](https://geant4.web.cern.ch) to run simulations of particles through matter.  

Key features include:<br/>

- Python API to build detectors
- Databases support for geometry, materials, optical properties and more
- Support for geometry variations and run numbers to adapt to different simulation setups
- Custom extensibility includes fieldmaps, hardware electronics and signal digitization
- Built-in ASCII and [ROOT](https://root.cern) output formats

<br/>


| Database and simulations |             
|--------------------------|
| {{ page.description }}   |
| *{{ page.arc_caption }}* |

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

## [Github Source Code](https://github.com/gemc/src)

<br/>

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

- M. Ungaro: Geant4 Monte-Carlo (GEMC) A database-driven simulation program, EPJ Web of Conf.  Volume 295, 2024, [https://doi.org/10.1051/epjconf/202429505005](https://doi.org/10.1051/epjconf/202429505005)

<br/><br/>

---

<br/>


**Licence**:

<br/><br/>
<br/><br/>
<br/><br/>


[gemcCodeExample]: assets/images/pythonAPI.png

[gemcExamplePic]: assets/images/pythonAPIGeo.png

[clas12v]: assets/images/clas12v.gif

[gemcLogo]: assets/images/gemcLogo.png