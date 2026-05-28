---
layout: default
title: Geometry Quickstart
order: 5
description: solid type builder and volume constructor
---

A system geometry is a collection of volume definitions. 
The volumes can be native Geant4 objects or imported from CAD or GDML files.

Before continuing, make sure you have read the [systems](../documentation/system) documentation and are working
within a system directory. 


# Quickstart: build native Geant4 Volumes

To build native Geant4 volumes, a set of functions and templates to build the Geant4 volumes[^1] can be used.

The following command displays the code needed to build a volume, for example a %%G4Box%% of 30 x 40 x 50 cm:

```python
scigTemplate.py -gv G4Box  -gvp '30 40 50 cm'
```

<script src="https://gist.github.com/maureeungaro/abd7d5efbae00a61107e4b210eff1dd8.js"></script>

You can paste it in `geometry.py` and modify it as needed with your desired parameters.

Use the `-silent`  option to omit the printout of the lines commented out with `#`.

Let's go over each line. The lines commented out with `#` set the default values as shown below.


2. volume constructor. The argument is the name of the volume
3. [solid type builder](solidTypes) . The arguments are its dimensions
4. volume's material name
5. the name of the volume that contains this volume
6. volume's description
7. volume's position. The default unit is %%mm%%, but an optional fourth argument with the unit can be added
8. volume's rotation. The default unit is %%deg%%, but an optional fourth argument with the unit can be added
9. volume's magnetic field
10. volume's color. This is a six-digit hexadecimal number. For example, %%ff0000%% is red,
    %%0x00ff00%% is green, %%0x0000ff%% is blue, %%0xffffff%% is white, and %%0x000000%% is black. An optional integer (0-5)
    7th argument can be added to set the transparency, where 0 is opaque and 5 is transparent
11. volume's style
12. volume's visibility
13. volume's sensitivity: this is the name of the digitization plugin associated with the volume
14. volume's identifier: unique set of pairs (string, id) that identifies the volume

The type builders can be listed with `scigTemplate.py -sl` and can be found [here](geometryDocs/solidTypes).

<br/>

In the following recording, a system %%forward%% is created and a %%G4Box%% is added to the %%build_target%% routine in `geometry.py`
using the template script:

<script async id="asciicast-sgKptHkpOxagaaQPkBsE7jkwB" src="https://asciinema.org/a/sgKptHkpOxagaaQPkBsE7jkwB.js" data-autoplay="true" data-loop="true"></script>


For more information on how to build native Geant4 volumes, see the [native geometry documentation](native_geometry).

<br/>

---

<br/>

# How to build import CAD volumes




<br/>
<br/>
<br/>
---
<br/>

[^1]: a Geant4 volume is usually 3 objects: a. a solid, that defines the dimensions.  b. a logical volume, that includes materials and fields. c. a physical volume, that places the volume within its mother volume.
