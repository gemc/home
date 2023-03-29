---
layout: default
title: System
order: 1
description: How to create a system, a hierarchical collection of volumes.

s1: "{::nomarkdown}<img width=420/> <ul style='list-style-type: square'>"
s2: "<li>Forward detector   <ul style='list-style-type: \" ⌙ ︎ \" '> "
s3: "<li>paddles <ul style='list-style-type: \" ⌙ ︎ \" '> <li> paddle 1</li> <li> ... </li> </ul> </li>  "
s4: "<li>pmts    <ul style='list-style-type: \" ⌙ ︎ \" '> <li> pmt 1   </li> <li> ... </li> </ul> </li> </ul> </li>"
s5: "<li>Central detector  <ul style='list-style-type: \" ⌙ ︎ \" '> "
s6: "<li>shield </li> <li> paddles <ul style='list-style-type: \" ⌙ ︎ \" '>  "
s7: "<li>light guides  <ul style='list-style-type: \" ⌙ ︎ \" '> <li> lg 1   </li> <li> ... </li> </ul> </li> "
s8: "<li>pmts          <ul style='list-style-type: \" ⌙ ︎ \" '> <li> pmt 1  </li> <li> ... </li> </ul> </li> </ul> </li>"
s9: "</li></ul>{:/}"

---

# Systems


A detector in gemc is composed by one or more *systems*, each a hierarchical collection of geant4 volumes like 
in the example below.


| Systems Hierarchy Visualisation       | Corresponding Hierarchy List                                                                                                  |
|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| [![systems]](../documentation/system) | {{ page.s1 }} {{ page.s2 }} {{ page.s3 }} {{ page.s4 }} {{ page.s5 }} {{ page.s6 }} {{ page.s7 }} {{ page.s8 }} {{ page.s9 }} |


To create a new system, the sci-g template script `scigTemplate.py` can be used. This script creates a new directory 
with the name of the system containing template files with default geometry and materials. 

For example, to create a 'forward' system:

``` 
scigTemplate.py -s forward
```

In the directory `forward`, the following files appear:

- `README.md`:  a template markdown file   
- `forward.py`: the main python script that calls geometry and material builders    
- `geometry.py`: the geometry builder; has a box and a tube as example volumes
- `materials.py`: the materials' builder; shows two different ways to define materials
- `forward.jcard`: the steering card that loads the detector and defines the event generator, the output and the options

To build the detector, execute `forward.py`.  This will create the databases for the geometry and materials. The default 
database format is `text` and the default variation is `default`, so the files 
`forward__geometry_default.txt` and `forward__materials_default.txt` will appear.

The steering card has one pi0 / event is generated and two outputs are defined: a root file and a text file. Modify as 
needed and run gemc:

```
gemc forward.jcard
```

These steps have been summarized in the following recording:

<script async id="asciicast-1wDOXfYmQKs53O31nOIlIDLda" src="https://asciinema.org/a/1wDOXfYmQKs53O31nOIlIDLda.js" data-autoplay="true" data-loop="true"></script>        
			 
                   
# Variations

The `scigTemplate` script accepts a `-v` option to create one or more variations of a system.  
For example, to create a `forward` system with two variations, `default` and `lead_target`:

```
scigTemplate.py -s forward -v default lead_target
```
This will allow to have two versions of the detector. As an example, the `lead_target` variation could be identical
to the default except for the target material. For more details check the [Variations Example](https://github.com/maureeungaro/sci-g/tree/main/examples/variations).





  ## Database factories		
    



<br/>

[systems]: /home/assets/images/systems.png
