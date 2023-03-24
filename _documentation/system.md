---
layout: default
title: System
order: 1
description: How to create a system, a hierarchical collection of volumes.

s1: "{::nomarkdown}<img width=420/> <ul style='list-style-type: square'>"
s2: "<li>Forward detector <ul style='list-style-type: \" ⌙ \"'> <li>calorimeter  <li>paddle 22</li> <li>pmt 22</li> <li>...</li> </li>  </li> </ul> </li>"
s3: "<br/><li>Central Detector <ul style='list-style-type: \" ⌙ ︎ \" '> <li>Time Of Flight "
s4: "<ul style='list-style-type: \" ⌙ \"'> <li>lead shield </li> <li>paddles <ul style='list-style-type: \" ⌙ \"'> <li>light guide 42</li> <li>pmt 42</li> </ul>  </li> </ul> "
s5: "</li></ul></li></ul>{:/}"
---

# Systems


A detector in gemc is composed by one or more *systems*, each a hierarchical collection of geant4 volumes like 
in the example below.


| Systems Hierarchy Visualisation       | Corresponding Hierarchy List                                          |
|---------------------------------------|-----------------------------------------------------------------------|
| [![systems]](../documentation/system) | {{ page.s1 }} {{ page.s2 }} {{ page.s3 }} {{ page.s4 }} {{ page.s5 }} |


To create a new system, sci-g the template script `scigTemplate.py` can be used. This script creates a new directory 
with the name of the system and copies template files with default geometry and materials into it. 

For example, to create a 'forward' system:

``` 
scigTemplate.py -s forward
```

In the directory `forward`, the following files are created:


- `README.md`:  a template markdown file   
- `forward.py`: the main python script that calls geometry and material builders    
- `geometry.py`: the geometry builder script. It has a box and a tube as example volumes.
- `materials.py`: the materials builder script. It shows two different ways to define materials.
- `forward.jcard`: the steering card that loads the detector and defines the event generator. the output and the options.

To build the detector, run `forward.py`.  





<script async id="asciicast-GFIOlrFZFpvc34kzifugdQuUE" src="https://asciinema.org/a/GFIOlrFZFpvc34kzifugdQuUE.js" data-autoplay="true" data-loop="true"></script>

    
        
			
                
                   
  ## Variations
                      
			

		
    



<br/>

[systems]: /home/assets/images/systems.png
