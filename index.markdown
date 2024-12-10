---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
# See https://github.com/jekyll/minima#readme

layout: default

description:  "{::nomarkdown} GEMC utilizes databases (ASCII, SQLite, MySQL) to dynamically create Geant4 
simulation objects, including geometry, materials, and more. 
Systems can be created or modified without requiring code recompilation. 
Additionally, geometry can be imported from CAD or GDML files and seamlessly integrated with 
native Geant4 volumes.<br/><br/>
<div style=\"text-align: center;\">
    <img src=\"assets/images/gemcArchitecture.png\" style=\"width: 80%;\" />
</div>
{:/}"
arc_caption: "Typical usage: detector geometries and materials are loaded from various databases sources.
Particles are transported through materials by Geant4, hits are collected and digitized, and output(s) are created.
Notice that GEMC users do not have to code the Geant4 simulation, but only the detector geometry and materials."

api:  "Geant4 volumes are built using the python API.
An example geometry: a flux scintillator paddle collects hits from protons impinging on a liquid hydrogen target"
api_caption:  "The [above snippet](https://gist.github.com/maureeungaro/8e8616b388d65df0c8168a6b205f0c43) is the only code needed to build the geometry and record all tracks hitting the paddle."

v1: "<br/> A detector can be re-used in multiple experiments, with configuration changes such as shifts components, changes of materials, addition or removal of certain volumes.<br/><br/>"
v2: "GEMC can manage this with a string variable called `variation`. This has the advantages:<br/><br/>"
v3: "{::nomarkdown}<li>Multiple versions of a detector are organized  using a single string</li>"
v4: "<li>Easiness to select the desired configuration</li><br/><br/>{:/}"
v5: "In the above animation two variations of the CLAS12 Central Detector (*clas12CD*) are shown. The geometries are identical except for the position of the target. <br/>"
v6: "In the JSON steering card the two variations of clas12CD are loaded by specifying the variation name: <br/><br/> <font size=\"2\"> { \"system\": \"clas12CD\", \"variation\": \"nominal\" } <br/>  { \"system\": \"clas12CD\", \"variation\": \"targetShift\" }</font>"


---

**GEMC** (**GE**ant **M**onte-**C**arlo) is a simulation program built on [Geant4](https://geant4.web.cern.ch)
 designed to leverage databases for modeling the passage of particles through matter. Key features include:<br/>

- Python API
- Support for geometry variations to adapt to different simulation setups
- Pre-packaged signal digitization tools, such as flux and dosimeter simulations
- Plugins mechanism to extend functionality, including custom user generators and digitization
- Emulation of hardware electronics
- Built-in ASCII and [ROOT](https://root.cern) output formats

<br/>

| Database sources: no-code simulations |             
|---------------------------------------|
| {{ page.description }}                |
| *{{ page.arc_caption }}*              |

<br/><br/>

| Python API        |                          |
|-------------------|--------------------------|
| ![gemcExamplePic] | ![gemcCodeExample]       |
| {{ page.api }}    | *{{ page.api_caption }}* |

<br/><br/>

| Detector Variations |                                                         |
|---------------------|---------------------------------------------------------|
| ![clas12v]          | {{ page.v1 }} {{ page.v2 }} {{ page.v3 }} {{ page.v4 }} |
| {{ page.v5 }}       | {{ page.v6 }}                                           |

<br/><br/>



[gemcCodeExample]: assets/images/pythonAPI.png

[gemcExamplePic]: assets/images/pythonAPIGeo.png

[clas12v]: assets/images/clas12v.gif

