




## Systems


A detector in gemc is composed by one or more *systems*, each a hierarchical collection of geant4 volumes. 
In the example below an example with two systems, Forward Detector and Central Detector, is shown.


| Systems Hierarchy Visualisation   | Corresponding Hierarchy List                                                                                        |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------|
| ![systems]] | {{ s1 }} {{ s2 }} {{ page.s3 }} {{ page.s4 }} {{ page.s5 }} {{ page.s6 }} {{ page.s7 }} {{ page.s8 }} {{ page.s9 }} |

### Create a system

To create a new system, use the script `templates.py`. It setups a new directory 
with the name of the system containing template files with default geometry and materials. 

For example, to create a `forward` system:

``` 
templates.py -s forward
```

In the directory `forward`, the following files appear:

- `README.md`:  a template markdown file   
- `forward.py`: the main python script that calls geometry and material builders    
- `geometry.py`: the geometry builder; has a box and a tube as example volumes
- `materials.py`: the materials' builder; shows two different ways to define materials
- `forward.jcard`: the steering card that loads the detector and defines the event generator, the output and the options

### Create the system geometry and run gemc

Following the above example, to build the detector, execute `forward.py`.  This will create the databases for the geometry and materials. The default 
database format is `text` and the default variation is `default`, so the files 
`forward__geometry_default.txt` and `forward__materials_default.txt` will appear.

To load the system in gemc, the following entry is added to the steering card:

```json
"+gsystem": [
        {
          "system":   "./forward",
          "factory": "text",
          "variation": "default"
        }
]
```

The steering card also setups 200 events, each with one {{ page.pi0 }}, with two outputs: a root file and a text file. Modify as 
needed and run gemc:

```
gemc forward.jcard
```

These steps have been summarized in the following recording:

<script async id="asciicast-1wDOXfYmQKs53O31nOIlIDLda" src="https://asciinema.org/a/1wDOXfYmQKs53O31nOIlIDLda.js" data-autoplay="true" data-loop="true"></script>        
			 
                   
### Variations

The `templates` script accepts a `-v` option to create one or more variations of a system.  
For example, to create a `forward` system with two variations, `default` and `lead_target`:

```
templates.py -s forward -v default lead_target
```
This will allow to have two versions of the same `forward` detector. As an example, the `lead_target` variation could be identical
to the default except for the target material. For more details check the [Variations Example](https://github.com/maureeungaro/sci-g/tree/main/examples/variations).





### Database factories		
    



<br/>

[systems]: /home/assets/images/systems.png

[s1]: "{::nomarkdown}<img width=420/> <ul style='list-style-type: square'>"
[s2]: "<li>Forward detector   <ul style='list-style-type: \" ⌙ ︎ \" '> "
[s3]: "<li>paddles <ul style='list-style-type: \" ⌙ ︎ \" '> <li> paddle 1</li> <li> ... </li> </ul> </li>  "
[s4]: "<li>pmts    <ul style='list-style-type: \" ⌙ ︎ \" '> <li> pmt 1   </li> <li> ... </li> </ul> </li> </ul> </li>"
[s5]: "<li>Central detector  <ul style='list-style-type: \" ⌙ ︎ \" '> "
[s6]: "<li>shield </li> <li> paddles <ul style='list-style-type: \" ⌙ ︎ \" '>  "
[s7]: "<li>light guides  <ul style='list-style-type: \" ⌙ ︎ \" '> <li> lg 1   </li> <li> ... </li> </ul> </li> "
[s8]: "<li>pmts          <ul style='list-style-type: \" ⌙ ︎ \" '> <li> pmt 1  </li> <li> ... </li> </ul> </li> </ul> </li>"
[s9]: "</li></ul>{:/}"
[pi0]: "&pi;<sup>0</sup>"