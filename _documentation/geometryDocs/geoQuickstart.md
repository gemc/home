---
layout: default
title: Geometry Quickstart
order: 5
description: solid type builder and volume constructor
---

A system geometry is a collection of volume definitions. 
The volumes can be native geant4 objects or be imported from  CAD / GDML.

Before continuing, make sure you have read the [systems](../documentation/system) documentation and are working
within a system directory. 


# Quickstart: build native Geant4 Volumes

To build native geant4 volumes a set of functions and templates to build the geant4 volumes[^1] can be used.

To following will display the code, shown below, to build a volume, for example a G4Box of 30x40x50 cm:

```python
scigTemplate.py -gv G4Box  -gvp '30 40 50 cm'
```

<script src="https://gist.github.com/maureeungaro/abd7d5efbae00a61107e4b210eff1dd8.js"></script>

you can paste it in the `geometry.py` file and modify it as needed with your desired parameters.

Use the `-silent`  option to omit the printout of the lines commented out with `#`.

Let's go over each line. The lines commented out with `#` set the default values as shown below.


2. volume constructor. The argument is the name of the volume
3. [solid type builder](geometryDocs/solidTypes) . The arguments are its dimensions
4. volume's material name
5. the name of the volume that contains this volume
6. volume's description
7. volume's position. The default unit is `mm` but an optional 4th argument with the unit can be added
8. volume's rotation. The default unit is `deg` but an optional 4th argument with the unit can be added
9. volume's magnetic field
10. volume's color. This is a 6 digits hexadecimal number. For example, `ff0000` is red, 
    `0x00ff00` is green and `0x0000ff` is blue. `0xffffff` is white and `0x000000` is black. An optional int (0-5) 
    7th argument can be added to set the transparency, where 0 is opaque and 5 is transparent
11. volume's style
12. volume's visibility
13. volume's sensitivity: this is the name of the digitization plugin associated with the volume
14. volume's identifier: unique set of pairs (string, id) that identifies the volume

The types builders can be listed with `scigTemplate.py -sl` and can found [here](geometryDocs/solidTypes).

<br/>

In the following recording, a system 'forward' is created and a G4Box is added to the build_target routine in geometry.py 
using the template script:

<script async id="asciicast-sgKptHkpOxagaaQPkBsE7jkwB" src="https://asciinema.org/a/sgKptHkpOxagaaQPkBsE7jkwB.js" data-autoplay="true" data-loop="true"></script>


For more information on how to build native Geant4 volumes, see the [native geometry documentation](geometryDocs/native_geometry).

<br/>

---

<br/>

# How to build import CAD volumes




<br/>
<br/>
<br/>
---
<br/>

[^1]: a geant4 volume is usually 3 objects: a. a solid, that defines the dimensions.  b. a logical volume, that includes materials and fields. c. a physical volume, that places the volume within its mother volume.
