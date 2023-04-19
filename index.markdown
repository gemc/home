---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
# See https://github.com/jekyll/minima#readme

layout: default


c1:  "{::nomarkdown}<br/> GEMC databases (txt, mysql) to store simulation parameters like geometry, materials, etc. No quantity is hard-coded: systems can be created w/o re-compiling the code."
c2: " In addition:<br/><br/><li>Complex geometries can be built and uploaded to the databases without programming knowledge thanks to an intuitive python API</li>"
c3: "<li>Models can be imported from CAD and/or GDML and mixed with the pyton API's.</li>"
c4: "<li>The geometry can be modded at run time, for example by applying tilts / displacements</li><br/>{:/}"
c5: "A typical GEMC usage: detector geometries and materials are loaded from various databases and the world is formed. Particles are swam through materials by Geant4, hits are digitized, and output(s) are created."

p1:  "Geant4 volumes are built using the sci-g python API."
p2:  "An example geometry: a flux scintillator paddle collects hits from protons impinging on a liquid hydrogen target"
p3:  "The [above snippet](https://gist.github.com/maureeungaro/8e8616b388d65df0c8168a6b205f0c43) is the only code needed to build the geometry and record all tracks hitting the paddle."

v1: "<br/> A detector can be re-used in multiple experiments, with configuration changes such as shifts components, changes of materials, addition or removal of certain volumes.<br/><br/>"
v2: "GEMC can manage this with a string variable called `variation`. This has the advantages:<br/><br/>"
v3: "{::nomarkdown}<li>Multiple versions of a detector are organized  using a single string</li>"
v4: "<li>Easiness to select the desired configuration</li><br/><br/>{:/}"
v5: "In the above animation two variations of the CLAS12 Central Detector (*clas12CD*) are shown. The geometries are identical except for the position of the target. <br/>"
v6: "In the JSON steering card the two variations of clas12CD are loaded by specifying the variation name: <br/><br/> <font size=\"2\"> { \"system\": \"clas12CD\", \"variation\": \"nominal\" } <br/>  { \"system\": \"clas12CD\", \"variation\": \"targetShift\" }</font>"


---

**GEMC** (**GE**ant **M**onte-**C**arlo)
is a program based on [Geant4](https://geant4.web.cern.ch) 
to simulate the passage of particles through matter.
It provides:<br/>

- MYSQL / Text Databases for geometry, materials, calibration constants, digitization
- Detector variations
- Emulation of hardware electronics, time windows
- Pre-defined digitizations such as flux and dosimeter
- Plugins mechanism for generators, fields, digitization, inefficiencies, output
- Built-in text and [ROOT](https://root.cern) output

<br/>

| Database sources: code-independent experiment description |             
|-----------------------------------------------------------|
| {{ page.c1 }} {{ page.c2 }} {{ page.c3 }} {{ page.c4 }}   |
| ![gemcArch]                                               |
| *{{ page.c5 }}*                                           |

<br/><br/>

| Python API                   |                                |
|------------------------------|--------------------------------|
| ![gemcExamplePic]            | ![gemcCodeExample]             |
| {{ page.p1 }}  {{ page.p2 }} | *{{ page.p3 }}*                |

<br/><br/>

| Detector Variations |                                                         |
|---------------------|---------------------------------------------------------|
| ![clas12v]          | {{ page.v1 }} {{ page.v2 }} {{ page.v3 }} {{ page.v4 }} |
| {{ page.v5 }}       | {{ page.v6 }}                                           |


<br/><br/>




[gemcArch]: assets/images/gemcArchitecture.png
[gemcCodeExample]: assets/images/pythonAPI.png
[gemcExamplePic]: assets/images/pythonAPIGeo.png
[clas12v]: assets/images/clas12v.gif

