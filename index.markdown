---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
# See https://github.com/jekyll/minima#readme

layout: default


c1:  "{::nomarkdown}<br/> GEMC databases (txt, mysql) to store simulation parameters like geometry, materials, etc. In addition:<br/><br/>"
c2: "<li>Complex geometries can be created and uploaded to the databases and without programming knowledge</li>"
c3: "<li>Models can be imported from CAD and/or GDML</li>"
c4: "<li>The geometry can be modded at run time, for example by applying tilts / displacements</li><br/>{:/}"
c5: "A typical GEMC usage: detector geometries and materials are loaded from various databases. The Geant4 world is formed, particles are swam through materials, hits are digitized, and output(s) are created."

p1:  "Geant4 volumes are built using the sci-g python API."
p2:  "An example geometry: an Aluminum beamdump is placed inside a flux-sensitive vacuumDetector mother volume."
p3:  "The above snippet is the only code needed to build the geometry and record all tracks in the vacuumDetector in the output."

v1: "<br/> A detector can be re-used in multiple experiments, often with changes such as a shift of some components, a change of materials, the addition or removal of certain volumes.<br/><br/>"
v2: "In GEMC this is controlled by a variables called variations. This has the advantages:"
v3: "{::nomarkdown}<li>Multiple versions of the geometry are indexed using variations</li>"
v4: "<li>The desired geometry variation is selected by using the corresponding string</li>{:/}"
v5: "In the above animation two variations of the CLAS12 Central Detector (clas12CD) are shown. The geometries are identical except for the position of the target. <br/>In the JSON steering card the two variations of clas12CD are loaded by specifying the variation name."
v6: "JSON lines that select the variations shown: <br/><br/> <font size=\"2\"> { \"system\": \"clas12CD\", \"variation\": \"nominal\" } <br/> <br/> { \"system\": \"clas12CD\", \"variation\": \"targetShift\" }</font>"


---


**GE**ant **M**onte-**C**arlo 
is a program based on [geant4](https://geant4.web.cern.ch) 
to simulate the passage of particles through matter.
It provides:<br/><br/>

- Database sources for geometry, materials, calibration constants, and more: nothing is hard-coded
- Detector variations
- Emulation of hardware electronics, time windows
- Pre-defined digitization types such as flux and dosimeter
- Plugins mechanism for generators, fields, digitization, inefficiencies, output

<br/><br/>

| Database sources: code-independent experiment description |             
|----------------------------------------------------------|
| {{ page.c1 }} {{ page.c2 }} {{ page.c3 }} {{ page.c4 }}  |
| ![gemcArch]                                              |
| *{{ page.c5 }}*                                          |

<br/><br/>

| Python API        |                                            |
|-------------------|--------------------------------------------|
| {{ page.p1 }}     | [Scig repo](https://github.com/gemc/sci-g) |
| ![gemcExamplePic] | ![gemcCodeExample]                         |
| {{ page.p2 }}     | *{{ page.p3 }}*                            |

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

