---
layout: default
title: Materials
directory: $SCIG/examples/scintillator_array
---

The setup is 5 different targets with materials built using diffent methods.

The geometry is constructed using the python script:

	./material_example.py

<br/>

Sets the desired number of cores, number of events, and verbosity in the jcard 'material_example.jcard'. To run gemc:

	gemc material_example.jcard 

Use the `-gui` option to run interactively:

	gemc material_example.jcard -gui

The geometry looks like this:

![scint_array]{:width="70%"}

<br/>

Another picture with 1000 events leaving hit in the sensitive bars:

![mats]{:width="70%"}


##### Target 1:

Uses a material from the Geant4 Material database.

##### Target 2:

Defines `my_peek` using fractional masses of materials from the Geant4 Material database.

##### Target 3:

Defines `my_epoxy` using number of atoms of pre-defined Geant4 elements.

##### Target 4:

Defines `my_carbonFiber` using fractional masses of `my_epoxy`and from the Geant4 Material database.

##### Target 5:

Defines `my_resistPaste` which uses a material from the Geant4 Material database, but with a different density.

[mats]:       /home/assets/images/examples/materials/five_targets_geo.png
