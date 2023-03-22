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


A detector in gemc is composed by one or more *systems*, each a hierarchical collection of geant4 volumes.
In the example below, the forward and central detector systems are defined.


| Systems Hierarchy Visualisation       | Corresponding Hierarchy List                                          |
|---------------------------------------|-----------------------------------------------------------------------|
| [![systems]](../documentation/system) | {{ page.s1 }} {{ page.s2 }} {{ page.s3 }} {{ page.s4 }} {{ page.s5 }} |


To create a new system, sci-g the template script `scigTemplate.py` can be used. This script creates a new directory 
with the name of the system and copies the template files into it. For example, let's create a 'forward' system:

``` 
scigTemplate.py -s forward
```

<script async id="asciicast-GFIOlrFZFpvc34kzifugdQuUE" src="https://asciinema.org/a/GFIOlrFZFpvc34kzifugdQuUE.js" data-autoplay="true" data-loop="true"></script>

    
        
			
                
                   
                        
			

		
    

The volumes can be geant4 objects built using the [sci-g](https://github.com/gemc/sci-g) python api or imported from
CAD / GDML.

<br/>

[systems]: /home/assets/images/systems.png
